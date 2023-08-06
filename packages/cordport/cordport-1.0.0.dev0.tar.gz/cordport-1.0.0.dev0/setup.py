from setuptools import setup, find_packages
import cordport

setup(
    name='cordport',
    packages=find_packages(),
    version=cordport.__version__,
    description='Central Office Re-architecture as Datacenter(CORD) ovs debug tool',
    author=cordport.__author__,
    author_email='aweimeow.tw@gmail.com',
    license=cordport.__license__,
    entry_points={
        'console_scripts': [
            'port = cordport.__main__:main',
        ],
    },
    url = 'https://github.com/aweimeow/cordport',
    download_url = 'https://github.com/aweimeow/cordport/archive/1.0.tar.gz'
)

