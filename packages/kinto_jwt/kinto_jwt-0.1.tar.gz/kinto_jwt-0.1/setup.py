from distutils.core import setup
setup(
  name = 'kinto_jwt',
  packages = ['kinto_jwt'], # this must be the same as the name above
  version = '0.1',
  description = 'Kinto JWT (Json Web Tokens) authentication policy',
  author = 'Danny Meier',
  author_email = 'danny@danflash.com',
  url = 'https://github.com/dannyyy/kinto_jwt', # use the URL to the github repo
  download_url = 'https://github.com/dannyyy/kinto_jwt/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['kinto', 'jwt', 'authentication', 'policy', 'pyramid', 'pyjwt'], # arbitrary keywords
  classifiers = [],
)