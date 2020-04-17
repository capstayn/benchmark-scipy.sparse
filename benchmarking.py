'''benchmarking.py - minimal benchmark on linear algebra libraries used by
scipy.

 - The script assumes all matrices to use in the benchmarking are allocated in
   three folders: {1k, 5k, 10k} which are on the same directory as the python
   call.
 - The benchmark is actually done by reading MatrixMarket matrices in these
   folders and timing how long takes for scipy.sparse.linalg.spsolve to resolve
   the system AX=B, where A is the input matrix and B is an appropriate column
   vector filled with random values in the range [0, 1]

 Author    - Pedro Cavestany
 Date      - April 2020
'''
# system calls and interface
import os
import argparse

# minimal profiler
import timeit

# to capture output of show_config()
import contextlib
import io

# The packages to benchmark
import numpy as np
import scipy as sp

# scipy modules
import scipy.sparse as ss
import scipy.io as sio
import scipy.stats as sst

# 1. A loop for folders and matrices
# 2. Read the matrix and import it
# 3. For each matrix create one random array of numbers (B in Ax=B)
# 4. time the call spsolve

def get_library_linked():
    '''Print out info about scipy'''

    # capture into a variable show_config output
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        sp.show_config()
    output = capture.getvalue()

    # look for library in use
    lines = output.split('\n')
    print('scipy is using: ')
    for line in lines:
        if 'libraries' in line:
            print('{}'.format(line))
    print('you get the gist ;-)\n')

def get_paths():
    '''walk through the directory tree and get the paths to our matrices
    we are in the "sparse_matrices" folder'''
    paths = []
    small = []
    medium = []
    large = []

    for (dirpath, _, filenames) in os.walk('.'):
        for filename in filenames:
            if filename.endswith('.mtx.gz') and dirpath == './1k':
                small.append(os.sep.join([dirpath, filename]))
            elif filename.endswith('.mtx.gz') and dirpath == './5k':
                medium.append(os.sep.join([dirpath, filename]))
            elif filename.endswith('.mtx.gz') and dirpath == './10k':
                large.append(os.sep.join([dirpath, filename]))
            elif filename.endswith('.mtx.gz'):
                print('WARNING: all .mtx matrices should be in either of\
                        {1k,5k,10k} folders')
                print('Current working directory: {}'.format(os.getcwd()))

    # sort filenames alphabetically
    paths = [sorted(l) for l in [small, medium, large]]
    return paths


def time_spsolve(mat_path, rpt, num):
    '''Dummy docstring'''
    # Preliminary steps for spsolve
    # A and B should be global for timeit to see them
    global A, B
    #import the sparse matrix from MatrixMarket format
    matmark = sio.mmread(mat_path)
    A = ss.csr_matrix(matmark)

    # Nice formatting
    info = sio.mminfo(mat_path)
    info_arr = np.array(info).flatten()
    print(
        mat_path,
        '\t\t',
        '{: <8} {: <8} {: <10} {: <15} {: <8} {: <10}'.format(*info_arr),
        end='\t')

    # Create an array with random values, to be used as B in the system AX=B
    B = sst.uniform.rvs(size=A.shape[0])

    # time spsolve with timeit
    setup_code = '''from __main__ import A, B
from scipy.sparse.linalg import spsolve'''
    test_code = 'spsolve(A, B)'

    # the number of executions <number> and times <repeat> these executions are
    # repeated can be configured.
    bench = timeit.Timer(setup=setup_code, stmt=test_code)
    times = bench.repeat(repeat=rpt, number=num)

    # The most sensible value to show is the minimum result, since all the rest
    # are greater due to interferences with other processes of the system.
    # Therefore, the average proccessing time is estimated by dividing the value
    # corresponding to the minimum test by the number of executions per test.
    print(min(times)/num)

def main():
    '''Dummy docstring'''
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='Minimal benchmarking on linear algebra libraries used by scipy')
    parser.add_argument(
        '-n', help='Number of executions per test', required=True)
    parser.add_argument(
        '-r', help='Repetitions performed over a test', required=True)
    args = parser.parse_args()
    number = int(args.n)
    repeat = int(args.r)

    # Print what libraries scipy is using:
    get_library_linked()

    # Get the paths to the matrices
    paths = get_paths()

    print('Number of executions per test: {}.'.format(number))
    print('Number of test repetitions: {}.'.format(repeat))
    print('Average time taken by spsolve in solving AX=B, for A:\n')
    print(
        'path\t\t\t {: <8} {: <8} {: <10} {: <15} {: <8} {: <10}'
        .format('rows', 'columns', 'entries', 'format', 'field', 'symmetry'),
        '\t processing time')
    print('-'*117)
    # We make the test for each folder
    for mats_paths in paths:
        for mat_path in mats_paths:
            # timeit only sees variables from __main__. It is possible to use
            # lambda or partial, but this is simpler
            time_spsolve(mat_path, repeat, number)

if __name__ == '__main__':
    main()
