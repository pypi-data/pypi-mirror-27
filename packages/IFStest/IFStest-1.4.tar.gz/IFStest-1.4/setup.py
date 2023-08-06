'''
from setuptools import setup,find_packages

setup(
   name='IFS',
   version='1.0',
   packages=find_packages(),
   description='IFS module',
   author='Humain Lab',
   author_email='test@hotmail.com',
   #packages=['IFS'],  #same as name
   install_requires=['numpy'], #external packages as dependencies

)

        package_dir = {
            'IFS': 'IFS',
            'IFS.Measures': 'IFS/Measures'},
        packages=['IFS', 'IFS.Measures'],
'''


from setuptools import setup,find_packages
'''from setuptool import util '''
if __name__ == "__main__":


    setup(
        name='IFStest',
		version = '1.4',
		packages=find_packages(),
		description='IFS module',
		author='Humain Lab',
		author_email='test@hotmail.com',
		install_requires = ['numpy'],
		url = 'http://humain-lab.teiemt.gr/?page_id=2366',
		licence='MIT',
		classifiers=[
			'Development Status :: 4 - Beta',
			'License :: OSI Approved :: Python Software Foundation License',
			'Programming Language :: Python',
		],
		include_package_data=True,
		package_data={
			'data':
				['Docs/Documentation',
				 'Docs/Realease Notes',
				 ],
		}
    )
