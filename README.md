# Generating QR codes in Python

A simple script which generates QR codes in Python. Currently works with numeric and alphanumeric modes, and supports up to and including Version 3. In time, I plan on adding Japanese support, as well as byte support, finally increasing the number of versions supported. The output of the script is in SVG format which is a scalable vector format, the code could easily be edited to export PNG images using PIL; this is something I might add at some point.

#### Usage:

    QR('H', 'http://www.paul-reed.co.uk')
  
First argument is the error detection level, accepted values are 'L', 'M', 'Q' and 'H'. Second argument is the text to be encoded. Running this script will generate an SVG file, which can be opened up in any browser, an example output is below:

 ![Input Image](https://github.com/PaulMakesStuff/Python-QR-Codes/blob/master/code.png)

#### Further Information:

[Thonkys QR Code Tutorial](https://www.thonky.com/qr-code-tutorial/) is a handy site which contains many answers to common questions when trying to build your own QR code.  
[Wikipedia's](https://en.m.wikipedia.org/wiki/QR_code]) entry on QR codes contains many useful images and some background information on QR codes.  
[ISO/IEC 18004:2015](https://www.iso.org/standard/62021.html) is the latest version of the international specification for QR codes. I used the 2005 version, I don't think there have been many changes between the two; and the 2005 version may be easier to get hold of.
