# Get-UdemyAPI-2.0
    Get Instructor & Course Information by using Udemy API 2.0

---


<br>
<br>
<br>

# 🎓 **UdemyAPI** - Fetch & Organize Udemy Courses & Curriculums 🚀

Welcome to **UdemyAPI**! 🎉 This Python tool is designed to interact with Udemy's API to help you **fetch courses** taught by instructors, extract detailed **curriculum data**, and save all this valuable information in a **structured JSON format** for easy use! Whether you're an educator 🧑‍🏫, student 🎓, or simply exploring Udemy’s extensive library 📚, this tool can streamline your learning experience! ✨

---

## 🛠️ **Features** 

✨ **Main Features:**
- **Fetch Instructor Courses** 📜: Retrieve the list of courses taught by a specific Udemy instructor.
- **Extract Detailed Curriculum** 📖: Pull the curriculum data for any course (sections, lectures, and more).
- **Instructor's Title Included** 🧑‍🏫: Each course’s data includes the instructor’s title for additional context.
- **Save Data as JSON** 💾: Save the fetched course and curriculum data in a clean, structured **JSON** file.

---

## 💻 **Installation Guide**

### Requirements:
To get started, you'll need:
- **Python 3.x** 🐍
- **Requests library**: A simple Python library for making HTTP requests.
  ```bash
  pip install requests
  ```

Once the dependencies are installed, you're ready to fetch courses and curriculums! 🎉

---

## 📝 **Usage Instructions**

### Code Overview 🛠️

The code is organized into two main classes:

1. **`UdemyAPI`**: This class is responsible for making requests to Udemy’s API to fetch courses and curriculum data. It acts as the **connector** to Udemy's API.
2. **`UdemyDataProcessor`**: This class takes the fetched data and processes it, cleaning and organizing it into a structured format. It also handles saving the data into **JSON files**.

---

### 🧑‍💻 **Code Breakdown** 🧐

#### 1️⃣ **`UdemyAPI` Class** - Interact with Udemy’s API 🎯

```python
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
```

- **Description**: This class is the bridge between your Python application and Udemy’s API. It uses specific **headers** for requests to ensure the proper format of the response.

---

#### 2️⃣ **Fetching Courses** 📚

```python
def fetch_taught_courses(self, profile_id: str) -> Dict:
    """
    Fetches the courses taught by a given Udemy instructor profile ID.
    """
    url = f"https://www.udemy.com/api-2.0/users/{profile_id}/taught-profile-courses/?learn_url"
```

- **Input**: **Profile ID** of a Udemy instructor (unique identifier).
- **Output**: A list of courses taught by the instructor with details like course title, course ID, and course URL. 📜
- **Purpose**: Retrieves courses associated with an instructor's profile for further processing.

---

#### 3️⃣ **Fetching Course Curriculum** 📘

```python
def fetch_course_curriculum(self, course_id: str, components: str = "curriculum_context") -> Dict:
    """
    Fetches curriculum data for a given Udemy course ID.
    """
    url = f"https://www.udemy.com/api-2.0/course-landing-components/{course_id}/me/?components={components}"
```

- **Input**: **Course ID** of a Udemy course.
- **Output**: Curriculum data that includes sections, lectures, and related content.
- **Purpose**: Extracts the full curriculum for a given course, which is structured as sections with lecture items.

---

#### 4️⃣ **`UdemyDataProcessor` Class** - Process and Save Data 📝

```python
class UdemyDataProcessor:
    """
    A class to process and save Udemy API data.
    """
    def extract_and_filter_curriculum(self, raw_data: Dict, course_info: Dict, user_title: str) -> Dict:
        """
        Extracts and filters curriculum data from the raw API response and adds course-specific details.
        """
```

- **Description**: This class processes the raw data from Udemy’s API to filter out unnecessary information and organizes the data into a usable format.
  
  - **Extract relevant curriculum data**: It filters out sections and lectures.
  - **Add instructor titles**: Each course is tagged with the instructor’s title for easy identification.

---

### 🔄 **Main Flow of the Script** 🔄

Here’s the workflow of how the script operates from start to finish:

1. **Input**: A list of **Udemy profile IDs** (comma-separated).
2. **Fetch Courses**: For each profile ID, the script fetches all courses taught by that instructor.
3. **Process Courses**: For each course, it extracts the **instructor’s title** and appends it to the course details.
4. **Fetch Curriculum**: After extracting courses, the script fetches and processes the **curriculum data** for each course.
5. **Save Data**: Finally, all the fetched and processed data is saved in **JSON files**:
   - `taught_courses.json`: Contains details of all courses.
   - `curriculums.json`: Contains the curriculum data of the courses.

