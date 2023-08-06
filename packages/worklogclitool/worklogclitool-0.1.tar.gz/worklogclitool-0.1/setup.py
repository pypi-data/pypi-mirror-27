from setuptools import setup

setup(
    name='worklogclitool',
    packages=['worklog'],
    version='0.1',
    description='A cli tool for loging work hours',
    author='Christoffer Berglund',
    author_email='christoffer.berglund.privat@gmail.com',
    keywords=['log','work','cli'],
    py_modules=['work'],
    install_requires=[
        'Click',
        'datetime',
    ],
    entry_points='''
        [console_scripts]
        work=work:work
    ''',
)
