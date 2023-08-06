from setuptools import setup

setup(
    name='seaborn_time_profile',
    version='0.0.1',
    description='SeabornTimingProfile collects, records, and reports timing'
                'data on code implementing a number of different execution'
                'strategies"',
    long_description='',
    author='Ben Christenson',
    author_email='Python@BenChristenson.com',
    url='https://github.com/SeabornGames/TimingProfile',
    install_requires=[],
    extras_require={
    },
    py_modules=['seaborn.time_profile'],
    license='MIT License',
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5'),
    entry_points='''
        [console_scripts]
        seaborn_table=seaborn.seaborn_table:main
    ''',
)