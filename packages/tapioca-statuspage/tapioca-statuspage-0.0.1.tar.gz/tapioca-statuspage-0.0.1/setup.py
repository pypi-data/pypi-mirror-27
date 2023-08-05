import codecs
import os
import re

from setuptools import setup, find_packages, Command

here = os.path.abspath(os.path.dirname(__file__))

package = 'tapioca_statuspage'

version = '0.0.0'
changes = os.path.join(here, 'CHANGES.rst')
match = r'^#*\s*(?P<version>[0-9]+\.[0-9]+(\.[0-9]+)?)$'
with codecs.open(changes, encoding='utf-8') as changes:
    for line in changes:
        res = re.match(match, line)
        if res:
            version = res.group('version')
            break

# Get the long description
with codecs.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Get version
with codecs.open(os.path.join(here, 'CHANGES.rst'), encoding='utf-8') as f:
    changelog = f.read()

# Get requirements.txt
with codecs.open(os.path.join(here, 'requirements.txt')) as f:
    install_requires = f.readlines()


class VersionCommand(Command):
    description = 'print library version'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print(version)


setup(
    name='tapioca-statuspage',
    version=version,
    description='StausPage.io wrapper using tapioca',
    long_description=long_description,
    author='Olist Developers',
    author_email='developers@olist.com',
    url='https://github.com/olist/tapioca-statuspage',
    packages=find_packages(exclude=['docs', 'tests*']),
    package_dir={'tapioca_statuspage': 'tapioca_statuspage'},
    include_package_data=True,
    install_requires=install_requires,
    license='MIT',
    zip_safe=False,
    keywords='statuspage',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    cmdclass={
        'version': VersionCommand,
    }
)
