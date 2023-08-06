#!/usr/bin/env python3

from subprocess import call

class Sudden:
	def __init__(self):
		pass
	def main(self):
		print('Main Hello World!')
	def update(self):
		call('sudo apt update', shell=True)
		call('sudo apt upgrade', shell=True)
	def install(self, tools):
		print('install {}'.format(tools))
		for tool in tools:
			print(tool)

if __name__ == '__main__':
    sudden = Sudden()
    sudden.main()