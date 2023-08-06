from setuptools import setup, find_packages

setup(name='NxMake',
      version='1.0.0a1',
      description='Customizable build system',
      url='https://github.com/maheshkhanwalkar/NxMake',
      author='Mahesh Khanwalkar',
      author_email='maheshkhanwalkar@gmail.com',
      license='Apache v2',
      classifiers=['Development Status :: 3 - Alpha', 'Intended Audience :: Developers',
                   'Topic :: Software Development :: Build Tools', 'Programming Language :: Python :: 3.5'],
      keywords='development',
      packages=find_packages(exclude=['test', 'venv']),
      python_requires='>=3.5')
