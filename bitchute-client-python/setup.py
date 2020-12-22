import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='bitchute-client',
    version='0.1.0',
    author='L. Hex',
    author_email='lhex@protonmail.com',
    description='A Python client library for BitChute',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/l-hex/bitchute-client-python',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
