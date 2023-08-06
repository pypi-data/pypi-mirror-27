import setuptools

setuptools.setup(
    name='pyanyzip',
    version='0.0.15',
    description='pyanyzip is a module to help with dealing with compressed files transparently',
    long_description='pyanyzip is a module to help with dealing with compressed files transparently',
    url='https://github.com/veltzer/pyanyzip',
    download_url='https://github.com/veltzer/pyanyzip',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    license='MIT',
    platforms=['python'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='python zip bz2 gzip',
    packages=setuptools.find_packages(),
    install_requires=[
        'pypipegzip',  # for opening zipped files
        'pylzma',  # for working with .xz files
        'typing',  # for types
    ],
)
