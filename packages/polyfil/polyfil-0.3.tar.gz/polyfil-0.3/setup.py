from setuptools import setup
setup(
  name = 'polyfil',
  packages = ['polyfil'], # this must be the same as the name above
  version = '0.3',
  description = 'A random test lib',
  author = 'laformarua',
  author_email = 'lcrua@utp.edu.co',
  url = 'https://github.com/laformarua/polyfill', # use the URL to the github repo
  download_url = 'https://github.com/laformarua/polyfill/archive/tag/0.2.tar.gz', # I'll explain this in a second
  keywords = ['testing', 'logging', 'example'], # arbitrary keywords
  classifiers = [],
  install_requires=[
   'opencv_python-3.4.0-cp37-cp37m-win_amd64.whl'
  ],
  dependency_links=['https://download.lfd.uci.edu/pythonlibs/gjr6o2id/opencv_python-3.4.0-cp37-cp37m-win_amd64.whl']

)
