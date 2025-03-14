import json

# Load the JSON file
with open("curriculums.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract section titles grouped by course
course_sections = {}
for course_id, course_data in data.items():
    sections = (
        course_data.get("curriculum_context", {}).get("data", {}).get("sections", [])
    )
    course_title = (
        course_data.get("curriculum_context", {})
        .get("data", {})
        .get("course_title", "Unknown Course")  # Ensure default value if missing
    )

    section_titles = [
        section["instructor"] for section in sections if "instructor" in section
    ]

    # Store titles under course ID
    course_sections[course_id] = {
        "course_title": course_title,
        "sections": section_titles,
    }

# Print result
for course_id, course_info in course_sections.items():
    print(f"\nCourse ID: {course_id}; Course Title: {course_info['course_title']}")
    print("---------------------")
    for section in course_info["sections"]:
        print(section)
