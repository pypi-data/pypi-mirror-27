"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages

setup(
    name='ragames',
    version='0.1.0',
    description='List OpenRA games',
    author='bullE',
    author_email='bulle.ragl@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='openra',
    packages=find_packages(),
    install_requires=['colorama'],

    entry_points={
        'console_scripts': [
            'ragames=ragames.ragames:main',
        ],
    },
)


