from setuptools import setup

setup(
    name='dbcl',
    version='0.1.2',
    description='A database command line interface that is engine-agnostic.',
    author='Kris Steinhoff',
    url='https://github.com/ksofa2/dbcl',
    download_url='https://github.com/ksofa2/dbcl/archive/0.1.2.tar.gz',

    packages=['dbcl'],
    entry_points={
        'console_scripts': ['dbcl=dbcl.command_line:command_loop'],
    },
    include_package_data=True,
    install_requires=[
        'sqlalchemy',
        'prompt_toolkit',
        'pygments',
        'terminaltables',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
        'pytest-mock',
        'coverage',
    ],
)
