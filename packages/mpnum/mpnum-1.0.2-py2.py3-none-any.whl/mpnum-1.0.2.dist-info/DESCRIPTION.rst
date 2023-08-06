[MPNUM]


A matrix product representation library for Python

mpnum is a flexible, user-friendly, and expandable toolbox for the
matrix product state/tensor train tensor format. mpnum provides:

-   support for well-known matrix product representations, such as:
-   matrix product states (MPS), also known as tensor trains (TT)
-   matrix product operators (MPO)
-   local purification matrix product states (PMPS)
-   arbitrary matrix product arrays (MPA)
-   arithmetic operations: addition, multiplication, contraction etc.
-   compression, canonical forms, etc.
-   finding extremal eigenvalues and eigenvectors of MPOs (DMRG)
-   flexible tools for new matrix product algorithms

To install the latest stable version run

    pip install mpnum

If you want to install mpnum from source, please run (on Unix)

    git clone https://github.com/dseuss/mpnum.git
    cd mpnum
    pip install .

In order to run the tests and build the documentation, you have to
install the development dependencies via

    pip install -r requirements.txt

For more information, see:

-   Introduction to mpnum
-   Notebook with code examples
-   Library reference
-   Contribution Guidelines

Required packages:

-   six, numpy, scipy

Supported Python versions:

-   2.7, 3.4, 3.5, 3.6

Alternatives:

-   TT-Toolbox for Matlab
-   ttpy for Python
-   ITensor for C++


How to contribute

Contributions of any kind are very welcome. Please use the issue tracker
for bug reports. If you want to contribute code, please see the section
on how to contribute in the documentation.


Contributors

-   Daniel Suess, daniel@dsuess.me, University of Cologne
-   Milan Holzaepfel, mail@mholzaepfel.de, Ulm University


License

Distributed under the terms of the BSD 3-Clause License (see LICENSE).


Citations

mpnum has been used and cited in the following publications:

-   I. Dhand et al. (2017), arXiv 1710.06103
-   I. Schwartz, J. Scheuer et al. (2017), arXiv 1710.01508
-   J. Scheuer et al. (2017), arXiv 1706.01315
-   B. P. Lanyon, Ch. Maier et al, Nat. Phys. (2017), arXiv 1612.08000



