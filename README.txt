Installation instruction

# install PySAM, pandas
    $ pip install NREL-pySAM, pandas, matplotlib
    
# install MiniZinc
    It can be installed directly through Ubuntu Software Center
    Other installation instructions are available here
    
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
     
