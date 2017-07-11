from setuptools import setup

setup(name='HandlingPOSTFlask', version='1.0',
      description='WPANEL is GUI tools helps to run the plybooks',
      author='pavan', author_email='mvvpavan@gmail.com',
      url='http://www.runnable.com/',

      #  Uncomment one or more lines below in the install_requires section
      #  for the specific client drivers/modules your application needs.
      install_requires=['flask', 'requests','gitpython',
                        #  'MySQL-python',
                        #  'pymongo',
                        #  'psycopg2',
      ],
     )
