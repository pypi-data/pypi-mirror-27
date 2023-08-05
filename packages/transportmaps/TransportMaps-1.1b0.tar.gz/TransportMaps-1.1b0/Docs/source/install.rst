Installation
============

Supported systems
-----------------

* \*nix like OS (Linux, Unix, ...)
* Mac OS

Other operating systems have not been tested and they likely require a more complex procedure for the installation (this includes the Microsoft Windows family..).

We reccommend to work in a virtual environment using `virtualenv <https://virtualenv.readthedocs.io/en/latest/>`_ or `Anaconda <https://www.continuum.io/why-anaconda>`_.

Installation requirements
-------------------------

* `gcc <https://gcc.gnu.org/>`_ (or an alternative C/C++ compiler), e.g. on Ubuntu:
* `gfortran <https://gcc.gnu.org/fortran/>`_ (or an alternative Fortran compiler), e.g. on Ubuntu:
* `python2 <https://www.python.org/>`_ or `python3 <https://www.python.org/>`_ (with development files)

.. toggle-header::
   :header: Installing requirements on Ubuntu 

     .. prompt:: bash

        sudo apt-get install gcc libc6-dev
        sudo apt-get install gfortran libgfortran3

     with `python2 <https://www.python.org/>`_

     .. prompt:: bash

        sudo apt-get install python python-dev

     or `python3 <https://www.python.org/>`_

     .. prompt:: bash

        sudo apt-get install python3 python3-dev

.. toggle-header:: 
   :header: Installing requirements on Mac OS (using homebrew)

     .. prompt:: bash
        
        brew install llvm
        brew install gfortran

     with `python2 <https://www.python.org/>`_

     .. prompt:: bash

        brew install python

     or `python3 <https://www.python.org/>`_

     .. prompt:: bash

        brew install python3

Installation
------------

First of all make sure to have the latest version of `pip <https://pypi.python.org/pypi/pip>`_ installed

.. prompt:: bash

   pip install --upgrade pip

The package and its python dependencies can be installed running the commands:

.. prompt:: bash

   pip install --upgrade numpy
   pip install --upgrade TransportMaps

If one whish to enable some of the optional dependencies:

.. prompt:: bash

   MPI=True SPHINX=True PLOT=True H5PY=True pip install --upgrade TransportMaps

These options will install the following modules:

* MPI -- parallelization routines (see the `tutorial <mpi-usage.html>`_). It requires the separate installation of an MPI backend (`openMPI <https://www.open-mpi.org/>`_, `mpich <https://www.mpich.org/>`_, etc.). The following Python modules will be installed:

  * `mpi4py <https://pypi.python.org/pypi/mpi4py>`_
  * `mpi_map <https://pypi.python.org/pypi/mpi_map>`_

* PLOT -- plotting capabilities:

  * `MatPlotLib <https://pypi.python.org/pypi/matplotlib/>`_

* SPHINX -- documentation generation packages

* H5PY -- routines for the storage of big data-set. It requires the separate installation of the `hdf5 <https://www.hdfgroup.org/>`_ backend.

  * `mpi4py <https://pypi.python.org/pypi/mpi4py>`_
  * `h5py <http://www.h5py.org/>`_

* PYHMC -- routines for Hamiltonian Markov Chain Monte Carlo

  * `pyhmc <http://pythonhosted.org/pyhmc/>`_

.. toggle-header:: rubric
   :header: Manual installation

     If anything goes wrong with the automatic installation you can try to install from source:

     .. prompt:: bash
                 
        git clone git@bitbucket.org:dabi86/transportmaps.git
        cd transportmaps
        pip install --upgrade numpy
        pip install --upgrade -r requirements.txt
        python setup.py install

     The following optional requirements can be installed as well:

     .. prompt:: bash
   
        pip install --upgrade -r requirements-MPI.txt
        pip install --upgrade -r requirements-PLOT.txt
        pip install --upgrade -r requirements-SPHINX.txt
        pip install --upgrade -r requirements-H5PY.txt

Running the Unit Tests
----------------------

Unit tests are available and can be run through the command:

   >>> import TransportMaps as TM
   >>> TM.tests.run_all()

There are >3500 unit tests, and it will take some time to run all of them.

FAQ
---

.. toggle-header::
   :header: List of Frequently Asked Questions

      * The package ``mpi4py`` fail to install with error: missing <mpi.h>
        One mpi backend must be installed on the machine (e.g. `OpenMPI <https://www.open-mpi.org/>`_, `MPICH <https://www.mpich.org/>`_) and find out where the corresponding header file <mpi.h> is located. Then the package can be installed by setting the environment variables ``CPLUS_INCLUDE_PATH`` or ``C_INCLUDE_PATH``:

        .. prompt:: bash

           CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:<mpi_path> \
           pip install --upgrade mpi4py


