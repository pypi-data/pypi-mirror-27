from setuptools import setup,find_packages
import os
import subprocess

setup(name='BirthdayFb',
      version='0.2',
      description='Schedule your Birthday wishes for your facebook friends and never Miss any birthdays',
      url='https://github.com/ankitpyc/Autopy/tree/master/Facebook_BirthdayWish_/Fb_Birthday',
      author='Ankit Mishra',
      author_email='ankitmishra@gmail.com',
      license='MIT',	
      entry_points={
        'console_scripts': ['WishFb = FaceBir.Happy:main','FbSettings = FaceBir.UpdateCred:Update'],
          },         
      include_package_data=True,
      packages=find_packages(),  
      install_requires=[
      'python-crontab==2.2.8',
      'click==6.7',
      'colorama',
      'chromedriver-installer==0.0.6',
      'colorama==0.3.9',
      'notify2==0.3.1',
      'pygobject==3.20.0',
      'requests==2.18.4',
      'selenium==3.6.0',
      'subprocess32==3.2.7'
      ],
      zip_safe=True)














