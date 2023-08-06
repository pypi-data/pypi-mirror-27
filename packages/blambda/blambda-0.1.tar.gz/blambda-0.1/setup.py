from setuptools import find_packages, setup

version = __import__('blambda').get_version()

setup(
    name='blambda',
    version=version,
    url='https://github.com/tcztzy/blambda',
    author='Tang Ziya',
    author_email='tcztzy@gmail.com',
    description='blambda is an implementation of Lisp in Python,',
    license='BSD',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Lisp',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Scheme',
        'Topic :: Software Development :: Interpreters',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
