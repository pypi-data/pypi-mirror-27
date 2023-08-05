from setuptools import setup

setup(name='cflask',
      version='0.1',
      description='Simple versioning api built on flask',
      url='http://github.com/csm10495/cflask',
      author='csm10495',
      author_email='csm10495@gmail.com',
      license='MIT',
      packages=['cflask'],
      install_requires=["flask"],
      python_requires='>=2.7, !=3.0.*, !=3.1.*',
      zip_safe=True)