from setuptools import setup, find_packages

import httpshare


long_description='''
TODO
'''

setup(
    name='httpshare',

    version='{major}.{minor}.{patch}'.format(**httpshare.version_info._asdict()),

    description='Q&D file transfer utility using an ephemeral HTTP service',
    long_description='',

    # The project's main homepage.
    url='https://github.com/lourkeur/httpshare',

    # Author details
    author='Louis Bettens',
    author_email='louis@bettens.info',

    # Choose your license
    license='zlib',

    classifiers=[
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: zlib/libpng License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',

        'Topic :: Communications :: File Sharing',
        'Topic :: Utilities',
    ],

    keywords='filetransfer',

    packages=['httpshare'],

    package_data={
        'httpshare': ['*.stpl', 'LICENSE.txt'],
    },
)
