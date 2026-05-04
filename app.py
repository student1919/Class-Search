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
ratings_df = pd.read_csv(os.path.join(base_Directory, "data", "matrix_a.csv"), index_col=0)

print(ratings_df.to_numpy)

# Define interests
interests = ["Language", "Arts", "STEM", "Humanities", "Social Science", "Natural Science"]

intrest_course_map = {
    "language": ["ENG BC3521", "FREN UN3867"],
    "arts": ["FILM UN2420"],
    "stem": ["APMA E4008", "COMS W1004"],
    "humanities": ["HIST UN1502", "POLS UN2601"],
    "social_science": ["AHIS BC3867", "ECON UN2261"],
    "natural_science": ["BMEN E4350", "BIOL BC1503"]
}

major_map = {
    # STEM & Engineering Group
    "computer_science": ["COMS", "CSEE", "ELEN"],
    "mechanical_engineering": ["MECE", "IEOR", "APMA"],
    "chemical_engineering": ["CHEN", "BMEN"],
    "biomedical_engineering": ["BMEN", "BIOL", "CHEN"],
    "mathematics": ["MATH", "APMA", "STAT"],
    "statistics": ["STAT", "IEOR", "MATH"],

    # Social Sciences Group
    "economics": ["ECON", "IEOR", "STAT"],
    "political_science": ["POLS", "SIPA"],
    "psychology": ["PSYC", "NEUR"],
    "sociology": ["SOCI", "SOCL"],
    "anthropology": ["ANTH"],

    # Humanities & History Group
    "history": ["HIST", "AMST"],  # AHIS = Asian History
    "philosophy": ["PHIL"],
    "english": ["ENGL", "CLEN"],
    "creative_writing": ["ENGL", "WRIT"],

    # Natural Sciences Group
    "biology": ["BIOL", "BMEN"],
    "neuroscience": ["PSYC", "  BIOL", "NEUR"],

    # Arts & Media Group
    "art_history": ["AHIS","AHAR"], # Standard is AHIS, but we use AHAR to keep Asian History separate
    "film_&_media_studies": ["FILM"]
}



# Function to create user-item matrix
# def create_user_item_matrix():
#     user_item_matrix = pd.DataFrame(np.zeros((len(student_df), len(course_df))), columns=course_df['course_code'], index=student_df['student_id'])
    
#     for student_idx, student in student_df.iterrows():
#         student_id = student['student_id']
#         student_interest = student['stated_interest']
        
#         for course_idx, course in course_df.iterrows():
#             course_category = course['category']
#             if course_category == student_interest:
#                 user_item_matrix.loc[student_id, course['course_code']] = 1
#             else:
#                 user_item_matrix.loc[student_id, course['course_code']] = 0
#     return user_item_matrix

def get_recommended_courses(course_scores_dictionary, ammount=12):
    #sorts the dictionary by which courses are rates the highest from the predicted scores for the new user, and returns the top 6 courses as recommendations
    sorted_dict = dict(sorted(course_scores_dictionary.items(), key=lambda item: item[1], reverse=True))
    return sorted_dict


@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user data from the frontend request
    user_data = request.get_json()
    major = user_data.get('major')
    preferences = user_data.get('preferences')
    
    # Filter or process the data based on the user's input (e.g., major)
    # Generate user-item interaction matrix
    #user_item_matrix = create_user_item_matrix()
    

    # Breaking up the matrix into SVD components
    U1, sig1, V1 = np.linalg.svd(ratings_df.to_numpy(), full_matrices=False)
    U, sigmaMatrix, V = linAlg.SVD(ratings_df.to_numpy())
    

    new_user_vector = linAlg.new_user_vector(preferences, course_df['course_code'].tolist(),intrest_course_map, major, major_map)
   
    
    k_nearest_neighbors = linAlg.KNN(new_user_vector, U, sigmaMatrix, V, 6)
    user_predicted_ratings = linAlg.predict_scores(new_user_vector, k_nearest_neighbors, ratings_df.to_numpy(), course_df['course_code'].tolist())

    
    #generates recomendations for the ui with items from the predicted scores dictionary
    #, and the course names from the course dataframe
    recommendations = []
    for _, course in course_df.iterrows():
        code = course['course_code']
        recommendations.append({
            "course_name": course['course_title'],
            "course_code": code,
            "score": user_predicted_ratings.get(code)
        })

    recommendations.sort(key=lambda x: x['score'], reverse=True)
    return jsonify({"courses": recommendations[:12]})

if __name__ == '__main__':
    app.run(debug=True)