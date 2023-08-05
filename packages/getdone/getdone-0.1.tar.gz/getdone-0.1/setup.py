from setuptools import setup

setup(name='getdone',
      version='0.1',
      description='An integrated ToDo list manager for your commandline',
      author='Durga Swaroop',
      author_email='durgaswaroop@gmail.com',
      license='MIT',
      packages=['getdone'],
      install_requires=['playsound', 'PyQt5'],
      scripts=['bin/gd', 'bin/td'],
      zip_safe=False)
