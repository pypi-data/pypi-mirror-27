*************************
PyNmcli
*************************

.. image:: https://travis-ci.org/fbarresi/PyNmcli.svg?branch=master
    :alt: Travis CI build status

Simple python interface to Network Manager CLI

PyNmcli provides a easy to use python (2.7+ or 3+) interface to Network Manager CLI.
Official documentation of nmcli under: https://developer.gnome.org/NetworkManager/stable/nmcli.html

Dependencies
========

This project has no dependencies and works with python 2.7+ (python 3 as well)

This package directly uses ``Network-Manager``.

Your can install it running the following command from shell: ::

sudo apt-get install network-manager

Installation
========

You may install this package in two ways:

- Compile from code (requires setuptools) ::

    pip install setuptools
    git clone https://github.com/fbarresi/PyNmcli.git
    cd PyNmcli
    python setup.py install

- Pypi ::

    pip install pynmcli

Usage
========

Just import the package::

    from pynmcli import NetworkManager

and call Network Manager function just like: ::

    result = NetworkManager.NetworkManager('--version').execute()

or ::

    result = NetworkManager.NetworkManager.Device().wifi('list').execute()

Contribute
========

Whould you like to contribute this project? YES, PLEASE!

Just fork this repository and submit your pull request.

Change log
========

- Version 1.0.1 - First release
