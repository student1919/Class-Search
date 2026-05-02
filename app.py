from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from the frontend

# Dummy data: Courses and students' preferences (this would be replaced with your real data)
courses = [
    {"id": 1, "name": "Introduction to AI", "category": "STEM"},
    {"id": 2, "name": "Philosophy of Mind", "category": "Humanities"},
    {"id": 3, "name": "Advanced Calculus", "category": "STEM"},
    {"id": 4, "name": "Modern History", "category": "Arts"},
    {"id": 5, "name": "Machine Learning", "category": "STEM"}
]

students = [
    {"id": 1, "major": "computer_science", "preferences": {"language": 30, "arts": 20, "humanities": 40, "social_science": 50, "natural_science": 80, "stem": 90}},
    {"id": 2, "major": "philosophy", "preferences": {"language": 80, "arts": 70, "humanities": 90, "social_science": 60, "natural_science": 40, "stem": 20}}
]

# Dummy function to simulate recommendation
@app.route('/recommend', methods=['POST'])
def recommend():
    user_data = request.get_json()
    user_preferences = np.array([list(user_data["preferences"].values())])  # Convert to NumPy array

    # Simulate SVD (for simplicity, we'll just use random scores here)
    recommendations = []
    for course in courses:
        # Just simulating score by a random value, you'd use cosine similarity here
        score = np.random.random() * 100
        recommendations.append({"name": course["name"], "score": round(score, 2)})

    return jsonify({"courses": recommendations})

if __name__ == '__main__':
    app.run(debug=True)