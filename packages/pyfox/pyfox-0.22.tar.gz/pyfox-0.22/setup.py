from distutils.core import setup
setup(
    name = 'pyfox',
    packages = ['pyfox'],
    version = '0.22',
    description = 'Shell for foxtrot',
    author = 'Shubham Sharma',
    author_email = 'shubham.sha12@gmail.com',
    url = 'https://github.com/gabber12/pyfox',
    download_url = 'https://github.com/gabber12/pyfox/archive/0.22.tar.gz',
    classifiers = [],
    entry_points = {
                    'console_scripts': ['foxtrot=pyfox.commands:command'],
    },
    install_requires=[
        'requests',
        'click',
        'json-logic',
        'requests',
        'prompt_toolkit',
        'pygments'
    ]
)
