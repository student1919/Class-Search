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



def SVD(A):
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
    U = A @ V.T / sigmaMatrix
    return U, sigmaMatrix, V

# test_matrix = np.array([[1, 2, 5], [3, 4, 9], [5, 6, 2], [7, 8, 1], [9, 10, 3]])
# U, sigmaMatrix, V = SVD(test_matrix)

def new_user_vector(preferences: dict, all_courses: list, Preference_Map):
   
    #fills in the new student vector with 0s 
    user_vector = np.zeros(len(all_courses))
    #iterates through each course index
    course_index = {code: i for i, code in enumerate(all_courses)}

    #loops through the preferences and fills in the user vector with the slider values
    # mapped to a score between 1 and 10, if the course is specifically one we are looking for
    for pref, slider_value in preferences.items():
        score = 1 + (slider_value / 100) * 9          # maps 0 -> 1, 100 -> 10
        for course_code in Preference_Map.get(pref, []):
            if course_code in course_index:
                user_vector[course_index[course_code]] = score

    return user_vector

def cosine_similarity(vector1, vector2):
    dot_product = np.dot(vector1, np.transpose(vector2))
    normalizedV1 = np.linalg.norm(vector1)
    normalizedV2 = np.linalg.norm(vector2)
    if normalizedV1 == 0 or normalizedV2 == 0:
        return 0.0
    return dot_product / (normalizedV1 * normalizedV2)

def KNN(user_vector, U, V, sigmaMatrix, k=5):
    
    #projects the new user vector into latent space (same space as rows of U)
    user_latent = user_vector @ V.T / sigmaMatrix   # shape (k,)
    
    similarities = []
    for i in range(U.shape[0]):
        similarity = cosine_similarity(user_latent, U[i])
        similarities.append((i, similarity))
    
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:k]

    