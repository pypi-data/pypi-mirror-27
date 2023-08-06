from setuptools import setup, find_packages

setup(
    name = 'orthanc_launcher',
    packages = find_packages(),
    version='0.1.3',  # always keep all zeroes version, it's updated by the CI script
    setup_requires=['twine', 'wheel'],
    description = 'Helpers class to launch Orthanc servers on Windows/Linux/OSX.',
    author = 'Alain Mazy',
    author_email = 'am@osimis.io',
    url = 'https://bitbucket.org/osimis/python-orthanc-launcher',
    keywords = ['orthanc', 'launcher'],
    classifiers = [],
    install_requires = [
        'requests==2.13.0',
        'docker==2.0.1',
        'osimis_timer==0.2.3',
        'osimis_logging==0.1.0',
        'osimis_cmd_helpers==0.1.1',
        'osimis_file_helpers==0.1.0'
    ],
)
