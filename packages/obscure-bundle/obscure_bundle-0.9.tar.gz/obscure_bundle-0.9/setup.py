from distutils.core import setup
setup(
  name='obscure_bundle',
  packages=['obscure_bundle'],
  version='0.9',
  description='Integration of obscure api into applauncher',
  author='Alvaro Garcia Gomez',
  author_email='maxpowel@gmail.com',
  url='https://github.com/maxpowel/obscure_bundle',
  download_url='https://github.com/maxpowel/obscure_bundle/archive/master.zip',
  keywords=['api', 'rest', 'obscure', 'applauncher'],
  classifiers=['Topic :: Adaptive Technologies', 'Topic :: Software Development', 'Topic :: System', 'Topic :: Utilities'],
  install_requires=['applauncher', 'sqlalchemy_bundle', 'obscure_api']
)
