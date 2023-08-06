from setuptools import setup

setup(name='ananke',
      version='0.1',
      description='This sdk is used to connect Ananke IOT platform',
      url='http://github.com/storborg/funniest',
      author='Effective Solutions LtD Sri Lanka',
      author_email='bathiyathennakoon@gmail.com',
      license='MIT',
      packages=['anankesdk'],
      install_requires=[
          'paho-mqtt',
      ],
      include_package_data=True,
      zip_safe=False)
