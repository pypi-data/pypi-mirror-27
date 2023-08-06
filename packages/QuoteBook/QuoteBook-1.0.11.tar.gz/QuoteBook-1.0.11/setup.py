from setuptools import find_packages, setup

try:
    import pypandoc
    longdescription = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    longdescription = 'A program used to store quotes.'

setup(
    name='QuoteBook',
    version='1.0.11',
    packages=find_packages(exclude=['*.design']),
    entry_points={
        'console_scripts': ['quotebook=QuoteBook.QuoteBook:main']
    },
    include_package_data=True,
    url='https://github.com/axelrechenberg/QuoteBook/',
    license='GPL-3.0',
    author='Axel Rechenberg',
    author_email='axelreche@gmail.com',
    description='A program used to store quotes.',
    long_description=longdescription,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: Polish',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Topic :: Other/Nonlisted Topic',
    ],
    keywords='quote storage pyqt5',
    python_requires='>=3.5',
    install_requires=[
                     "PyQt5",
                     "pyperclip",
                 ],
)
