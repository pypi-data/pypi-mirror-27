.. _install:

Installation
============

.. note:: 

   Fermipy is only compatible with Science Tools v10r0p5 or later.  If
   you are using an earlier version, you will need to download and
   install the latest version from the `FSSC
   <http://fermi.gsfc.nasa.gov/ssc/data/analysis/software/>`_.  Note
   that it is recommended to use the *non-ROOT* binary distributions
   of the Science Tools.

These instructions assume that you already have a local installation
of the Fermi Science Tools (STs).  For more information about
installing and setting up the STs see :ref:`stinstall`.  If you are
running at SLAC you can follow the `Running at SLAC`_ instructions.
For Unix/Linux users we currently recommend following the
:ref:`condainstall` instructions.  For OSX users we recommend
following the :ref:`pipinstall` instructions.  The
:ref:`dockerinstall` instructions can be used to install the STs on
OSX and Linux machines that are new enough to support Docker.

.. _stinstall:

Installing the Fermi Science Tools
----------------------------------

The Fermi STs are a prerequisite for fermipy.  To install the STs we
recommend using one of the non-ROOT binary distributions available
from the `FSSC
<http://fermi.gsfc.nasa.gov/ssc/data/analysis/software/>`_.  The
following example illustrates how to install the binary distribution
on a Linux machine running Ubuntu Trusty:

.. code-block:: bash

   $ curl -OL http://fermi.gsfc.nasa.gov/ssc/data/analysis/software/tar/ScienceTools-v10r0p5-fssc-20150518-x86_64-unknown-linux-gnu-libc2.19-10-without-rootA.tar.gz
   $ tar xzf ScienceTools-v10r0p5-fssc-20150518-x86_64-unknown-linux-gnu-libc2.19-10-without-rootA.tar.gz
   $ export FERMI_DIR=ScienceTools-v10r0p5-fssc-20150518-x86_64-unknown-linux-gnu-libc2.19-10-without-rootA/x86_64-unknown-linux-gnu-libc2.19-10
   $ source $FERMI_DIR/fermi-init.sh

More information about installing the STs as well as the complete list
of the available binary distributions is available on the `FSSC
software page
<http://fermi.gsfc.nasa.gov/ssc/data/analysis/software/>`_.
   
.. _pipinstall:

Installing with pip
-------------------

These instructions cover installation with the ``pip`` package
management tool.  This method will install fermipy and its
dependencies into the python distribution that comes with the Fermi
Science Tools.  First verify that you're running the python from the
Science Tools

.. code-block:: bash

   $ which python

If this doesn't point to the python in your Science Tools install
(i.e. it returns /usr/bin/python or /usr/local/bin/python) then the
Science Tools are not properly setup.

Before starting the installation process, you will need to determine
whether you have setuptools and pip installed in your local python
environment.  You may need to install these packages if you are
running with the binary version of the Fermi Science Tools distributed
by the FSSC.  The following command will install both packages in your
local environment:

.. code-block:: bash

   $ curl https://bootstrap.pypa.io/get-pip.py | python -

Check if pip is correctly installed:

.. code-block:: bash

   $ which pip

Once again, if this isn't the pip in the Science Tools, something went
wrong.  Now install fermipy by running

.. code-block:: bash

   $ pip install fermipy

To run the ipython notebook examples you will also need to install
jupyter notebook:
   
.. code-block:: bash

   $ pip install jupyter

.. Running pip and setup.py with the ``user`` flag is recommended if you do not
.. have write access to your python installation (for instance if you are
.. running in a UNIX/Linux environment with a shared python
.. installation).  To install fermipy into the common package directory
.. of your python installation the ``user`` flag should be ommitted.

Finally, check that fermipy imports:

.. code-block:: bash

   $ python
   Python 2.7.8 (default, Aug 20 2015, 11:36:15)
   [GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.56)] on darwin
   Type "help", "copyright", "credits" or "license" for more information. 
   >>> from fermipy.gtanalysis import GTAnalysis
   >>> help(GTAnalysis)

.. _condainstall:
   
Installing with Anaconda Python
-------------------------------

.. note:: 

   The following instructions have only been verified to work with
   binary Linux distributions of the Fermi STs.  If you are using OSX
   or you have installed the STs from source you should follow the
   :ref:`pipinstall` thread above.

These instructions cover how to use fermipy with a new or existing
anaconda python installation.  These instructions assume that you have
already downloaded and installed the Fermi STs from the FSSC and you
have set the ``FERMI_DIR`` environment variable to point to the location
of this installation.

If you already have an existing anaconda python installation then fermipy
can be installed from the conda-forge channel as follows:

.. code-block:: bash

   $ conda config --append channels conda-forge
   $ conda install fermipy
   
If you do not have an anaconda installation, the ``condainstall.sh``
script can be used to create a minimal anaconda installation from
scratch.  First download and source the ``condainstall.sh`` script
from the fermipy repository:

.. code-block:: bash

   $ curl -OL https://raw.githubusercontent.com/fermiPy/fermipy/master/condainstall.sh
   $ source condainstall.sh

