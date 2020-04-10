from setuptools import setup
setup(name='covidapi',
      version='0.1.0',
      packages=['covidapi'],
      entry_points={
          'console_scripts': [
              'import_regions_jh = covidapi.import_regions_jh:main',
          ]
      },
      )
