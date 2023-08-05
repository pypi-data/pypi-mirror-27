from distutils.core import setup
setup(
  name = 'digIndicators',
  packages = ['digIndicators'],
  version = '1.1.8',
  description = 'Domain: indicator',
  author = 'Jiayuan Ding',
  author_email = 'jiayuand@usc.edu',
  url = 'https://github.com/usc-isi-i2/dig_indicators', #github 
  download_url = 'https://github.com/usc-isi-i2/dig_indicators', # I'll explain this in a second
  keywords = ['domain', 'dig'], # arbitrary keywords
  classifiers = [],
  install_requires=['fasttext>=0.8.3',
                    'numpy>=1.13.2',
                    'scikit-learn>=0.19.0',
                    'scipy>=0.19.1',
                    'cython>=0.27.3',
                    'requests>=2.18.0']
)
