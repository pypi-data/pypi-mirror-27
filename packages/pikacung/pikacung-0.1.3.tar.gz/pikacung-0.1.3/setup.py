from distutils.core import setup


setup(
    name = 'pikacung',
    packages = ['pikacung'],
    version = '0.1.3',
    description = 'Pika wrapper for simple publisher and consumer helper',
    author = 'M Gilang Januar',
    author_email = 'mgilangjanuar@gmail.com',
    url = 'https://github.com/mgilangjanuar/pikacung',
    download_url = 'https://github.com/mgilangjanuar/pikacung/archive/0.1.3.tar.gz',
    keywords = ['pika', 'message queue', 'rabbitmq'],
    classifiers = [],
    install_requires=['pika>=0.11.2']
)
