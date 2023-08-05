from setuptools import setup, find_packages

__author__ = 'ikarishinjigao'

setup(
    name='zmz',
    version='0.1.1',
    description='Scripts for getting download links from www.zimuzu.tv.',
    author='ikarishinjigao',
    author_email='ikarishinjigao@gmail.com',
    url='https://github.com/ikarishinjigao/Zimuzu-Scraping',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords=['zmz', 'zimuzu', 'ZIMUZU'],
    license='MIT License',
    install_requires=[
        'click',
        'lxml',
        'prettytable',
        'bs4',
        'requests',
        'progressbar2',
    ],
    entry_points="""
        [console_scripts]
        zmz = zmz.__main__:main
    """,
)