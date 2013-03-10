'''
Created on 07/02/2013

@author: u65838
'''
import numpy as np  
import time  
  
N = 6000  
M = 10000  
  
k_list = [64, 80, 96, 104, 112, 120, 128, 144, 160, 176, 192, 200, 208, 224, 240, 256, 384]  
  
def get_gflops(M, N, K):  
    return M*N*(2.0*K-1.0) / 1000**3  
  

def test_eigenvalue():  
    i= 500 
    data = np.random.random((i,i))  
    result = np.linalg.eig(data) 
    
def test_svd():  
    i = 1000 
    data = np.random.random((i,i))  
    result = np.linalg.svd(data)  
    result = np.linalg.svd(data, full_matrices=False) 
    
def test_inv():  
    i = 1000 
    data = np.random.random((i,i))  
    result = np.linalg.inv(data) 
    
def test_det():  
    """
    Test the computation of the matrix determinant  
    """ 
    i = 1000 
    data = np.random.random((i,i))  
    result = np.linalg.det(data)  

def test_dot():  
    """  
    Test the dot product  
    """ 
    i = 1000 
    a = np.random.random((i, i))  
    b = np.linalg.inv(a)  
    result = np.dot(a, b) - np.eye(i)  



np.show_config()  
  
for K in k_list:  
    a = np.array(np.random.random((M, N)), dtype=np.double, order='C', copy=False)  
    b = np.array(np.random.random((N, K)), dtype=np.double, order='C', copy=False)  
    A = np.matrix(a, dtype=np.double, copy=False)  
    B = np.matrix(b, dtype=np.double, copy=False)  
  
    C = A*B  
  
    start = time.time()  
  
    C = A*B  
    C = A*B  
    C = A*B  
    C = A*B  
    C = A*B  
  
    end = time.time()  
  
    tm = (end-start) / 5.0  
  
    print "{0:4}, {1:9.7}, {2:9.7}".format(K, tm, get_gflops(M, N, K) / tm) 
    
# test eigenvalues
start = time.time()
test_eigenvalue()
end = time.time()
tm = (end-start) / 5.0
print "test eigenvalue,  " + str(tm)

#single value decompositions
start = time.time()
test_svd()
end = time.time()  
tm = (end-start) / 5.0  
print "single value decompositions,  " + str(tm)

#matrix inversions
start = time.time()
test_inv()
end = time.time()  
tm = (end-start) / 5.0  
print "matrix inversions,  " + str(tm)


#Test the computation of the matrix determinant  
start = time.time()
test_det()
end = time.time()  
tm = (end-start) / 5.0  
print "matrix determinant,  " + str(tm)


#Test the dot product
start = time.time()
test_dot()
end = time.time()  
tm = (end-start) / 5.0  
print "dot product,  " + str(tm)