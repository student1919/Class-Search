import pandas as pd
import numpy as np

interests = ["Language", "Arts", "STEM", "Humanities", "Social Science", "Natural Science"]

majors = [
  "Computer Science",
  "Economics",
  "Political Science",
  "Psychology",
  "Biology",
  "History",
  "English",
  "Mathematics",
  "Neuroscience",
  "Chemical Engineering",
  "Mechanical Engineering",
  "Biomedical Engineering",
  "Statistics",
  "Philosophy",
  "Anthropology",
  "Sociology",
  "Art History",
  "Creative Writing",
  "Film & Media Studies"
]

# Mapping of majors to interest weights for weighted random selection
major_to_interests = {
    "Computer Science": {"STEM": 0.6, "Language": 0.1, "Arts": 0.1, "Humanities": 0.05, "Social Science": 0.05, "Natural Science": 0.1},
    "Economics": {"Social Science": 0.5, "STEM": 0.2, "Language": 0.1, "Arts": 0.1, "Humanities": 0.05, "Natural Science": 0.05},
    "Political Science": {"Social Science": 0.6, "Humanities": 0.2, "Language": 0.1, "Arts": 0.05, "STEM": 0.03, "Natural Science": 0.02},
    "Psychology": {"Social Science": 0.5, "Natural Science": 0.2, "Humanities": 0.15, "STEM": 0.1, "Language": 0.03, "Arts": 0.02},
    "Biology": {"Natural Science": 0.6, "STEM": 0.2, "Social Science": 0.1, "Humanities": 0.05, "Language": 0.03, "Arts": 0.02},
    "History": {"Humanities": 0.6, "Social Science": 0.2, "Language": 0.1, "Arts": 0.05, "STEM": 0.03, "Natural Science": 0.02},
    "English": {"Language": 0.5, "Humanities": 0.3, "Arts": 0.1, "Social Science": 0.05, "STEM": 0.03, "Natural Science": 0.02},
    "Mathematics": {"STEM": 0.7, "Natural Science": 0.1, "Social Science": 0.1, "Humanities": 0.05, "Language": 0.03, "Arts": 0.02},
    "Neuroscience": {"Natural Science": 0.6, "STEM": 0.2, "Social Science": 0.1, "Humanities": 0.05, "Language": 0.03, "Arts": 0.02},
    "Chemical Engineering": {"STEM": 0.8, "Natural Science": 0.1, "Social Science": 0.05, "Humanities": 0.03, "Language": 0.01, "Arts": 0.01},
    "Mechanical Engineering": {"STEM": 0.8, "Natural Science": 0.1, "Social Science": 0.05, "Humanities": 0.03, "Language": 0.01, "Arts": 0.01},
    "Biomedical Engineering": {"STEM": 0.7, "Natural Science": 0.2, "Social Science": 0.05, "Humanities": 0.03, "Language": 0.01, "Arts": 0.01},
    "Statistics": {"STEM": 0.7, "Social Science": 0.15, "Natural Science": 0.1, "Humanities": 0.03, "Language": 0.01, "Arts": 0.01},
    "Philosophy": {"Humanities": 0.6, "Social Science": 0.2, "Language": 0.1, "Arts": 0.05, "STEM": 0.03, "Natural Science": 0.02},
    "Anthropology": {"Social Science": 0.5, "Humanities": 0.3, "Natural Science": 0.1, "Language": 0.05, "Arts": 0.03, "STEM": 0.02},
    "Sociology": {"Social Science": 0.6, "Humanities": 0.2, "Language": 0.1, "Arts": 0.05, "STEM": 0.03, "Natural Science": 0.02},
    "Art History": {"Arts": 0.4, "Humanities": 0.4, "Language": 0.1, "Social Science": 0.05, "STEM": 0.03, "Natural Science": 0.02},
    "Creative Writing": {"Language": 0.4, "Arts": 0.3, "Humanities": 0.2, "Social Science": 0.05, "STEM": 0.03, "Natural Science": 0.02},
    "Film & Media Studies": {"Arts": 0.5, "Humanities": 0.3, "Language": 0.1, "Social Science": 0.05, "STEM": 0.03, "Natural Science": 0.02},
}

# Generate 38 students 2 per major, with weighted interests based on their major
student_data = []
for i in range(38):
    student_id = f"S_{(i+1):03d}"
    major = majors[i%len(majors)]
    
    # Get weighted interests for this major
    interest_weights = major_to_interests[major]
    weights = np.array([interest_weights[interest] for interest in interests])
    weights = weights / weights.sum()  # Normalize
    
    stated_interest = np.random.choice(interests, p=weights)
    
    student_data.append({
        "student_id": student_id,
        "major": major,
        "stated_interest": stated_interest
    })

# Create DataFrame
df = pd.DataFrame(student_data)
print(df)

df.to_csv("mock_student_data.csv", index=False)

