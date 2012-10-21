import os
import errno

def mkdir_p(path):
	"""emulate unix `mkdir -p` command"""
	try:
		os.makedirs(path)
	except OSError, e:
		if exc.errno == errno.EEXIST:
			pass
		else:
			raise

def touch(name):
	"""emulate unix `touch` command"""
	with file(name, 'a'):
		os.utime(name, None)


