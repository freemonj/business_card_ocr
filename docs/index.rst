.. Business Card OCR documentation master file, created by
   sphinx-quickstart on Sat Mar 23 01:53:44 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Business Card OCR's documentation!
=============================================

Overview
--------

This application parses the results of the optical character recognition (OCR) component in order to extract the name, phone number, and email address from the processed business card image.



Installation / Usage
--------------------
This application requires python version 3.x. No external packages outside of
the pythone standard template library are necessary.


**To build web based docs:**

You need to install sphinx package: http://www.sphinx-doc.org/en/master/usage/installation.html

*cd* into **docs** and type 
    *$ make html*

Then have your browser open the **index.html** file in *build/html/* directory


Example
-------

*$  python -f <input document path/filename>*

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
