::

    pip install beatboxtestbed

``beatboxtestbed`` needs a number of other packages, all of them available through PyPi.
They should automatically be installed when using pip. Please read the installation
instructions of the ``boxmox`` package, as they contain instructions on how to install
the underlying box model BOXMOX.

``beatboxtestbed`` relies on 2 environmental variables to set the absolute path to work and
archive directories for beatbox experiments. You should add these directives to
your .bashrc, .profile (or similar, depending on your shell)::

   export BEATBOX_WORK_PATH="/path/to/you/beatbox/work/directory"
   export BEATBOX_ARCHIVE_PATH="/path/to/you/beatbox/archive/directory"
