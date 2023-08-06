
SETUP_INFO = dict(
    name = 'date-detector',
    version = '1.0.1',
    author = 'Itai Shirav',
    author_email = 'itais@infinidat.com',

    url = 'https://github.com/ishirav/date-detector',
    license = 'BSD',
    description = """A Python module for scanning text and extracting dates from it""",
    long_description = """A Python module for scanning text and extracting dates from it""",

    # http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],

    install_requires = [
'setuptools',
'six'
],
    namespace_packages = [],

    package_dir = {'': 'src'},
    package_data = {'': []},
    include_package_data = True,
    zip_safe = False,

    entry_points = dict(
        console_scripts = [],
        gui_scripts = [],
        ),
)

if SETUP_INFO['url'] is None:
    _ = SETUP_INFO.pop('url')

def setup():
    from setuptools import setup as _setup
    from setuptools import find_packages
    SETUP_INFO['packages'] = find_packages('src')
    _setup(**SETUP_INFO)

if __name__ == '__main__':
    setup()

