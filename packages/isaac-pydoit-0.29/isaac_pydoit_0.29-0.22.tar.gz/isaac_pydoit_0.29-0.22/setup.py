from distutils.core import setup

setup(
    name='isaac_pydoit_0.29',
    packages=['doit'],  # ['isaac_pydoit_0.29'],
    version='0.22',
    description=('A simple fork of pydoit version' +
                 ' 0.29 that only considers a file changed only if' +
                 ' that file is newer than the one listed in the pydoit' +
                 ' database'
                 ),
    author='Isaac Rockafellow',
    author_email='isaac.rockafellow@gmail.com',
    url='https://github.com/irockafe/pydoit_0.29_fork',
    keywords=['pydoit', 'doit', 'make'],
    classifiers=['Programming Language :: Python :: 2.7',
                 ],
    install_requires=['cloudpickle', 'six', 'configparser'],
    entry_points={'console_scripts': [
                      'doit = doit.__main__:main'
                                ]
                  },
)
