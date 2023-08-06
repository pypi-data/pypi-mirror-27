from distutils.core import setup
setup(
  name = 'hko_weather',
  packages = ['hko_weather'], # this must be the same as the name above
  scripts=['bin/hko_weather'],
  version = '0.1',
  description = 'A HKO Weather Library',
  classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.5',
  ],
  author = 'Nick Shek',
  author_email = 'alfshek@hotmail.com',
  url = 'https://github.com/nickshek/hko_weather', # use the URL to the github repo
  download_url = 'https://github.com/nickshek/hko_weather/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['HKO','Weather'], # arbitrary keywords
  license='MIT',
  install_requires=[
      'requests(>=2.18)',
      'inscriptis(>=0.0.3.2)',
      'lxml(>=4.1.1)',
      'cement(>=2.10.2)',
  ],
  include_package_data=True,
)
