from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='tos=languagematcher',
      version='0.1',
      description='blank',
      long_description=readme(),
      url='blank',
      author='hiiwave',
      author_email='hiiwave@gmail.com',
      license='blank',
      packages=['tos_languagematcher'],
      install_requires=[
        'pandas',
      ],
      zip_safe=False)