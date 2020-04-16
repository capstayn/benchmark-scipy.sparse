# benchmarking-scipy.sparse
Benchmarking of spsolve function of scipy.sparse on linear algebra libraries used by scipy

## Some remarks on the sparse matrices used

- The .rua files are Harwell-Boeing format.  The .mtx files are MatrixMarket format. 

- The names of the folders indicate the size of the sparse matrices stored in
  them. These matrices have been shopped around [Matrix
  Market](https://math.nist.gov/MatrixMarket/). In each folder their names are
  numbered by convenience, and their actual names and origins are: 

### 1k

1.[jpwh](https://math.nist.gov/MatrixMarket/data/Harwell-Boeing/cirphys/jpwh_991.html)

2.[orsirr](https://math.nist.gov/MatrixMarket/data/Harwell-Boeing/oilgen/orsirr_1.html)

3.[west0989](https://math.nist.gov/MatrixMarket/data/Harwell-Boeing/chemwest/west0989.html)

### 5k

1.[add32](https://math.nist.gov/MatrixMarket/data/misc/hamm/add32.html)

2.[gemat11](https://math.nist.gov/MatrixMarket/data/Harwell-Boeing/gemat/gemat11.html)

### 10k

1.[bcsstk17](https://math.nist.gov/MatrixMarket/data/Harwell-Boeing/bcsstruc2/bcsstk17.html)

2.[E30R4000](https://math.nist.gov/MatrixMarket/data/SPARSKIT/drivcav/e30r4000.html)

## Usage

The script requires two arguments, `-n <int>`, and `-r <int>`, which account for the
number of executions to be run per test and the number of tests to repeat,
respectively. Execute the script with `-h` option for more details.
