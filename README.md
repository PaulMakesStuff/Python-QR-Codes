# Generating QR codes in Python

A simple script which generates QR codes in Python. Currently works with numeric and alphanumeric modes, and supports up to and including Version 3. In time, I plan on adding Japanese support, as well as byte support, finally increasing the number of versions supported. The output of the script is in SVG format which is a scalable vector format, the code could easily be edited to export PNG images using PIL; this is something I might add at some point.

#### Usage

  QR('H', 'http://www.paul-reed.co.uk')
  
First argument is the error detection level, accepted values are 'L', 'M', 'Q' and 'H'. Second argument is the text to be encoded. Running this script will generate an SVG file, which can be opened up in any browser, an example output is below:

 ![Input Image](https://github.com/PaulMakesStuff/Python-QR-Codes/blob/master/code.png)
