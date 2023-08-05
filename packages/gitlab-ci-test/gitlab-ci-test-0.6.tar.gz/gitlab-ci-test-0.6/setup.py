from setuptools import setup

setup(
    name='gitlab-ci-test',    # This is the name of your PyPI-package.
    version='0.6',                          # Update the version number for new releases
    scripts=['gitlab_ci.bat', 'helloworld.py'],                 # The name of your scipt, and also the command you'll be using for calling it
	#url='https://pypi.python.org/pypi/gitlab-ci-test/',
	author="Artsiom Kushniarou",
	author_email="kushnerovartem@gmail.com"
)
