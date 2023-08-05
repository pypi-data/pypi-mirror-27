from setuptools import setup


def full_description():
    with open('README.md') as f:
        return f.read()


setup(name='getdone',
      version='0.1.2',
      description='An integrated ToDo list manager for your commandline',
      long_description=full_description(),
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Utilities'
      ],
      keywords='todo todolist todo manager getting things done gtd organizer tasks',
      author='Durga Swaroop',
      author_email='durgaswaroop@gmail.com',
      url='https://github.com/durgaswaroop/get-done',
      license='MIT',
      packages=['getdone'],
      install_requires=['playsound', 'PyQt5'],
      scripts=['bin/gd', 'bin/td'],
      zip_safe=False)
