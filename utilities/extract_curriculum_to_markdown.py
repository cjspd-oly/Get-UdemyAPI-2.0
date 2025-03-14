import json


def format_time(content_length_text):
    """Converts time format HH:MM:SS or MM:SS to 'X hr Y min Z sec'."""
    parts = list(map(int, content_length_text.split(":")))

    if len(parts) == 3:  # Format: HH:MM:SS
        hours, minutes, seconds = parts
    elif len(parts) == 2:  # Format: MM:SS
        hours, minutes, seconds = 0, parts[0], parts[1]
    else:
        return "0 sec"

    formatted_time = []
    if hours > 0:
        formatted_time.append(f"{hours} hr")
    if minutes > 0:
        formatted_time.append(f"{minutes} min")
    if seconds > 0:
        formatted_time.append(f"{seconds} sec")

    return " ".join(formatted_time) if formatted_time else "0 sec"


# Load the JSON file
with open("curriculums.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract course and section details
markdown_output = "# 📌 Course Progress Tracker\n\n"
markdown_output += "**Track your progress easily with this TODO list.**\n\n"
markdown_output += "---\n\n"

for course_id, course_data in data.items():
    sections = (
        course_data.get("curriculum_context", {}).get("data", {}).get("sections", [])
    )
    course_title = (
        course_data.get("curriculum_context", {})
        .get("data", {})
        .get("course_title", "Unknown Course")
    )

    markdown_output += f"## 🎯 {course_title}\n"
    markdown_output += f"**Course ID:** `{course_id}`\n\n"

    markdown_output += "### Sections\n"

    for section in sections:
        instructor = section.get("instructor", "Unknown Instructor")
        raw_length = section.get("content_length_text", "00:00")
        formatted_length = format_time(raw_length)

        markdown_output += f"- [ ] **{instructor}** ({formatted_length})\n"

    markdown_output += "\n---\n\n"

# Save output to a markdown file
with open("curriculum_todo.md", "w", encoding="utf-8") as md_file:
    md_file.write(markdown_output)

# Print confirmation message
print("✅ Markdown file 'curriculum_todo.md' has been created successfully!")
