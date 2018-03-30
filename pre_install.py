import commands
import time
import os

def apt_install():
	cmds = ['python -m pip install twilio', 'python -m pip install requests', 'python -m pip install lxml', 
			'python -m pip install email', 'python -m pip install cssselect']

	for cmd in cmds:
		print os.system(cmd)

def install_pip():
	cmds = ['python get-pip.py']
	for cmd in cmds:
		print os.system(cmd)

def main():
	install_pip()
	apt_install()

main()