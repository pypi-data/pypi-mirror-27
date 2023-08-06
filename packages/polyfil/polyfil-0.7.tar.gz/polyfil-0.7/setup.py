from setuptools import setup
setup(
  name = 'polyfil',
  packages = ['polyfil'], # this must be the same as the name above
  version = '0.7',
  description = 'A random test lib',
  author = 'laformarua',
  author_email = 'lcrua@utp.edu.co',
  url = 'https://github.com/laformarua/polyfil', # use the URL to the github repo
  download_url = 'https://github.com/laformarua/polyfil/archive/0.6.tar.gz', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
  install_requires=[
   'opencv-python'
  ]

)