```python
if __name__ == "__main__":
    # Initialize API and Processor
    udemy_api = UdemyAPI()
    data_processor = UdemyDataProcessor()

    # Input: List of profile IDs (provided dynamically)
    profile_ids = input("Enter Udemy profile IDs (comma-separated): ").split(",")
    profile_ids = [pid.strip() for pid in profile_ids if pid.strip()]  # Clean the inputs

    # Fetch and Save Taught Courses
    courses_output_file = "taught_courses.json"
    data_processor.fetch_and_save_taught_courses(profile_ids, courses_output_file, udemy_api)

    # Fetch and Save Curriculums
    with open(courses_output_file, "r") as file:
        taught_courses_data = json.load(file)
    courses = []
    for profile_id, course_data in taught_courses_data.items():
        user_title = course_data["instructor"]  # Extract instructor title
        for course in course_data["results"]:
            # Add instructor title to each course
            course["user_title"] = user_title
            courses.append(course)

    curriculums_output_file = "curriculums.json"
    data_processor.fetch_and_save_curriculums(courses, curriculums_output_file, udemy_api)
```

- **Step-by-Step Flow**:
  1. **Fetch taught courses** using `fetch_and_save_taught_courses`.
  2. **Process** and **add instructor titles** to the course data.
  3. **Fetch and filter curriculum data** for each course.
  4. **Save the structured data** to JSON files: `taught_courses.json` and `curriculums.json`.

---

### 🧑‍🏫 **File Structure** 🗂️

Here’s how the project is organized:

```
/UdemyAPI
    ├── udemy_api.py           # The main Python script with all the logic
    ├── taught_courses.json    # JSON file containing the list of taught courses
    ├── curriculums.json       # JSON file containing the detailed curriculum data
    ├── README.md              # This README file 📖
    └── requirements.txt       # List of dependencies 📜
```

---

## 🚀 **How to Run the Script** 🎉

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/UdemyAPI.git
   cd UdemyAPI
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the script**:
   ```bash
   python udemy_api.py
   ```

4. **Input**: The script will prompt you to enter a list of Udemy profile IDs (comma-separated). 📌
5. **Output**: The script will fetch the data and save it in:
   - `taught_courses.json` 📜
   - `curriculums.json` 📘

---

## 🤝 **Contributing** 🌟

We love **open-source contributions**! If you want to help improve the project:
1. **Fork** the repository 🍴
2. Create a **new branch** 🌱
3. **Commit** your changes 💻
4. **Open a pull request** 📨

---

## 🛡️ **License** 📜

This project is licensed under the **MIT License**. You can check the [LICENSE](LICENSE) file for more details.

---

## 👏 **Acknowledgements** 🙌

A big thanks to **Udemy** for providing the API! 🎓 Without them, this tool wouldn't be possible!

---

## 🔧 **Troubleshooting** 🛠️

If you run into any issues while using this project, here are some common problems and their solutions:

### 1. **Problem: Missing Dependencies**

**Error Message**:
```
ModuleNotFoundError: No module named 'requests'
```

**Solution**:
Make sure to install all dependencies by running:
```bash
pip install -r requirements.txt
```

### 2. **Problem: API Rate Limits** ⏳

If you get an error message related to API rate limits (e.g., **429 Too Many Requests**), it means you're sending too many requests in a short period. Udemy’s API has rate limits to prevent abuse. Here's what you can do:
- **Wait a while** and try again.
- Implement **rate-limiting** in your script to handle this gracefully.

### 3. **Problem: Missing or Incorrect Profile IDs**

**Error Message**:
```
Error fetching courses for profile ID XYZ: 404 Not Found
```

**Solution**:
Double-check that you’ve entered the correct **Udemy Profile ID** for the instructor. It should look something like `2994446` (numeric ID). If the instructor has a public profile, you can find their ID in the URL of their profile page.

---

## 📝 **Future Improvements** 🌟

There are several features and improvements that could be added to this project:

1. **Rate Limiting**: Implement rate-limiting in the script to avoid hitting API limits.
2. **Error Handling**: Improve error handling for network-related issues and edge cases.
3. **Course Metadata**: Add additional course metadata (e.g., course description, ratings, etc.) to the output JSON.
4. **Curriculum Summary**: Add a feature to generate a **curriculum summary** based on course sections and lectures.
5. **Automated Scheduling**: Implement a scheduler to automatically fetch new courses and curriculum updates periodically.

---

## 🧑‍🤝‍🧑 **Community & Support** 💬

If you need help or want to discuss improvements, feel free to reach out:
- **GitHub Discussions**: Use the GitHub issues tab to ask questions or report bugs.
- **Social Media**: Share your experience with the project and follow for updates.

---

## 👀 **Watch & Star** ⭐

If you find this project useful, don’t forget to:
- ⭐ **Star** the repository on GitHub to show your support!
- 👀 **Watch** the repository to stay updated with the latest changes!

---

## 🚀 **Enjoy using UdemyAPI!** 🎉

We hope this tool helps you enhance your Udemy learning experience, whether you’re a student or instructor. Stay curious, and happy learning! 🎓📚

---

<!-- ## 🔗 **Links** 🌐

- [Udemy API Documentation](https://www.udemy.com/developers/)
- [Udemy](https://www.udemy.com/) 

---
-->