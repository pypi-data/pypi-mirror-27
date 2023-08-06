from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='aligem',
      version='0.1',
      description='ALICE Grid Enviroment Manager',
      long_description=readme(),
      keywords='aligem ALICE CERN high energy physics',
      url='http://github.com/vpacik/aligem',
      author='Vojtech Pacik',
      author_email='vojtech.pacik@cern.ch',
      license='APACHE',
      packages=['aligem'],
      test_suite='nose.collector',
      tests_require=['nose', 'nose-cover3'],
      entry_points = {
          'console_scripts': ['aligem=aligem.command_line:main'],
      },
      include_package_data=True,
      zip_safe=False)
