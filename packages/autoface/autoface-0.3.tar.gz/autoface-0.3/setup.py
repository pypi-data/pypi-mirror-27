from setuptools import setup
setup(name='autoface',
      version='0.3',
      maintainer='Ahmed Elmahy',
      maintainer_email='elmahy2005@gmail.com',
      license='LGPL',
      packages=['autoface'],
      install_requires=['selenium','python-dateutil'],
      scripts=['bin/autoface-test'],
      dependency_links=['https://github.com/mobolic/facebook-sdk.git#egg=facebook-sdk']
      )
