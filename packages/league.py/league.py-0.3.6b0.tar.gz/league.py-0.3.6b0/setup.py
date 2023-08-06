from setuptools import setup, find_packages
import re, os

try:
    import pypandoc

    description = pypandoc.convert("README.md", "rst")
except (IOError, ImportError):
    description = "An Asyncio friendly wrapper for Riot's League API"

on_rtd = os.getenv('READTHEDOCS') == 'True'

requirements = ["aiohttp>=2.2.3"]

if on_rtd:
    requirements.append('sphinxcontrib-napoleon')
    requirements.append('sphinxcontrib-asyncio')
    requirements.append("sphinx==1.5.6")

version = ''
with open('league/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('version is not set')

setup(
    name='league.py',
    version=version,
    packages=['league'],
    url='https://github.com/datmellow/League.py',
    python_requires='>=3.5',
    license='MIT',
    author='datmellow',
    author_email='lucas@iceteacity.com',
    install_requires=requirements,
    description=description,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]

)
