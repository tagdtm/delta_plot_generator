# distutils: language=c
# cython: language_level=3, boundscheck=False, wraparound=False
# cython: cdivision=True

import numpy as np
cimport numpy as np

def get_data_cython(np.ndarray[int,ndim=2] R, np.ndarray[int,ndim=2] R2, np.ndarray[int,ndim=2] G, np.ndarray[int,ndim=2] G2, np.ndarray[int,ndim=1] R_reference, np.ndarray[int,ndim=1] G_reference, np.ndarray[int,ndim=1] data_r, int height, int width):
    # get data
    # Initialise data (scalor value)
    cdef np.ndarray[int,ndim = 2] data = 200 * np.ones((height,width),dtype=int)
    cdef np.ndarray[int,ndim = 2] data2 = 200 * np.ones((height,width),dtype=int)
    # Count the scalor value matches to the given accuracy
    cdef int count = 0
    cdef int count2 = 0
    cdef int count3 = 0
    # the smaller, the more accurate but less data. the input should be integer.
    cdef int acc = 6
    cdef int acc2 = 4
    cdef int acc3 = 8
    cdef int acc4 = 7
    cdef int acc5 = 1
    cdef int acc6 = 1

    cdef int i,j,x,y
    # select search region (the car region on the picture)
    # This process is done to reduce the computational cost
    # all of the if statement is optimised based on the RBG gradient, so strongly recommended not to touch here
    # There could be further optimisation can be carried on, but it is reasonable for daily usage.
    for y in range(190, 540):
        for x in range(280, width-280):
            # Find scalor value for baseline
            for i in range(100):
                if i < 30 or i > 50:
                    if i < 90:
                        if  R_reference[i] - acc < R[y,x] and R[y,x] < R_reference[i] + acc:
                            if G_reference[i] - acc2 < G[y,x] and G[y,x] < G_reference[i] + acc2:
                                data[y,x] = data_r[i]
                                count += 1
                                count3 +=1
                                break
                    else:
                        if  R_reference[i] - acc5 < R[y,x] and R[y,x] < R_reference[i] + acc5:
                            if G_reference[i] - acc6 < G[y,x] and G[y,x] < G_reference[i] + acc6:
                                data[y,x] = data_r[i]
                                count += 1
                                count3 +=1
                                break
                else:
                    if  R_reference[i] - acc3 < R[y,x] and R[y,x] < R_reference[i] + acc3:
                        if G_reference[i] - acc4 < G[y,x] and G[y,x] < G_reference[i] + acc4:
                            data[y,x] = data_r[i]
                            count += 1
                            count3 +=1
                            break
            # Find scalor value for comparison picture
            for j in range(100):
                if data[y,x] != 200:
                    if j < 30 or j > 50:
                        if j < 90:
                            if  R_reference[j] - acc < R2[y,x] and R2[y,x] < R_reference[j] + acc: 
                                if G_reference[j] - acc2 < G2[y,x] and G2[y,x] < G_reference[j] + acc2:
                                    data2[y,x] = data_r[j]
                                    count2 += 1
                                    break
                        else:
                            if  R_reference[j] - acc5 < R2[y,x] and R2[y,x] < R_reference[j] + acc5:
                                if G_reference[j] - acc6 < G2[y,x] and G2[y,x] < G_reference[j] + acc6:
                                    data2[y,x] = data_r[j]
                                    count2 += 1
                                    break
                    else:
                        if  R_reference[j] - acc3 < R2[y,x] and R2[y,x] < R_reference[j] + acc3:
                            if G_reference[j] - acc4 < G2[y,x] and G2[y,x] < G_reference[j] + acc4:
                                data2[y,x] = data_r[j]
                                count2 += 1                                
                                break
                # If the value for baseline isn't found, we don't search the value for comparison.
                else:
                    break
            # if only one side of data is recognised, that data should be deleted.
            # For example, baseline = 2, and if the comparison = 0, delta is calculate as -2, which is wrong.
            if data[y,x] != 200:
                if data2[y,x] == 200:
                    data[y,x] = 200
                    count -= 1

    print(count,count2,count3, (540-190)*(width-280*2))
    return data, data2