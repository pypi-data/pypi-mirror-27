import os

from setuptools import setup


README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='gitlab_wrapper',
    version='0.0.2',
    py_modules=["gitlab_wrapper"],
    license='BSD License',
    description='',
    long_description=README,
    url='https://github.com/suguby/gitlab_wrapper',
    author='Shandrinov Vadim',
    author_email='suguby@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Education',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Topic :: Education',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='git gitlab skillbox',
    install_requires=[
        'python-gitlab==1.1.0'
    ]
)
