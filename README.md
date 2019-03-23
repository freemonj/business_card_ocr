Business Card OCR
===============================

version number: 1.0.0
author: Freemon Johnson

Overview
--------

This application parses the results of the optical character recognition (OCR) component in order to extract the name, phone number, and email address from the processed business card image.



Installation / Usage
--------------------
This application requires python version 3.x. No external packages outside of
the pythone standard template library are necessary.


**To build web based docs:**

You need to install sphinx package: [here](http://www.sphinx-doc.org/en/master/usage/installation.html)

_cd_ into **docs** and type 
    _$ sphinx-build -b html <docs directory path> <build/html directory path>_

Then have your browser open the **index.html** file in _build/html/_ directory


Example
-------

_$  python -f <input document path/filename>_ 
