from setuptools import setup

setup(
	name='recall-cmds',
	packages=['recall'],
	version='0.0.5',
	url='https://github.com/mavcook/recall',
	author='Maverick Cook',
	author_email='mav@mavcook.com',
	description='A tool to view and edit templated commands that you forget.',


	entry_points={
		'console_scripts': [
			'recall=recall.recall:main',
		],
	},


	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3.3',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
	],

	python_requires='>=3',
)
