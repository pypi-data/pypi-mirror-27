BrainIAK Real-time cloud
========================

|Travis| |Appveyor| |License|

Getting started on client machine
---------------------------------

First, install Docker
(`Mac <https://store.docker.com/editions/community/docker-ce-desktop-mac>`__,
`Linux <https://store.docker.com/editions/community/docker-ce-server-ubuntu>`__,
`Windows <https://store.docker.com/editions/community/docker-ce-desktop-windows>`__).
Then, run

.. code:: bash

    # Sudo may be necessary
    docker pull brainiak/rtcloud
    docker run -it -p 8888:8888 brainiak/rtcloud
    ./bin/client/notebook

Getting started on server machine (Ubuntu 16.04)
------------------------------------------------

.. code:: bash

    git clone git@github.com:brainiak/rtcloud.git
    ./bin/server/install

Setting up cloud formation
--------------------------

.. code:: bash

    aws configure
    ./bin/cloud/launch

MATLAB
------

Make sure MATLAB\_R2017b is installed.

.. code:: bash

    export MATLAB_ROOT=[MATLAB_ROOT]

TODO
----

::

    echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p

-  `HPC on
   EC2 <https://d0.awsstatic.com/Projects/P4114756/deploy-elastic-hpc-cluster_project.pdf>`__
-  Code coverage
-  Codacy
-  Linting

Switching AWS regions
---------------------

-  May need to use custom
   `AMI <https://github.com/awslabs/cfncluster/blob/master/amis.txt>`__

Related work
------------

-  `Gadgetron <http://gadgetron.github.io>`__
-  Doron Friedman

BrainIAK Real-time cloud
========================

|Travis| |Appveyor| |License|

Getting started on client machine
---------------------------------

First, install Docker
(`Mac <https://store.docker.com/editions/community/docker-ce-desktop-mac>`__,
`Linux <https://store.docker.com/editions/community/docker-ce-server-ubuntu>`__,
`Windows <https://store.docker.com/editions/community/docker-ce-desktop-windows>`__).
Then, run

.. code:: bash

    # Sudo may be necessary
    docker pull brainiak/rtcloud
    docker run -it -p 8888:8888 brainiak/rtcloud
    ./bin/client/notebook

Getting started on server machine (Ubuntu 16.04)
------------------------------------------------

.. code:: bash

    git clone git@github.com:brainiak/rtcloud.git
    ./bin/server/install

Setting up cloud formation
--------------------------

.. code:: bash

    aws configure
    ./bin/cloud/launch

MATLAB
------

Make sure MATLAB\_R2017b is installed.

.. code:: bash

    export MATLAB_ROOT=[MATLAB_ROOT]

TODO
----

::

    echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p

-  `HPC on
   EC2 <https://d0.awsstatic.com/Projects/P4114756/deploy-elastic-hpc-cluster_project.pdf>`__
-  Code coverage
-  Codacy
-  Linting

Switching AWS regions
---------------------

-  May need to use custom
   `AMI <https://github.com/awslabs/cfncluster/blob/master/amis.txt>`__

Related work
------------

-  `Gadgetron <http://gadgetron.github.io>`__
-  Doron Friedman

.. |Travis| image:: https://travis-ci.org/brainiak/rtcloud.svg?branch=master
   :target: https://travis-ci.org/brainiak/rtcloud
.. |Appveyor| image:: https://ci.appveyor.com/api/projects/status/dldyb9jmwla03y0e/branch/master?svg=true
   :target: https://ci.appveyor.com/project/danielsuo/rtcloud/branch/master
.. |License| image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
   :target: https://opensource.org/licenses/Apache-2.0
