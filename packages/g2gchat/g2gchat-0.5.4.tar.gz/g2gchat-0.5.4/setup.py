from setuptools import setup

setup(
    name = 'g2gchat',
    version = '0.5.4',
    keywords=['g2gchat','chat','multichat'],
    author='Srikanth,Lalith',
    author_email='rs.chemikala@globaledgesoft.com',
    description='A Messenger for globalites with features including file transfer, backup of chat sessions and more...',
    packages = ['g2gchat'],
    scripts = ['g2gchat/g2gchat.py','g2gchat/config_parser.py'],
    #entry_points={   
    #    'console_scripts': [
    #        'g2gchat = g2gchat.py:main',
    #    ],
 
    #}
)
