from setuptools import setup

setup(
    name = 'g2gchat',
    version = '0.5.1',
    keywords=['g2gchat','chat','multichat'],
    author='Srikanth,Lalith',
    author_email='rs.chemikala@globaledgesoft.com',
    description='A Messenger for globalites with features including file transfer, backup of chat sessions and more...',
    packages = ['g2gchat'],
    entry_points={   
        'console_scripts': [
            'g2gchat = g2gchat.__init__:main',
        ],
 
    }
)
