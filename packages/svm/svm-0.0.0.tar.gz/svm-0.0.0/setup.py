from setuptools import setup

setup(name='svm',
      version='0.0.0',
      url='http://nedappjira001.int.asurion.com:8990/scm/gsa/retail_toolkit.git',
      description='Version manager for Apache Spark',
      author='Chris Kirby',
      author_email='kirbycm@gmail.com',
      license='MIT',
      packages=['svm'],
      install_requires=['requests'],
      zip_safe=False)