from setuptools import setup

setup(
    name = 'mpesa',
    version = '0.0.1',
    description = 'a pip installable mpesa package',
    #url = '',
    author = 'Sheila Wambui Karienye',
    author_email = 'sheila.karienye@gmail.com',
    keywords = 'mpesa API module',
    packages = ['mpesa'],
    install_requires = ['pip', 'requests'],
    python_requires='>=2.6',
)