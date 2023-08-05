import setuptools

"""
The documentation can be found at:
http://setuptools.readthedocs.io/en/latest/setuptools.html
"""
setuptools.setup(
    # the first three fields are a must according to the documentation
    name='pydmt',
    version='0.0.51',
    packages=[
        'pydmt',
        'pydmt.api',
        'pydmt.builders',
        'pydmt.core',
        'pydmt.features',
        'pydmt.scripts',
        'pydmt.utils',
    ],
    # from here all is optional
    description='python dependency management tool',
    long_description='python dependency management tool',
    author='Mark Veltzer',
    author_email='mark.veltzer@gmail.com',
    maintainer='Mark Veltzer',
    maintainer_email='mark.veltzer@gmail.com',
    keywords=[
        'pydmt',
        'cons',
        'scons',
        'software construction',
        'make',
        'maven',
        'mvn',
    ],
    url='https://veltzer.github.io/pydmt',
    download_url='https://github.com/veltzer/pydmt',
    license='MIT',
    platforms=[
        'python3',
    ],
    install_requires=[
        'click',
        'pyfakeuse',
        'pylogconf',
        'mako',
        'Sphinx',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Utilities',
    ],
    data_files=[
    ],
    entry_points={'console_scripts': [
        'pydmt_build=pydmt.scripts.build:main',
    ]},
    python_requires='>=3',
)
