from setuptools import setup, find_packages
from ethermine_monitor import __version__ as version


setup(
    name='ethermine-monitor',
    version=version,
    description=('Monitor ethermine workers'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='bot monitor crypto cryptocurrency ethermine',
    author='Jon Robison',
    author_email='narfman0@gmail.com',
    url='https://github.com/narfman0/ethermine-monitor',
    license='LICENSE',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=['requests', 'flask'],
    test_suite='tests',
)
