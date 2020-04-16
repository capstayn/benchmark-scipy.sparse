# benchmarking.py - minimal benchmark on linear algebra libraries used by scipy. 
#
# -The script assumes all matrices to use in the benchmarking are allocated
# in three folders: {1k, 5k, 10k} which are on the same directory as the python
# call.
# -The benchmark is actually done by reading MatrixMarket matrices in these
# folders and timing how long takes for scipy.sparse.linalg.spsolve to resolve
# the system AX=B, where A is the input matrix and B is an appropriate column
# vector filled with random values in the range [0, 1] 
#
# Author    - Pedro Cavestany
# Date      - April 2020

# The packages to benchmark
import scipy as sp
import numpy as np

# scipy modules
import scipy.sparse as ss
import scipy.io as sio
import scipy.stats as sst

# system calls and interface
import sys 
import os
import argparse 

# minimal profiler
import timeit

# to capture output of show_config()
import contextlib 
import io

# 1. A loop for folders and matrices
# 2. Read the matrix and import it
# 3. For each matrix create one random array of numbers (B in Ax=B)
# 4. time the call spsolve

def get_library_linked():
    
    # capture into a variable show_config output
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        sp.show_config()
    output = capture.getvalue()

    # look for library in use
    lines = output.split("\n")
    print ("scipy is using: ")
    for line in lines: 
        if "libraries" in line: 
            print ('{}'.format(line))
    print ("you get the gist ;-)\n")

def get_paths():
    # walk through the directory tree and get the paths to our matrices
    # we are in the "sparse_matrices" folder
    paths = []
    k1 = []
    k5 = []
    k10 = []
    
    for (dirpath, dirnames, filenames) in os.walk("."):
        for filename in filenames:
            if filename.endswith('.mtx.gz') and dirpath == "./1k": 
                k1.append(os.sep.join([dirpath, filename]))
            if filename.endswith('.mtx.gz') and dirpath == "./5k": 
                k5.append(os.sep.join([dirpath, filename]))
            if filename.endswith('.mtx.gz') and dirpath == "./10k": 
                k10.append(os.sep.join([dirpath, filename]))

    paths.append(list(k1))
    paths.append(list(k5))
    paths.append(list(k10))

    return paths

def spsolve(path, A, B):
    # Apply spsolve 
    ss.linalg.spsolve(A,B)

def time_spsolve(mat_path, rpt, num):
    
    # Preliminary steps for spsolve
    # A and B should be global for timeit to see them
    global A, B
    #import the sparse matrix from MatrixMarket format
    matmark = sio.mmread(mat_path)
    A = ss.csr_matrix(matmark)

    # Nice formatting
    info = sio.mminfo(mat_path)
    info_arr = np.array(info).flatten()
    print(mat_path,'\t\t', "{: <8} {: <8} {: <10} {: <15} {: <8} {: <10}".format(*info_arr), end='\t')
    
    # Create an array with random values, to be used as B in the system AX=B
    B = sst.uniform.rvs(size=A.shape[0])

    # time spsolve with timeit
    SETUP_CODE = "from __main__ import spsolve, glob_mat_path, A, B" 
    TEST_CODE = "spsolve(glob_mat_path, A, B)"

    # the number of executions <number> and times <repeat> these executions are
    # repeated can be configured.
    bench = timeit.Timer(setup = SETUP_CODE, stmt = TEST_CODE)
    times = bench.repeat(repeat=rpt, number=num) 

    # The most sensible value to show is the minimum result, since all the rest
    # are greater due to interferences with other processes of the system.
    # Therefore, the average proccessing time is estimated by dividing the value
    # corresponding to the minimum test by the number of executions per test.
    print(min(times)/num)   

def main(argv):

    # Parse arguments
    parser = argparse.ArgumentParser(description='Minimal benchmarking on linear algebra libraries used by scipy')
    parser.add_argument('-n', help='Number of executions per test', required=True)
    parser.add_argument('-r', help='Repetitions performed over a test',required=True)
    args = parser.parse_args()
    number = int(args.n)
    repeat = int(args.r)

    # Print what libraries scipy is using: 
    get_library_linked()

    # Get the paths to the matrices
    paths = get_paths()

    print("Number of executions per test: {}.".format(number))
    print("Number of test repetitions: {}.".format(repeat))
    print("Average time taken by spsolve in solving AX=B, for A:\n")
    print('path\t\t\t {: <8} {: <8} {: <10} {: <15} {: <8} {: <10}'
            .format("rows", "columns", "entries", "format", "field", "symmetry"), 
            '\t processing time')
    print('----------------------------------------------------------------------------------------------------------------')
    # We make the test for each folder
    for mats_paths in paths:
        for mat_path in mats_paths:
            # timeit only sees variables from __main__, so I make glob_mat_path
            # global. It is possible to use lambda or partial, but this is
            # simpler
            global glob_mat_path
            glob_mat_path = mat_path
            time_spsolve(mat_path, repeat, number)

main(sys.argv)
