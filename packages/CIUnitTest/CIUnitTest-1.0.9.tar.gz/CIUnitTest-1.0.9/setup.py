import setuptools

setuptools.setup(
    name='CIUnitTest',
    version='1.0.9',
    description='Provides test results of unittest in JSON format, in '
                'order to be able to use the results programmatically.',
    long_description=open('README.rst').read(),
    author='Arseni Mourzenko',
    author_email='arseni.mourzenko@pelicandd.com',
    url='http://go.pelicandd.com/n/python-ciunittest',
    license='MIT',
    keywords='unittest ci continuous-integration json',
    py_modules=['ciunittest']
)
