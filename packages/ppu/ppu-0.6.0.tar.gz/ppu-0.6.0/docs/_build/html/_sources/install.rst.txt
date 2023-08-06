Installation using pip
======================

System-wide
-----------

::

    sudo pip install --install-option='-O2' ppu

User mode
---------

::

    pip install --user --install-option='-O2' ppu

Installation from sources
=========================

To install the library from sources system-wide run run the following
command:

::

    sudo python setup.py install -O2

If you don't want to install it system-wide you can install it in your
home directory; run run the following command:

::

    python setup.py install --user -O2

Option '--user' installs scripts into $HOME/.local/bin;
add the directory to your $PATH or move the script to a directory in your
$PATH.
