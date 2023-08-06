from setuptools import setup, find_packages

from os import path

here = path.abspath(path.dirname(__file__))

setup(name='anadaptor',
      version='0.0.1',
      description='No path vars no problem.',
      #packages=['anadaptor'],
      entry_points={'console_scripts': ['anadaptor=anadaptor.main:main'],},
	  url='https://github.com/draperjames/anadaptor',
	  author='James Draper',
	  author_email='james.draper@duke.edu',
	  license='MIT',
	  packages=find_packages(),
	  classifiers=[
	  'Development Status :: 3 - Alpha',
	  'Intended Audience :: Developers',
	  'Topic :: Software Development :: Build Tools',
	  'License :: OSI Approved :: MIT License',
	  'Programming Language :: Python :: 3.5',
	  'Programming Language :: Python :: 3.6',
	  ],
    keywords='anadaptor',
	)
