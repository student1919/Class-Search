import pandas as pd
import numpy as np


major_map = {
    # STEM & Engineering Group
    "Computer Science": ["COMS", "CSEE", "ELEN"],
    "Mechanical Engineering": ["MECE", "IEOR", "APMA"],
    "Chemical Engineering": ["CHEN", "BMEN"],
    "Biomedical Engineering": ["BMEN", "BIOL", "CHEN"],
    "Mathematics": ["MATH", "APMA", "STAT"],
    "Statistics": ["STAT", "IEOR", "MATH"],

    # Social Sciences Group
    "Economics": ["ECON", "IEOR", "STAT"],
    "Political Science": ["POLS", "SIPA"],
    "Psychology": ["PSYC", "NEUR"],
    "Sociology": ["SOCI", "SOCL"],
    "Anthropology": ["ANTH"],

    # Humanities & History Group
    "History": ["HIST", "AMST"],  # AHIS = Asian History
    "Philosophy": ["PHIL"],
    "English": ["ENGL", "CLEN"],
    "Creative Writing": ["ENGL", "WRIT"],

    # Natural Sciences Group
    "Biology": ["BIOL", "BMEN"],
    "Neuroscience": ["PSYC", "  BIOL", "NEUR"],

    # Arts & Media Group
    "Art History": ["AHIS","AHAR"], # Standard is AHIS, but we use AHAR to keep Asian History separate
    "Film & Media Studies": ["FILM"]
}
# Load your mock data
students = pd.read_csv('data/mock_student_data.csv')
courses = pd.read_csv('data/mock_courses_data.csv')

# 1. Create a "Cross-Join" to get every possible student-course combination
# This creates 38 * 24 = 912 rows
students['key'] = 1
courses['key'] = 1
df = pd.merge(students, courses, on='key').drop("key", axis=1)

# 2. Define the scoring function based on your proposal

def calculate_affinity(row):
    score = 5.0  # Neutral base/Mean imputation [cite: 18]
    
    # 1. Major Match (using the Mapping) - Variable score with randomness
    student_major = row['major']
    course_dept = row['department_code'].strip().upper()
    
    if student_major in major_map:
        if course_dept in major_map[student_major]:
            # Major match: random between 2.0 and 3.5
            score += np.random.uniform(2.0, 3.5)
            
    # 2. Interest Match (Sliders) - Variable score with randomness
    if row['stated_interest'] == row['category']:
        # Interest match: random between 1.0 and 2.5
        score += np.random.uniform(1.0, 2.5)
    
    # 3. Course Popularity (Culpa Rating) - Increased importance
    # Culpa rating now contributes -1.5 to +1.5 (centered at 0 for rating 3.0)
    culpa_contribution = (row['culpa_rating'] - 1) * 0.75 - 1.5
    score += culpa_contribution
    
    # 4. Add some random noise for more variation
    score += np.random.normal(0, 0.3)  # Mean 0, std dev 0.3
        
    return np.round(np.clip(score, 1.0, 10.0), 2)  # Clip between 1.0 and 10.0 and round to 2 decimals

# Create the Matrix
df['affinity_score'] = df.apply(calculate_affinity, axis=1)
matrix_a = df.pivot(index='student_id', columns='course_code', values='affinity_score')
A = matrix_a.to_numpy()

# 3. Apply the logic and Pivot into Matrix A
df['affinity_score'] = df.apply(calculate_affinity, axis=1)
matrix_a = df.pivot(index='student_id', columns='course_code', values='affinity_score')

matrix_a.to_csv("data/matrix_a.csv")

# Convert to a NumPy array for SVD
A = matrix_a.to_numpy()
print(f"Matrix A shape: {A.shape}") # Should be (38, 24)