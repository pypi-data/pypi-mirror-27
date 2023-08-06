from distutils.core import setup

setup(
    name='parseMFT',
    version='0.2',
    author='Tim Doty',
    author_email='pip@baldskirkja.com',
    packages=['parsemft'],
    url='http://github.com/thoromyr/parseMFT',
    download_url='https://github.com/thoromyr/parseMFT/archive/v0.2.tar.gz',
    license='LICENSE.txt',
    description='Parse the $MFT from an NTFS filesystem.',
    long_description=open('README.md').read(),
    scripts=['parseMFT.py'],
    classifiers = [],
    keywords = ['mft', 'forensics'],
)
