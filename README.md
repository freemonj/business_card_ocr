Business Card OCR
===============================

version number: 1.0.0
author: Freemon Johnson

Overview
--------

This application parses the results of the optical character recognition (OCR) component in order to extract the name, phone number, and email address from the processed business card image.

Methodology
-----------
	Memory:
		I process the input document one line at time as opposed to reading the entire document into memory.
	Runtime:
		My most compute expensive function is locating any part of the username in the line.
		The runtime at worst case O(n) + O(n) = 2 O(n) which equates to O(n).
		I could have used more built-ins i.e. translate() or regular expressions but I chose readability over any additional performance increases.
	Storage:
		I have a rotating time-stamped log for debugging purposes that creates a log folder and appends log level information into "business-card-ocr.log".


Installation / Usage
--------------------
This application requires python version 3.x. No external packages outside of
the python standard template library are necessary to run the **ocr** application.


**To build web based documentation:**

You need to install _sphinx_ package: [here](http://www.sphinx-doc.org/en/master/usage/installation.html)

Please edit the following files on your system after running: 
	
	$ sphinx-quickstart

**conf.py**:

	_sys.path.append(<where you *.rst files are located>)_
	
	I highly recommend changing the <html_theme> to "default" or "sphinx_rtd_theme"

_cd_ into **docs** and type 

    _$ sphinx-build -b html <docs directory path> <build/html directory path>_


My documentation is already located at **index.html** file in _build/html/_ directory.


Example
-------

_$  python ocr.py -f <input document path/filename>_ 
