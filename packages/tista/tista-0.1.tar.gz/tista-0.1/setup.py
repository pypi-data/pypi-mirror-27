from distutils.core import setup
setup(
    name='tista',
    packages=['tista'],
    version='0.1',
    description='A (numba,cuda)-accelerated Time Series Technical Analysis library',
    author='Luc Alapini',
    author_email='synncox@gmail.com',
    license='MIT',
    url='https://gitlab.com/dioone/tista',
    # I'll explain this in a second
    download_url='https://gitlab.com/dioone/tista/repository/v0.1/archive.tar.gz',
    keywords=['technical analysis', 'python', 'time series',
              'indicators', 'numba', 'cuda'],
    classifiers=[],
)