If you do not already have anaconda python installed on your system
this script will create a new installation under ``$HOME/miniconda``.
If you already have anaconda installed and the ``conda`` command is in
your path the script will use your existing installation.  After
running ``condainstall.sh`` fermipy can be installed with conda:

.. code-block:: bash

   $ conda install fermipy

Alternatively fermipy can be installed from source following the
instructions in :ref:`gitinstall`.

Once fermipy is installed you can initialize the ST/fermipy
environment by running ``condasetup.sh``:

.. code-block:: bash

   $ curl -OL https://raw.githubusercontent.com/fermiPy/fermipy/master/condasetup.sh 
   $ source condasetup.sh

If you installed fermipy in a specific conda environment you should
switch to this environment before running the script:
   
.. code-block:: bash

   $ source activate fermi-env
   $ source condasetup.sh

.. _dockerinstall:

Installing with Docker
----------------------

.. note::

   This method for installing the STs is currently experimental
   and has not been fully tested on all operating systems.  If you
   encounter issues please try either the pip- or anaconda-based
   installation instructions.

Docker is a virtualization tool that can be used to deploy software in
portable containers that can be run on any operating system that
supports Docker.  Before following these instruction you should first
install docker on your machine following the `installation instructions
<https://docs.docker.com/engine/installation/>`_ for your operating
system.  Docker is currently supported on the following operating
systems:

* macOS 10.10.3 Yosemite or later
* Ubuntu Precise 12.04 or later
* Debian 8.0 or later
* RHEL7 or later
* Windows 10 or later

Note that Docker is not supported by RHEL6 or its variants (CentOS6,
Scientific Linux 6).

These instructions describe how to create a docker-based ST
installation that comes preinstalled with anaconda python and fermipy.
The installation is fully contained in a docker image that is roughly
2GB in size.  To see a list of the available images go to the `fermipy
Docker Hub page <https://hub.docker.com/r/fermipy/fermipy/tags/>`_.
Images are tagged with the release version of the STs that was used to
build the image (e.g. 11-05-00).  The *latest* tag points to the image
for the most recent ST release.

To install the *latest* image first download the image file:

.. code-block:: bash

   $ docker pull fermipy/fermipy
   
Now switch to the directory where you plan to run your analysis and execute
the following command to launch a docker container instance:

.. code-block:: bash
   
   $ docker run -it --rm -p 8888:8888 -v $PWD:/workdir -w /workdir fermipy/fermipy

This will start an ipython notebook server that will be attached to
port 8888.  Once you start the server it will print a URL that you can
use to connect to it with the web browser on your host machine.  The
`-v $PWD:/workdir` argument mounts the current directory to the
working area of the container.  Additional directories may be mounted
by adding more volume arguments ``-v`` with host and container paths
separated by a colon.

The same docker image may be used to launch python, ipython, or a bash
shell by passing the command as an argument to ``docker run``:

.. code-block:: bash
   
   $ docker run -it --rm -v $PWD:/workdir -w /workdir fermipy/fermipy ipython
   $ docker run -it --rm -v $PWD:/workdir -w /workdir fermipy/fermipy python
   $ docker run -it --rm -v $PWD:/workdir -w /workdir fermipy/fermipy /bin/bash

By default interactive graphics will not be enabled.  The following
commands can be used to enable X11 forwarding for interactive graphics
on an OSX machine.  This requires you to have installed XQuartz 2.7.10
or later.  First enable remote connections by default and start the X
server:

.. code-block:: bash
                
   $ defaults write org.macosforge.xquartz.X11 nolisten_tcp -boolean false
   $ open -a XQuartz

Now check that the X server is running and listening on port 6000:

.. code-block:: bash
                
   $ lsof -i :6000

If you don't see X11 listening on port 6000 then try restarting XQuartz.

Once you have XQuartz configured you can enable forwarding by setting
DISPLAY environment variable to the IP address of the host machine:

.. code-block:: bash

   $ export HOST_IP=`ifconfig en0 | grep "inet " | cut -d " " -f2`
   $ xhost +local:
   $ docker run -it --rm -e DISPLAY=$HOST_IP:0 -v $PWD:/workdir -w /workdir fermipy ipython

Running at SLAC
---------------

This section provides specific installation instructions for running
in the SLAC computing environment.  First download and source the
``slacsetup.sh`` script:

.. code-block:: bash

   $ wget https://raw.githubusercontent.com/fermiPy/fermipy/master/slacsetup.sh -O slacsetup.sh
   $ source slacsetup.sh
   
To initialize the ST environment run the ``slacsetup`` function:

.. code-block:: bash

   $ slacsetup

This will setup your ``GLAST_EXT`` path and source the setup script
for one of the pre-built ST installations (the current default is
11-05-00).  To manually override the ST version you can provide the
release tag as an argument to ``slacsetup``:

.. code-block:: bash

   $ slacsetup XX-XX-XX

Because users don't have write access to the ST python installation
all pip commands that install or uninstall packages must be executed
with the ``--user`` flag.  After initializing the STs environment,
install fermipy with pip:

