from setuptools import setup

setup(
    name = 'g2gchat',
    version = '0.5',
    author='Lalith,Srikanth',
    description='A Messenger for globalites with features including file transfer, backup of chat sessions and more...',
    packages = ['g2gchatclient'],
    #include_package_data=True,
    #package_data = {'g2gchatclient':['config_file.conf']},
    scripts = ['g2gchatclient/g2gchat.py','g2gchatclient/config_parser.py'],
#    entry_points={   
#        'console_scripts': [
#            'g2gchat=g2gchat.py:main',
#        ],
#    }
)
