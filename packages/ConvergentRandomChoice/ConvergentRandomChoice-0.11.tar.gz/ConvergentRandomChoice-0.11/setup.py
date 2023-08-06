from distutils.core import setup
setup(
  name = 'ConvergentRandomChoice',
  packages = ['ConvergentRandomChoice'],
  version = '0.11',
  description = 'Convergent Random Walk Choice lib.',
  author = 'Joshua Gang',
  author_email = 'joshua.gang@gmail.com',
  url = 'https://github.com/MrTyton/ConvergentRandomChoice', 
  download_url = 'https://github.com/MrTyton/ConvergentRandomChoice/archive/0.11.tar.gz',
  liscence = 'GNU',
  keywords = ['random walk', 'numpy',], 
  install_requires=['numpy'],
  python_requires='>=3.6',
  classifiers = ['Programming Language :: Python :: 3.6'],
)