.. code-block:: bash

   $ pip install fermipy --user

This will install fermipy in ``$HOME/.local``.  You can verify that
the installation has succeeded by importing
`~fermipy.gtanalysis.GTAnalysis`:

.. code-block:: bash

   $ python
   Python 2.7.8 |Anaconda 2.1.0 (64-bit)| (default, Aug 21 2014, 18:22:21) 
   [GCC 4.4.7 20120313 (Red Hat 4.4.7-1)] on linux2
   Type "help", "copyright", "credits" or "license" for more information.
   Anaconda is brought to you by Continuum Analytics.
   Please check out: http://continuum.io/thanks and https://binstar.org
   >>> from fermipy.gtanalysis import GTAnalysis

Alternatively you can install with conda as follows:

.. code-block:: bash

   # Note that this first command may take a long time (> 10 m)
   $ conda create -n fermipy --clone=root
   $ conda config --append channels conda-forge
   $ source activate fermipy
   (fermipy) $ conda install fermipy
   
.. _upgrade:
   
Upgrading
---------

By default installing fermipy with ``pip`` or ``conda`` will get the latest tagged
released available on the `PyPi <https://pypi.python.org/pypi>`_
package respository.  You can check your currently installed version
of fermipy with ``pip show``:

.. code-block:: bash

   $ pip show fermipy

or ``conda info``:

.. code-block:: bash

   $ conda info fermipy
   
To upgrade your fermipy installation to the latest version run the pip
installation command with ``--upgrade --no-deps`` (remember to also
include the ``--user`` option if you're running at SLAC):
   
.. code-block:: bash
   
   $ pip install fermipy --upgrade --no-deps
   Collecting fermipy
   Installing collected packages: fermipy
     Found existing installation: fermipy 0.6.6
       Uninstalling fermipy-0.6.6:
         Successfully uninstalled fermipy-0.6.6
   Successfully installed fermipy-0.6.7

If you installed fermipy with ``conda`` the equivalent command is:

.. code-block:: bash

   $ conda update fermipy
   
   
.. _gitinstall:
   
Building from Source
--------------------

These instructions describe how to install fermipy from its git source
code repository using the ``setup.py`` script.  Installing from source
can be useful if you want to make your own modifications to the
fermipy source code or test features in an untagged commit.  Note that
non-expert users are recommended to install a tagged release of
fermipy following the :ref:`pipinstall` or :ref:`condainstall`
instructions above.

First clone the fermipy git repository and cd to the root directory of
the repository:

.. code-block:: bash

   $ git clone https://github.com/fermiPy/fermipy.git
   $ cd fermipy
   
To install the latest commit in the master branch run ``setup.py
install`` from the root directory:

.. code-block:: bash

   # Install the latest commit
   $ git checkout master
   $ python setup.py install --user 

A useful option if you are doing active code development is to install
your working copy of the package.  This will create an installation in
your python distribution that is linked to the copy of the code in
your local repository.  This allows you to run with any local
modifications without having to reinstall the package each time you
make a change.  To install your working copy of fermipy run with the
``develop`` argument:

.. code-block:: bash

   # Install a link to your source code installation
   $ python setup.py develop --user 

You can later remove the link to your working copy by running the same
command with the ``--uninstall`` flag:

.. code-block:: bash

   # Install a link to your source code installation
   $ python setup.py develop --user --uninstall
   
You also have the option of installing a previous release tag.  To see
the list of release tags run ``git tag``.  To install a specific
release tag, run ``git checkout`` with the tag name followed by
``setup.py install``:
   
.. code-block:: bash
   
   # Checkout a specific release tag
   $ git checkout X.X.X 
   $ python setup.py install --user 


   
Issues
------

If you get an error about importing matplotlib (specifically something
about the macosx backend) you might change your default backend to get
it working.  The `customizing matplotlib page
<http://matplotlib.org/users/customizing.html>`_ details the
instructions to modify your default matplotlibrc file (you can pick
GTK or WX as an alternative).  Specifically the ``TkAgg`` and
``macosx`` backends currently do not work on OSX if you upgrade
matplotlib to the version required by fermipy.  To get around this
issue you can switch to the ``Agg`` backend at runtime before
importing fermipy:

.. code-block:: bash

   >>> import matplotlib
   >>> matplotlib.use('Agg')

However note that this backend does not support interactive plotting.

If you are running OSX El Capitan or newer you may see errors like the following:

.. code-block:: bash
                
   dyld: Library not loaded

In this case you will need to disable the System Integrity Protections
(SIP).  See `here
<http://www.macworld.com/article/2986118/security/how-to-modify-system-integrity-protection-in-el-capitan.html>`_
for instructions on disabling SIP on your machine.

In some cases the setup.py script will fail to properly install the
fermipy package dependecies.  If installation fails you can try
running a forced upgrade of these packages with ``pip install --upgrade``:

.. code-block:: bash

   $ pip install --upgrade --user numpy matplotlib scipy astropy pyyaml healpy wcsaxes ipython jupyter
