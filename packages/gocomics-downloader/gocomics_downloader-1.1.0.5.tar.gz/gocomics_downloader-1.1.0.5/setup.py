from setuptools import setup


setup(name='gocomics_downloader',
    version='1.1.0.5',
    description='Conveniently download the comic images from GoComics comic files. ',
    url='https://github.com/PokestarFan/GoComics-Downloader',
    author='PokestarFan',
    author_email='pokestarfan@yahoo.com',
    license='MIT',
    packages=['gocomics_downloader'],
    install_requires=[
        'BeautifulSoup4',
        'requests',
        'lxml',
		'mainchecker'
    ],
    zip_safe=True)
