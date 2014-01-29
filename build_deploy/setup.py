#!/usr/bin/env python
from distutils.core import setup



import os, sys

data_dirs=["src/templates","src/qrapp/static"]
data_files = []
for r in data_dirs:
    for (root, dirs, files) in os.walk(r):
        r = "/".join(root.split('/')[1:])
        print r, [root + "/" + f for f in files]
        data_files.append( ("/var/www/" + r, [root + "/" + f for f in files] ) ) 

# print data_files
data_files.append(("/etc/init.d/", ["holin.sh"] ))
data_files.append(("/etc/nginx/sites-available/", ["holin_nginx.conf"]))


#"""
setup(
    name='holin',
    version='0.0.1',
    author='Vasiliy G. Stavenko',
    author_email='stavenko@gmail.com',
    package_dir={'':'src'},
    packages = ["app", 'holin', 'image_gallery'],
    data_files = data_files,
    scripts = ["holin_init.sh"],
    #scripts=['bin/stowe-towels.py','bin/wash-towels.py'],
    #url='http://pypi.python.org/pypi/TowelStuff/',
    license='LICENSE.txt',
    description='Holin python app',
    long_description="Holin",
    
)
#"""
