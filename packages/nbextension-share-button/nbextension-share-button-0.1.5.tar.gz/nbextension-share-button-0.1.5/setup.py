from setuptools import setup
setup(
  name = 'nbextension-share-button',
  version = '0.1.5',
  description = 'A Jupyter Notebook extension that adds a share button to the toolbar.',
  author = 'Globo.com',
  url = 'https://github.com/globocom/nbextension-share-button/',
  keywords = ['nbextension', 'share', 'notebook'],
  classifiers = [],
  packages = ['nbextension_share_button'],
  package_dir = {'nbextension_share_button': 'nbextension_share_button'},
  include_package_data = True
)
