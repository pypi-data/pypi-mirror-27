import os.path
import sys

from setuptools import setup, find_packages

full_version = ''

root_dir = os.path.abspath(os.path.dirname(__file__))

readme_file = os.path.join(root_dir, 'README.rst')
with open(readme_file, encoding='utf-8') as f:
    long_description = f.read()

version_module = os.path.join(root_dir, 'src', 'mattermostdriver', 'version.py')
with open(version_module, encoding='utf-8') as f:
    exec(f.read())

py_version = sys.version_info[:2]

if py_version < (3, 4):
    raise Exception("python-mattermost-driver requires Python >= 3.4.")

setup(
    name='mattermostdriver-asyncio',
    version=full_version,
    description='An asyncio Python Mattermost Driver',
    long_description=long_description,
    author='Nate Mara',
    author_email='nate.mara@kroger.com',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'aiohttp>=2.3.4',
        'async-timeout>=1.4.0',
        'aiodns>=1.1.1',
        'cchardet>=2.1.1',
        'websockets>=3.2',
    ],
)
