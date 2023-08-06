|mpnum|
=======

A matrix product representation library for Python
--------------------------------------------------

|Travis| |Documentation Status| |Coverage Status| |Code Climate|

mpnum is a flexible, user-friendly, and expandable toolbox for the
matrix product state/tensor train tensor format. mpnum provides:

-  support for well-known matrix product representations, such as:
-  matrix product states
   (`MPS <http://mpnum.readthedocs.org/en/latest/intro.html#matrix-product-states-mps>`__),
   also known as tensor trains (TT)
-  matrix product operators
   (`MPO <http://mpnum.readthedocs.org/en/latest/intro.html#matrix-product-operators-mpo>`__)
-  local purification matrix product states
   (`PMPS <http://mpnum.readthedocs.org/en/latest/intro.html#local-purification-form-mps-pmps>`__)
-  arbitrary matrix product arrays
   (`MPA <http://mpnum.readthedocs.org/en/latest/intro.html#matrix-product-arrays>`__)
-  arithmetic operations: addition, multiplication, contraction etc.
-  `compression <http://mpnum.readthedocs.org/en/latest/mpnum.html#mpnum.mparray.MPArray.compress>`__,
   `canonical
   forms <http://mpnum.readthedocs.org/en/latest/mpnum.html#mpnum.mparray.MPArray.canonicalize>`__,
   etc.
-  finding `extremal
   eigenvalues <http://mpnum.readthedocs.org/en/latest/mpnum.html#mpnum.linalg.eig>`__
   and eigenvectors of MPOs (DMRG)
-  flexible tools for new matrix product algorithms

For more information, see:

-  `Introduction to
   mpnum <http://mpnum.readthedocs.org/en/latest/intro.html>`__
-  `Notebook with code examples
  <https://github.com/dseuss/mpnum/blob/master/examples/mpnum_intro.ipynb>`__
-  `Library reference <http://mpnum.readthedocs.org/en/latest/>`__

Required packages:

-  six, numpy, scipy

Supported Python versions:

-  2.7, 3.4, 3.5, 3.6

Contributors
------------

-  Daniel Suess, daniel@dsuess.me, `University of
   Cologne <http://www.thp.uni-koeln.de/gross/>`__
-  Milan Holzaepfel, mail@mholzaepfel.de, `Ulm
   University <http://qubit-ulm.com/>`__

License
-------

Distributed under the terms of the BSD 3-Clause License

.. |mpnum| image:: https://github.com/dseuss/mpnum/raw/master/docs/mpnum_logo_144.png
.. |Travis| image:: https://travis-ci.org/dseuss/mpnum.svg?branch=master
   :target: https://travis-ci.org/dseuss/mpnum
.. |Documentation Status| image:: https://readthedocs.org/projects/mpnum/badge/?version=latest
   :target: http://mpnum.readthedocs.org/en/latest/?badge=latest
.. |Coverage Status| image:: https://coveralls.io/repos/github/dseuss/mpnum/badge.svg?branch=master
   :target: https://coveralls.io/github/dseuss/mpnum?branch=master
.. |Code Climate| image:: https://codeclimate.com/github/dseuss/mpnum/badges/gpa.svg
   :target: https://codeclimate.com/github/dseuss/mpnum
