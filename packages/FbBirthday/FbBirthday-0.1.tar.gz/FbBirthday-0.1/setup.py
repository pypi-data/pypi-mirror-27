from setuptools import setup,find_packages
from distutils.sysconfig import get_python_inc
from setuptools.command.develop import develop
from setuptools.command.install import install
import base64
import os
import subprocess
class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    # def run(self):
    #     # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
    #   username = raw_input("Enter your facebook username : ")
    #   password = raw_input("Enter your facebook password : ")
    #   wish_time = raw_input("wish_time : ")
    #   f = open('Fb_Birthday/Authentication.py', 'w' )
    #   f.write("Facebook_User_Id = "+'"'+str(base64.b64encode(username))+'"' +"\n")
    #   f.write("Facebook_Password = "+'"'+str(base64.b64encode(password))+'"' +"\n")
    #   f.write("wish_time = "+'"'+str(wish_time)+'"' +"\n")
    #   f.close()
    #   print "Updated Credentials ..."
    #   subprocess.call("python "+os.getcwd()+'/Fb_Birthday/scheduler.py',shell=True)

      
		

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    # print "Running program in install mode"
    # def run(self):
    #   username = raw_input("Enter your facebook username : ")
    #   password = raw_input("Enter your facebook password : ")
    #   wish_time = raw_input("wish_time : ")
    #   f = open('Fb_Birthday/Authentication.py', 'w' )
    #   f.write("Facebook_User_Id = "+'"'+str(base64.b64encode(username))+'"' +"\n")
    #   f.write("Facebook_Password = "+'"'+str(base64.b64encode(password))+'"' +"\n")
    #   f.write("wish_time = "+'"'+str(wish_time)+'"' +"\n")
    #   f.close()
    #   print "Updated Credentials ..."
    #   subprocess.call("python "+os.getcwd()+'/Fb_Birthday/scheduler.py',shell=True)
    #   install.run(self)

        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION



setup(name='FbBirthday',
      version='0.1',
      description='Schedule your Birthday wishes for your facebook friends and never Miss any birthdays',
      url='http://github.com/storborg/funniest',
      author='Ankit Mishra',
      author_email='ankitmishra@gmail.com',
      license='MIT',
      entry_points={
          'console_scripts': ['WishFb=FbBirthday.Notification:notify_event']
          },
      packages=['FbBirthday'],          
      install_requires=['python-crontab'],
      zip_safe=True)


