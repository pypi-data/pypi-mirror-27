from setuptools import setup

setup(
    name='seaborn_meta',
    version='0.0.1',
    description='SeabornMeta allows for simple changing'
				'of names between conventions, as well'
				'as auto-generating init files',
    long_description='',
    author='Ben Christenson',
    author_email='Python@BenChristenson.com',
    url='https://github.com/SeabornGames/meta',
    download_url='https://github.com/SeabornGames/meta'
                 '/tarball/download',
    keywords=['meta'],
    install_requires=[],
    extras_require={
    },
    py_modules=['seaborn.meta'],
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
        meta=seaborn.meta
    ''',
)
