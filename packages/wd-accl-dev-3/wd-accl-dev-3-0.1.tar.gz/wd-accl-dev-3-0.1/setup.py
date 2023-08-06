from setuptools import setup
from setuptools.command.install import install
import os
import json
import optparse


class MyInstall(install):

    def run(self):
        install.run(self)
        
        print(os.environ['ACCLKEY'])
        print("python lib/auto_script.py"+os.environ['ACCLKEY']+" --role-name 11")
        
        print("Installing accelerator")
        print("\n\n\n\nInstalling accelerator!!!!\n\n\n\n")
        print("Started Running script")
        os.system("python lib/auto_script.py --role-name "+os.environ['ACCLKEY']+" --function-name "+os.environ['ACCLKEY']+" --api-name "+os.environ['ACCLKEY']+" --s3-bucket-name "+os.environ['ACCLKEY']+" --stage-name myStage")
        print("Script run successfully")


setup(name='wd-accl-dev-3',
      version='0.1',
      description='Accelerator V3',
      url='http://whirldatascience.com',
      author='Whirldata',
      author_email='flyingcircus@example.com',
      license='MIT',
      cmdclass={'install': MyInstall},
      include_package_data = True,
      data_files=[("lib",['lib/lambda.json'])],
      packages=['lib'],
      zip_safe=False)
