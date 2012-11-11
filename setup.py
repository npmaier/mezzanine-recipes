from distutils.core import setup
import os
from mezzanine_recipes import __version__

setup(
    name='mezzanine-recipes',
    version=__version__,
    author='Thomas Jetzinger',
    author_email='thomas@jetzinger.com',
    description='Recipe pages for the Mezzanine CMS',
    url='https://github.com/tjetzinger/mezzanine-recipes',
    packages=['.'.join(i[0].split(os.sep))
              for i in os.walk('mezzanine_events')
              if '__init__.py' in i[2]
    ],
    install_requires=[
        'Mezzanine==1.2.4',
        'django-tastypie==0.9.11',
        'uuid==1.30',
    ],
)
