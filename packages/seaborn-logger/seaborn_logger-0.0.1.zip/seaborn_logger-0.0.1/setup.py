from setuptools import setup

setup(
    name='seaborn_logger',
    version='0.0.1',
    description='SeabornLogger enables the streaming of the'
                'data relevant ot a program\'s to a logging'
				'file',
    long_description='',
    author='Ben Christenson',
    author_email='Python@BenChristenson.com',
    url='https://github.com/SeabornGames/Logger',
    download_url='https://github.com/SeabornGames/Logger'
                 '/tarball/download',
    keywords=['os'],
    install_requires=[],
    extras_require={
    },
    py_modules=['seaborn.logger'],
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
        logger=seaborn.logger
    ''',
)
