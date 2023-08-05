from setuptools import setup

setup(name='cflask',
      version='0.1.1',
      description='Simple versioning api built on flask',
      url='http://github.com/csm10495/cflask',
      author='csm10495',
      author_email='csm10495@gmail.com',
      license='MIT',
      packages=['cflask'],
      install_requires=["flask"],
      python_requires='>=2.7, !=3.0.*, !=3.1.*',
      zip_safe=True,
    long_description="""\
Easy to use versioning API based on flask.
Check out https://github.com/csm10495/cflask for documentation.
""",
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],)