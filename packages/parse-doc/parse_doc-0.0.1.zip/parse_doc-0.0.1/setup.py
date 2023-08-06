from setuptools import setup

setup(
    name='parse_doc',
    version='0.0.1',
    description='SeabornCallingFunction reads metadata regarding '
                'functions applied to its member functions."',
    long_description='',
    author='Ben Christenson',
    author_email='Python@BenChristenson.com',
    url='https://github.com/christensonb/SeabornCallingFunction',
    download_url='https://github.com/christensonb/SeabornCallingFunction'
                 '/tarball/download',
    keywords=['metadata'],
    install_requires=[],
    extras_require={
    },
    py_modules=['seaborn.calling_function'],
    license='MIT License',
    packages=['seaborn'],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6'],
    entry_points='''
        [console_scripts]
        calling_function=seaborn.calling_function
    ''',
)
