import re


def parse_resume(text):
    section_aliases = {
        "summary": ["summary", "profile", "professional summary", "career summary", "objective", "career objective",],
        "experience": ["experience", "work experience", "professional experience", "employment history", "work history",],
        "education": ["education", "academic background", "academic qualifications",],
        "skills": ["skills", "technical skills", "core skills", "expertise",],
        "projects": ["projects", "personal projects", "academic projects",],
        "certifications": ["certification", "certifications", "certificates", "licenses & certifications", "certifications & achievements",],
        "achievements": ["achievement", "achievements", "awards", "awards & honors", "accomplishments",],
        "internships": ["internships",]
    }
    parsing_dict = {}
    lines = text.splitlines()
    lines = [line.strip() for line in lines if line.strip() != ""]
    normalized_lines = [line.lower() for line in lines]
    for key, values in section_aliases.items():
        for value in values:
            if value.lower() in normalized_lines:
                parsing_dict[key] = normalized_lines.index(value.lower())
                break
    sorted_dict = sorted(parsing_dict.items(), key=lambda x: x[1])
    section_dict = {}
    for current, next_element in zip(sorted_dict, sorted_dict[1:] + [None]):
        if next_element is not None:
            section_dict[current[0]] = lines[current[1] + 1:next_element[1]]
        else:
            section_dict[current[0]] = lines[current[1] + 1:]

    for index, line in enumerate(lines):
        if line.lower().startswith("impact"):
            section_dict["summary"] = " ".join(lines[index:sorted_dict[0][1]]).split(":",1)[1].strip()
            break
    return section_dict


def find_date(line):
    date_pattern = r"((?:[A-Za-z]+['\s])?\d{2,4})\s*[-–—]\s*((?:[A-Za-z]+['\s])?\d{2,4}|[Pp]resent)"
    return re.findall(date_pattern, line)

def parse_education(lines):
    education_data = []
    for index, line in enumerate(lines):
        education_dict = {}
        matches = find_date(line)
        if matches:
            education_dict["start_date"] = matches[0][0]
            education_dict["end_date"] = matches[0][1]
            details = [i.strip() for i in lines[index-1].split(',')]
            education_dict["institution"] = details[1]
            education_dict["degree"] = details[0]
            education_dict["location"] = details[2]
            education_dict["cgpa"] = details[3].split(":")[1].strip()
        if education_dict:
            education_data.append(education_dict)
    return education_data


def combine_bullet_lines(lines):
    if lines:
        points_list = []
        point = ""
        for i in lines:
            if i.startswith("•"):
                if point != "":
                    points_list.append(point.lstrip("•").strip())
                point = i
            else:
                point += " " + i
        points_list.append(point.lstrip("•").strip())
        return points_list
    else:
        return []


def parse_experience(lines):
    experience_data = []
    date_matches = {}
    for index, line in enumerate(lines):
        date_match = find_date(line)
        if date_match:
            date_matches[index] = date_match
    date_indexes = list(date_matches.keys())
    for  experience_index, (date_index, date_match) in enumerate(date_matches.items()):
        experience_dict = {"start_date": date_match[0][0], "end_date": date_match[0][1], "role": lines[date_index - 1].strip(),
                           "company": lines[date_index + 1].strip(), "location": lines[date_index + 2].strip()}
        if  experience_index+1 < len(date_indexes):
            experience_dict["responsibilities"] = lines[date_index+3: date_indexes[experience_index+1]-1]
        else:
            experience_dict["responsibilities"] = lines[date_index+3:]
        experience_data.append(experience_dict)

    for value in experience_data:
        value['responsibilities'] = combine_bullet_lines(value['responsibilities'])
    return experience_data


def parse_projects(lines):
    project_data = []
    project_headers = {}
    for index, line in enumerate(lines):
        if "|" in line and not line.startswith("|"):
            project_name, technologies = line.split("|", 1)
            project_headers  [index] = (project_name, technologies)

    project_indexes = list(project_headers.keys())
    for i, (key, value) in enumerate(project_headers.items()):
        project_dict = {"project_name": value[0].strip(),
                        "technologies": [value.strip() for value in value[1].split(",")]}
        if i + 1 < len(project_indexes):
            project_dict["project_description"] = lines[key+1: project_indexes[i+1]]
        else:
            project_dict["project_description"] = lines[key+1:]

        project_data.append(project_dict)

    for value in project_data:
        value['project_description'] = combine_bullet_lines(value['project_description'])
    return project_data


def parse_skills(lines):
    skill_data = []
    skill_headings = [
        "Programming",
        "AI & ML",
        "AI Frameworks & Libraries",
        "LLM Concepts",
        "Databases & Tools"
    ]
    section_dict = {}
    for index, line in enumerate(lines):
        for heading in skill_headings:
            if line.startswith(heading):
                section_dict[index] = heading
                break

    for key, value in section_dict.items():
        if lines[key] != value:
            skill_line = lines[key].split(value, 1)[1].strip()
        else:
            skill_line = lines[key + 1].strip()
        skills = [
            skill.strip()
            for skill in skill_line.split(",")
        ]
        skill_dict = {
            "category": value,
            "skills": skills
        }
        skill_data.append(skill_dict)
    return skill_data