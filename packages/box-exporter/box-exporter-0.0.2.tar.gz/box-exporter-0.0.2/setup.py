from setuptools import setup

requires = ['docopt', 'records', 'boxsdk[jwt]', 'psycopg2']

setup(
    name='box-exporter',
    version='0.0.2',
    description='A utility that allows you to export data from a database to a '
                'folder on box',
    long_description='',
    license='AGPLv3',
    author='m1yag1',
    author_email='me@mikefromit.com',
    py_modules=['boxexporter'],
    install_requires=requires,
    zip_safe=False,
    entry_points={
        'console_scripts': ['boxex=boxexporter:cli']
    },
    classifiers=[],
)
