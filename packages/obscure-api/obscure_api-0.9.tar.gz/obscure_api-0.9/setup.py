from distutils.core import setup
setup(
  name='obscure_api',
  packages=['obscure_api'],
  version='0.9',
  description='Library to make obscured apis',
  author='Alvaro Garcia Gomez',
  author_email='maxpowel@gmail.com',
  url='https://github.com/maxpowel/obscure_api',
  download_url='https://github.com/maxpowel/obscure_api/archive/master.zip',
  keywords=['api', 'rest', 'obscure'],
  classifiers=['Topic :: Adaptive Technologies', 'Topic :: Software Development', 'Topic :: System', 'Topic :: Utilities'],
  install_requires=['Werkzeug', 'anytree', 'python-jose', 'pycrypto']
)
