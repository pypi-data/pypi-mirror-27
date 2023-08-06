#!/usr/bin/env python

from setuptools import setup, find_packages

from aiongrok import version


def long_description():
    with open('README.rst') as f:
        return f.read()


download_url = 'https://github.com/resurtm/aiongrok/archive/v{}.tar.gz'
download_url = download_url.format(version)

setup(
    name='aiongrok',
    version=version,
    description='aiohttp ngrok API library',
    long_description=long_description(),
    url='https://github.com/resurtm/aiongrok',
    download_url=download_url,
    author='resurtm',
    author_email='resurtm@gmail.com',
    license='MIT',
    classifiers=[
        # 'Development Status :: 1 - Planning',
        'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=['aiohttp'],
    platforms='any',
)
