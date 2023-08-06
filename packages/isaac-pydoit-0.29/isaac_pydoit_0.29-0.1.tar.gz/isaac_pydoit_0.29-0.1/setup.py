from distutils.core import setup

setup(
    name='isaac_pydoit_0.29',
    packages= ['isaac_pydoit'],  # ['isaac_pydoit_0.29'],
    version='0.1',
    description=('A simple fork of pydoit version' +
                 ' 0.29 that only considers a file changed only if' +
                 ' that file is newer than the one listed in the pydoit' +
                 ' database'
                 ),
    author='Isaac Rockafellow',
    author_email='isaac.rockafellow@gmail.com',
    url='https://github.com/irockafe/pydoit_0.29_fork',
    download_url=('https://github.com/irockafe/' +
                  'pydoit_0.29_fork/archive/0.1.tar.gz'
                  ),
    keywords=['pydoit', 'doit', 'make'],
    classifiers=['Programming Language :: Python :: 2.7',
                 ],
    entry_points={'console_scripts': [
                      'doit = doit.__main__:main'
                                ]
                  },
)
