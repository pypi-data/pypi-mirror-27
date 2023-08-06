from setuptools import setup
from setuptools.command.install import install
import os
import json
import optparse


class MyInstall(install):

    def run(self):
        install.run(self)
        print("Installing accelerator")
        print("\n\n\n\nInstalling accelerator!!!!\n\n\n\n")
        print("Started Running script")
        os.system("python lib/auto_script.py --role-name testmyRole --function-name testmyFunction --api-name testmyApi --s3-bucket-name acclmybucket --stage-name myStage")
        print("Script run successfully")


setup(name='wd-accl-17',
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
