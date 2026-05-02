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

test_matrix = np.array([[1, 2, 5], [3, 4, 9], [5, 6, 2], [7, 8, 1], [9, 10, 3]])
U, sigmaMatrix, V = SVD(test_matrix)

# print('The matrix U is \n', U, '\n')

# print('The diagonal entries of Sigma are \n', sigmaMatrix, '\n')

# print('The matrix VT is \n', V, '\n')

# u, s, vt = np.linalg.svd(test_matrix, full_matrices=False)

# print("Built in SVD from numpy: \n")
# print('The matrix U is \n', u, '\n')

# print('The diagonal entries of Sigma are \n', s, '\n')

# print('The matrix VT is \n', vt, '\n')

# def predict_User_Score(user, item, U, sigmaMatrix, V):
    
    
# def cosine_similarity(vecA, vecB):
#     return np.dot(vecA, vecB) / (np.linalg.norm(vecA) * np.linalg.norm(vecB))    