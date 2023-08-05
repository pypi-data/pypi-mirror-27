from setuptools import setup

setup(name='kurator',
      version='0.1',
      description='Command line tool to help with media dumps',
      keywords=['media','dump','file','transfer','exif','photos','images','duplicate','rename'],
      url='http://github.com/saltycatfish/kurator',
      download_url = 'https://github.com/saltycatfish/kurator/archive/0.1.tar.gz',
      author='SaltyCatFish',
      author_email='ryan@saltycatfish.com',
      license='MIT',
      packages=['kurator'],
      install_requires=[
        'click==6.7',
        'ExifRead==2.1.2',
        'olefile==0.44',
        'Pillow==4.2.1',
        'psycopg2==2.7.3.1',
        'pyasn1==0.3.6',
        'pyasn1-modules==0.1.4',
        'rsa==3.4.2',
        'six==1.11.0',
        'uritemplate==3.0.0'
      ],
      entry_points = {
        'console_scripts': ['kurator=kurator.command_line:main'],
      },
      zip_safe=False)
