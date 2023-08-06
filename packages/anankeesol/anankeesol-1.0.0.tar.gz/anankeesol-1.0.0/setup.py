from setuptools import setup

setup(name='anankeesol',
      version='1.0.0',
      description='This sdk is used to connect Ananke IOT platform',
      url='',
      author='Effective Solutions LtD Sri Lanka',
      author_email='bathiyathennakoon@gmail.com',
      license='MIT',
      packages=['anankeesol'],
      install_requires=[
          'paho-mqtt',
      ],
      include_package_data=True,
      zip_safe=False)
