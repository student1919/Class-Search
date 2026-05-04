#SVD implentation for recomendation system
import numpy as np

#taken from online https://www.sfu.ca/~jtmulhol/py4math/linalg/np-gramschmidt/
def gram_schmidt(A):
    '''input: A set of linearly independent vectors stored
              as the columns of matrix A
       outpt: An orthongonal basis for the column space of A.'''
    # get the number of vectors.
    A = np.copy(A).astype(np.float64) # create a local instance of the array
    n = A.shape[1]
    for j in range(n):
        # For the vector in column j, find the perpendicular
        # of the projection onto the previous orthogonal vectors.
        for k in range(j):
            A[:, j] -= np.dot(A[:, k], A[:, j]) * A[:, k]
        # If original vectors aren't lin indep then we can check for this:
        # 
        if np.isclose(np.linalg.norm(A[:, j]), 0, rtol=1e-15, atol=1e-14, equal_nan=False):
            A[:, j] = np.zeros(A.shape[0])
        else:    
            A[:, j] = A[:, j] / np.linalg.norm(A[:, j])
    return A



def SVD(A, k=10):
    #compresses matrix A to the k-rank apporoximation, returning decompressed A
    Atranspose = np.transpose(A)
    Atranspose_A  = Atranspose@A
    w, v = np.linalg.eigh(Atranspose_A) # w = eigenvalues, v= eigenvectors
    indicies = np.argsort(w)[:: -1] # sorts by descending
    w = w[indicies]
    v = v[:, indicies]
    #check the line below
    V = gram_schmidt(v).T

    singularValues = np.sqrt(np.abs(w))
    sigmaMatrix = np.sort(singularValues)[:: -1] # sorts by descending

    k = min(A.shape)
    #truncate to sigma and Vt to k-rank approximation
    sigmaMatrix = sigmaMatrix[:k]
    V = V[:k]
    U = A @ V.T / sigmaMatrix
    return U, sigmaMatrix, V

# test_matrix = np.array([[1, 2, 5], [3, 4, 9], [5, 6, 2], [7, 8, 1], [9, 10, 3]])
# U, sigmaMatrix, V = SVD(test_matrix)

def new_user_vector(preferences: dict, all_courses: list, Preference_Map, major, major_map):
   
    #fills in the new student vector with 0s 
    user_vector = np.zeros(len(all_courses))
    #iterates through each course index
    course_index = {code: i for i, code in enumerate(all_courses)}
    #print(major)
    matched_depts = major_map.get(major, [])
    #loops through the preferences and fills in the user vector with the slider values
    # mapped to a score between 1 and 10, if the course is specifically one we are looking for
    
    for pref, slider_value in preferences.items():
        score = 1 + (int(slider_value) / 100) * 9# maps 0 -> 1, 100 -> 10
       
        #print(Preference_Map.get(pref, []))
        for course_code in Preference_Map.get(pref, []):
           # print("Preference:", pref, "Course Code:", course_code, "Score:", score)
            if course_code in course_index:
                user_vector[course_index[course_code]] = score

            course_dept = course_code.strip().split()[0].upper()
            if any(course_dept.startswith(dept) for dept in matched_depts):
                score += np.random.uniform(2.25, 2.75)
                user_vector[course_index[course_code]] = np.clip(score, 1.0, 10.0)
    
    return user_vector

def cosine_similarity(vector1, vector2, mask=None):
    if mask is not None:
        #hides the values that you want to skip over, in this case, hides the 0s from the user vector and the corresponding values from the course vector
        vector1 = vector1[mask]
        vector2 = vector2[mask]
    dot_product = np.dot(vector1, vector2)
    normalizedV1 = np.linalg.norm(vector1)
    normalizedV2 = np.linalg.norm(vector2)
    if normalizedV1 == 0 or normalizedV2 == 0:
        return 0.0
    return dot_product / (normalizedV1 * normalizedV2)

def KNN(user_vector, U, sigmaMatrix, V, k=5):
    #K-nearest neighbors algorithm to find the k most similar course vectors in U to the user vector using cosine similarity
    
    #takes all indicies of the sigma matrix that are zero and sets them to 1, to avoid a division by 0 error
    sigmaMatrix = np.where(sigmaMatrix > 1e-10, sigmaMatrix, 1.0)
    #projects the new user vector into latent space, which is the same space as rows of U
    
    user_latent = user_vector @ V.T / sigmaMatrix   

    similarities = []

    mask = user_vector > 0
    for i in range(U.shape[0]):
        #calculates the cosine similarity between the new user vector and each course vector in U, 
        #only considering the dimensions where the user vector has non-zero values
        similarity = cosine_similarity(user_latent, U[i], mask = mask)
        similarities.append((i, similarity))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:k]

def predict_scores(user_vector, neighbors, ratings_matrix, all_courses):
    predicted_vector = user_vector.copy()
    #calculate probable ratings from the new user to each course
    for i in range(len(all_courses)):
        sum = 0
        for student in neighbors:
            student_id = student[0]
            #finds an average rating from the neighbors for each course
            other_student_rating = ratings_matrix[student_id][i]
            sum += other_student_rating
        #saves the predicted score for the course as the average rating from the neighbors
        predicted_vector[i] = sum / len(neighbors) if len(neighbors) > 0 else 0
    
    #crates a dictionary mapping course codes to predicted scores for the new user
    ratings_Dictionary = {course: predicted_vector[i] for i, course in enumerate(all_courses)}
    return ratings_Dictionary