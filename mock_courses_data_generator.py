import pandas as pd
import numpy as np


df = pd.read_csv("data/2026-Spring.csv")

print(df.head(5))
print(df.columns)
print(df.shape[0])

print(list(df.columns))

included_schools = [
"Barnard College",
"Columbia College",
"Engineering:Undergraduate",
"General Studies"]

# Keep only courses open to the included schools
# df = df[df['open_to'].str.contains('|'.join(included_schools), na=False)]

new_df =df.drop(columns=['scheduled_time_start', 'scheduled_time_end', 'call_number', 'campus', 'class_id', 'course_subtitle','location', 'method_of_instruction', 'open_to', 'scheduled_days', 'section_key', 'type'])
# Drop courses that have prerequisites
new_df = new_df[new_df['prerequisites'].isna() | (new_df['prerequisites'] == '')]

# Drop courses with specific course codes
excluded_codes = ["ACCT", "CHEN", "BUSI", "DVPR", "JOUR", "LAW", "MTFC", "SIPA", "ACTU"]
new_df = new_df[~new_df['course_code'].str.contains('|'.join(excluded_codes), na=False)]

# Keep only courses with course code numbers between 1 and 4 (e.g., B1000-B4999 or BC1000-BC4999)
def extract_course_level(course_code):
    import re
    # Extract the number part after school code letter(s) (1 or 2 letters)
    # Format: DEPARTMENT [SCHOOL_CODE(1-2 letters)]NUMBER
    match = re.search(r'[A-Z]{1,2}(\d+)$', course_code)
    if match:
        number = match.group(1)
        return int(number[0])  # Get the first digit
    return None

new_df['course_level'] = new_df['course_code'].apply(extract_course_level)
new_df = new_df[new_df['course_level'].isin([1, 2, 3, 4])]
new_df = new_df.drop(columns=['course_level'])

# Exclude courses with "Project" or "Research" in the title
new_df = new_df[~new_df['course_title'].str.contains('Project|Research', case=False, na=False)]

# Exclude courses with "Independent Study" or "Disc" in the title
new_df = new_df[~new_df['course_title'].str.contains('Study|Disc|Seminar|Rec', case=False, na=False)]

# Categorize courses by subject area
def categorize_course(course_code):
    stem_codes = ["CSOR", "CSEE", "CSAS", "IEOR", "CSEN", "APMA", "ECON", "MATH", "STAT", "PHYS", "CHEM", "BIOL", "COMS"]
    social_science_codes = ["ECON", "POLS", "PSYC", "SOCI", "ANTH"]
    humanities_codes = ["PHIL", "HIST", "CLAS", "COMP", "RELI"]
    language_codes = ["AHIS", "ENGL", "CHIN", "FREN", "GERM", "ITAL", "JAPN", "KORE", "RUSS", "SPAN", "ARAB"]
    arts_codes = ["ARTE", "ARTW", "ARTX", "ARTH", "MUSC", "DANC", "FILM", "VISA"]
    natural_science_codes = ["BIOL", "ASTR", "BMEN", "BIET", "CHEM", "EEES"]
    
    code_prefix = course_code.split()[0] if ' ' in course_code else course_code
    
    if any(code_prefix.startswith(prefix) for prefix in stem_codes):
        return "STEM"
    elif any(code_prefix.startswith(prefix) for prefix in social_science_codes):
        return "Social Science"
    elif any(code_prefix.startswith(prefix) for prefix in humanities_codes):
        return "Humanities"
    elif any(code_prefix.startswith(prefix) for prefix in language_codes):
        return "Language"
    elif any(code_prefix.startswith(prefix) for prefix in arts_codes):
        return "Arts"
    elif any(code_prefix.startswith(prefix) for prefix in natural_science_codes):
        return "Natural Science"
    else:
        return "Other"

new_df['category'] = new_df['course_code'].apply(categorize_course)

# Select courses by category with specified counts
category_counts = {
    "STEM": 6,
    "Social Science": 5,
    "Humanities": 4,
    "Language": 3,
    "Arts": 3,
    "Natural Science": 3
}

selected_courses = []
for category, count in category_counts.items():
    category_df = new_df[new_df['category'] == category]
    if len(category_df) >= count:
        selected = category_df.sample(n=count, random_state=42)
        selected_courses.append(selected)

new_df = pd.concat(selected_courses, ignore_index=True)

# Add culpa rating column with random values between 1.00 and 5.00
new_df['culpa_rating'] = np.random.uniform(1.00, 5.00, len(new_df)).round(2)

print(new_df.head(5))
print(new_df.shape[0])
print("\nCategory distribution:")
print(new_df['category'].value_counts())

new_df.to_csv("mock_courses_data.csv", index=True)
