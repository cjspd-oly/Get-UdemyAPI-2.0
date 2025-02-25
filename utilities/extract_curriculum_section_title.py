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

    section_titles = [
        section["instructor"] for section in sections if "instructor" in section
    ]

    # Store titles under course ID
    course_sections[course_id] = section_titles

# Print result
for course_id, sections in course_sections.items():
    print(f"\nCourse ID: {course_id}")
    print("---------------------")
    for section in sections:
        print(section)
