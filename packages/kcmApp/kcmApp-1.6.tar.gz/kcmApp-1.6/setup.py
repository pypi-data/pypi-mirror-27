from distutils.core import setup

setup(
    name = 'kcmApp',
    packages = ['kcmApp'],
    version = '1.6',
    description = 'A django App for kcm',
    author = 'davidtnfsh',
    author_email = 'davidtnfsh@gmail.com',
    url = 'https://github.com/udicatnchu/kcmApp',
    download_url = 'https://github.com/udicatnchu/kcmApp/archive/v1.6.tar.gz',
    keywords = ['kcmApp'],
    classifiers = [],
    license='GPL3.0',
    install_requires=[
    ],
    dependency_links=[
        'git+git://github.com/UDICatNCHU/KCM.git@master#egg=KCM',
    ],
    zip_safe=True,
)
