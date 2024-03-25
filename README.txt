Installation instruction

# install PySAM, pandas
    $ pip install nrel-pysam==3.0.1, pandas==1.5.3, matplotlib

	## Note 1: We found that the weather file routines have changed in the latest version of PySAM (v5.0.1), which is not yet incorporated in this repository. Therefore, a downgrade to an earlier version of PySAM should be performed. Use the following command to install version 3.0.1: 
	$ pip install nrel-pysam==3.0.1
	Alternatively, you can force reinstall the specific version with:
	$ pip install --force-reinstall nrel-pysam=3.0.1

	## Note 2: We have also noticed that some function routines in pandas have changed since the development of this package. The tested version of pandas in our repository is v1.5.3. When using the latest version of pandas (e.g. v2.2.1), the following revisions are necessary:

    1) The 'append' function should be changed to '_append'.
    2) The variable name 'line_terminator' in the 'to_csv' function should be changed to 'lineterminator' (for example, as used on line 286 in get_weather_data.py).

    
# install MiniZinc
    It can be installed directly through Ubuntu Software Center
    Other installation instructions are available [here](https://www.minizinc.org/).
    
# install openmpi
    $ sudo apt install lam4-dev     # version 7.1.4-6build2, or
    $ sudo apt install mpich        # version 3.3.2-2build1
    $ sudo apt install openmpi-bin  # version 4.0.3-0ubuntu1
    Reference : https://rantahar.github.io/introduction-to-mpi/setup.html 
    
    Check if it is successfully installed by
    $ mpicc --showme:version
    
# install Dakota and openmpi
    $ sudo apt install openmpi-bin libltdl7 liblapack3 libhwloc15 \
  libgslcblas0 libquadmath0 libboost-regex1.71.0 libgsl23 \
  libevent-2.1-7 libgfortran5 libboost-filesystem1.71.0 libopenmpi3 \
  libicu66 libblas3 libstdc++6 libevent-pthreads-2.1-7 \
  libboost-serialization1.71.0 
    $ OS=ubuntu-20.04
    $ DAKOTA_VERSION=6.14.0   
    $ export PKGN=dakota-${DAKOTA_VERSION}-${OS}-x86_64-jp
    $ export DAKURL="https://cloudstor.aarnet.edu.au/plus/s/TaoO6XnrGRiwoiC/download?path=%2F&files=$PKGN.tar.gz"
    $ sudo tar zxv --strip-components=3 -C /usr/local < <(wget "$DAKURL" -q -O-)
    
    Add dakota python package to the PYTHONPATH
    $ export PYTHONPATH=$PYTHONPATH:/usr/local/share/dakota/Python
    or add this path in bashrc
    
# Git clone the package

# run optimisation_LCOH.py    
     
