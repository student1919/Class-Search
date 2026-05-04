from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import linAlg
import os
#from sklearn.decomposition import TruncatedSVD

app = Flask(__name__)
CORS(app)

# Load the data
base_Directory = os.path.dirname(os.path.abspath(__file__))
mock_student_data_path = os.path.join(base_Directory, "data", "mock_student_data.csv")
mock_courses_data_path = os.path.join(base_Directory, "data", "mock_courses_data.csv")
student_df = pd.read_csv(mock_student_data_path)
course_df = pd.read_csv(mock_courses_data_path)

# Define interests
interests = ["Language", "Arts", "STEM", "Humanities", "Social Science", "Natural Science"]

# Function to create user-item matrix
def create_user_item_matrix():
    user_item_matrix = pd.DataFrame(np.zeros((len(student_df), len(course_df))), columns=course_df['course_code'], index=student_df['student_id'])
    
    for student_idx, student in student_df.iterrows():
        student_id = student['student_id']
        student_interest = student['stated_interest']
        
        for course_idx, course in course_df.iterrows():
            course_category = course['category']
            if course_category == student_interest:
                user_item_matrix.loc[student_id, course['course_code']] = 1
            else:
                user_item_matrix.loc[student_id, course['course_code']] = 0
    return user_item_matrix

# Function to apply SVD
# def apply_svd(user_item_matrix):
#     svd = TruncatedSVD(n_components=5)
#     svd_matrix = svd.fit_transform(user_item_matrix)
#     return svd_matrix


@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user data from the frontend request
    user_data = request.get_json()
    major = user_data.get('major')
    preferences = user_data.get('preferences')
    
    # Filter or process the data based on the user's input (e.g., major)
    # Generate user-item interaction matrix
    user_item_matrix = create_user_item_matrix()
    print("User-Item Matrix:")
    print(user_item_matrix)

    # Apply SVD to the matrix
    U, sigmaMatrix, V = linAlg.SVD(user_item_matrix.to_numpy())
    
    # You can then make recommendations based on the SVD matrix and the user's preferences
    # For simplicity, let's return some of the top courses for the user
    recommendations = []
    for idx, course in course_df.iterrows():
        recommendations.append({
            "course_name": course['course_title'],
            "course_code": course['course_code'],
            "score": np.random.random()  # You can calculate a more precise score here
        })

    return jsonify({"courses": recommendations})

if __name__ == '__main__':
    app.run(debug=True)