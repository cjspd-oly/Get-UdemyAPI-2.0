import requests
import json
from typing import List, Dict


class UdemyAPI:
    """
    A class to interact with Udemy's API and fetch instructor profile and course data.
    """

    def __init__(self):
        """Initialize UdemyAPI with required headers."""
        self.headers = {
            "accept": "application/json, text/plain, */*",
            "x-udemy-cache-device": "None",
            "x-udemy-cache-language": "en",
        }

    def fetch_taught_courses(self, profile_id: str) -> Dict:
        """
        Fetches the courses taught by a given Udemy instructor profile ID.

        Args:
            profile_id (str): The profile ID of the instructor.

        Returns:
            Dict: Filtered course data, including the instructor's title.
        """
        url = f"https://www.udemy.com/api-2.0/users/{
            profile_id}/taught-profile-courses/?learn_url"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            raw_data = response.json()
        except requests.RequestException as e:
            print(f"Error fetching courses for profile ID {profile_id}: {e}")
            return {}

        # Extract the first instructor's title (if available)
        visible_instructors = raw_data.get("results", [{}])[
            0].get("visible_instructors", [])
        user_title = visible_instructors[0].get(
            "title", "Unknown Instructor") if visible_instructors else "Unknown Instructor"

        # Filter and return the response
        return {
            "instructor": user_title,
            "count": raw_data.get("count", 0),
            "results": [
                {
                    "id": course.get("id"),
                    "title": course.get("title"),
                    "url": course.get("url"),
                }
                for course in raw_data.get("results", [])
            ],
        }

    def fetch_course_curriculum(self, course_id: str, components: str = "curriculum_context") -> Dict:
        """
        Fetches curriculum data for a given Udemy course ID.

        Args:
            course_id (str): The ID of the Udemy course.
            components (str): The components to request from the Udemy API (default: "curriculum_context").

        Returns:
            Dict: Parsed JSON response containing curriculum data.
        """
        url = f"https://www.udemy.com/api-2.0/course-landing-components/{
            course_id}/me/?components={components}"

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching data for course ID {course_id}: {e}")
            return {}


class UdemyDataProcessor:
    """
    A class to process and save Udemy API data.

    Methods:
        extract_and_filter_curriculum(raw_data: Dict, course_info: Dict) -> Dict
        fetch_and_save_taught_courses(profile_ids: List[str], output_file: str)
        fetch_and_save_curriculums(course_ids: List[Dict], output_file: str)
    """

    @staticmethod
    def extract_and_filter_curriculum(raw_data: Dict, course_info: Dict, user_title: str) -> Dict:
        """
        Extracts and filters curriculum data from the raw API response and adds course-specific details.

        Args:
            raw_data (Dict): Raw JSON data returned by the Udemy API.
            course_info (Dict): A dictionary containing course-specific information (e.g., title, URL).
            user_title (str): The title (name) of the instructor.

        Returns:
            Dict: Filtered curriculum data containing only relevant fields.
        """
        curriculum_context = raw_data.get(
            "curriculum_context", {}).get("data", {})
        filtered_sections = []

        for section in curriculum_context.get("sections", []):
            filtered_section = {
                "instructor": section.get("title", ""),
                "content_length_text": section.get("content_length_text", ""),
                #  ? -1: Invalid lecture count
                "lecture_count": section.get("lecture_count", -1),
                "items": [
                    {
                        "title": item.get("title", ""),
                        "content_summary": item.get("content_summary", ""),
                        # ? 404 Not Found
                        "learn_url": item.get("learn_url", "ERROR404"),
                        # ? -1: Invalid object index
                        "object_index": item.get("object_index", -1),
                        # ? 400 Bad Request: If the file type is malformed or missing
                        "item_type": item.get("item_type", "ERROR400"),
                    }
                    for item in section.get("items", [])
                ],
            }
            filtered_sections.append(filtered_section)

        return {
            "instructor": user_title,
            "curriculum_context": {
                "data": {
                    "sections": filtered_sections,
                    "estimated_content_length_text": curriculum_context.get(
                        "estimated_content_length_text", ""
                    ),
                    "num_of_published_lectures": curriculum_context.get(
                        "num_of_published_lectures", 0
                    ),
                    "course_title": course_info.get("title", ""),
                    "course_url": course_info.get("url", ""),
                }
            },
        }

    def fetch_and_save_taught_courses(
        self, profile_ids: List[str], output_file: str, api: UdemyAPI
    ):
        """
        Fetches and saves taught courses data for multiple Udemy profiles.

        Args:
            profile_ids (List[str]): List of Udemy profile IDs.
            output_file (str): Name of the JSON file to save the data.
            api (UdemyAPI): An instance of UdemyAPI to fetch data.
        """
        all_taught_courses = {}

        for profile_id in profile_ids:
            print(f"Fetching courses for profile ID {profile_id}...")
            data = api.fetch_taught_courses(profile_id)
            if data:
                all_taught_courses[profile_id] = data
            else:
                print(f"Skipping profile ID {profile_id} due to an error.")

        try:
            with open(output_file, "w") as file:
                json.dump(all_taught_courses, file, indent=4)
            print(f"Taught courses data saved to {output_file}")
        except IOError as e:
            print(f"Error saving data to file: {e}")

    def fetch_and_save_curriculums(
        self, courses: List[Dict], output_file: str, api: UdemyAPI
    ):
        """
        Fetches and saves curriculum data for multiple Udemy courses.

        Args:
            courses (List[Dict]): List of dictionaries containing course IDs and their additional details.
            output_file (str): Name of the JSON file to save the data.
            api (UdemyAPI): An instance of UdemyAPI to fetch data.
        """
        all_curriculums = {}

        for course in courses:
            course_id = course["id"]
            user_title = course.get("user_title", "Unknown Instructor")
            print(f"Fetching curriculum for course ID {course_id}...")
            raw_data = api.fetch_course_curriculum(course_id)
            if raw_data:
                filtered_data = self.extract_and_filter_curriculum(
                    raw_data, course, user_title)
                all_curriculums[course_id] = filtered_data
            else:
                print(f"Skipping course ID {course_id} due to an error.")

        try:
            with open(output_file, "w") as file:
                json.dump(all_curriculums, file, indent=4)
            print(f"Curriculum data saved to {output_file}")
        except IOError as e:
            print(f"Error saving data to file: {e}")


if __name__ == "__main__":
    # Initialize API and Processor
    udemy_api = UdemyAPI()
    data_processor = UdemyDataProcessor()

    # Input: List of profile IDs (provided dynamically)
    profile_ids = input(
        "Enter Udemy profile IDs (comma-separated): ").split(",")
    profile_ids = [pid.strip()
                   for pid in profile_ids if pid.strip()]  # Clean the inputs

    # Step 1: Fetch taught courses for all profile IDs
    courses_output_file = "taught_courses.json"
    data_processor.fetch_and_save_taught_courses(
        profile_ids, courses_output_file, udemy_api)

    # Step 2: Read the fetched courses and extract course IDs
    with open(courses_output_file, "r") as file:
        taught_courses_data = json.load(file)
    courses = []
    for profile_id, course_data in taught_courses_data.items():
        user_title = course_data["instructor"]  # Extract instructor title
        for course in course_data["results"]:
            # Add instructor title to each course
            course["user_title"] = user_title
            courses.append(course)

    # Step 3: Fetch curriculums for the extracted courses
    curriculums_output_file = "curriculums.json"
    data_processor.fetch_and_save_curriculums(
        courses, curriculums_output_file, udemy_api)
