from setuptools import setup

setup(
	name = 'plimoTeste',
	version = '0.2',
	description = 'Um projeto estupido usando dependencias',
	url = 'https://github.com/plimo263',
	author = 'Marcos Felipe da Silva Jardim',
	author_email = 'plimo263@gmail.com',
	license = 'MIT',
	classifiers = [
		# Informa em qual versao do python meu projeto trabalha
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.2',
    	'Programming Language :: Python :: 3.3',
    	'Programming Language :: Python :: 3.4',
    	'Programming Language :: Python :: 3.5',
    	'Programming Language :: Python :: 3.6',
	],
	pyton_requires = '>=3',
	install_requires = ['requests', 'pymysql'],
	py_modules = ['pteste'],
);
