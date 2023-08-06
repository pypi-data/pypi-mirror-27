from distutils.core import setup
setup(
  name = 'chipledclient',
  packages = ['client'], # this must be the same as the name above
  version = '0.2',
  description = 'Client library for chip LED controller (see https://github.com/oxygen0211/chip-led-controller)',
  author = 'Julian Engelhardt',
  author_email = 'jengelhardt211@gmail.com',
  url = 'https://github.com/oxygen0211/chip-led-client', # use the URL to the github repo
  download_url = 'https://github.com/oxygen0211/chip-led-client/archive/0.1.tar.gz', # I'll explain this in a second
  keywords = ['LED', 'C.H.I.P.', 'NextThing.co', 'GPIO'], # arbitrary keywords
  classifiers = [],
)
