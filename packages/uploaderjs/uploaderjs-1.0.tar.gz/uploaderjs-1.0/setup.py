from setuptools import setup

setup(name='uploaderjs',
	  version='1.0',
	  description='Official from uploaderjs',
	  url='https://uploaderjs@bitbucket.org/uploaderjs/uploaderjs_pkpy.git',
	  author='Jure Bernava Prah',
	  author_email='webjure@gmail.com',
	  license='MIT',
	  packages=['uploaderjs'],
	  install_requires=[
		  'requests',
	  ],
	  zip_safe=False)
