#import subprocess
import multiprocessing
import sys
import os
import time
import getpass
import textwrap
import argparse
import tempfile
import atexit
from .ssh import worker
from .args import args
from .rcexceptions import SSHKeyNotLoaded

debug = 1

def clean_file(filename):
    """Cleanup pass file on exit."""
    os.unlink(filename)

def main():

	user = args.user or getpass.getuser()
        if args.password:
            user_password = getpass.getpass()
            pass_file = tempfile.NamedTemporaryFile(delete=False)
            atexit.register(clean_file, pass_file.name)
            pass_file.write("echo %s" % user_password)
            os.chmod(pass_file.name, 0500)
            os.environ['DISPLAY'] = "dummy"
            os.environ['SSH_ASKPASS'] = pass_file.name
            pass_file.close()
        else:
            user_password = None

	debug = args.debug

	#try:
	print "Running command \"%s\" on hosts in file \"%s\"" % (args.command[0], args.file[0].name)
	#except:
		#print "Usage: %s <filename> <command>" % (sys.argv[0])
		#sys.exit(1)

	if args.sudo:
		password = getpass.getpass("sudo password: ")
		command = "echo '%s' | sudo -S %s" % (password, args.command[0])
	else:
		command = args.command[0]


	#f = open(sys.argv[1], "r")
	#hosts = f.read()
	#f.close()

	hosts = args.file[0].read()
	args.file[0].close()

	pool = multiprocessing.Pool(processes=100)

	results = []
        worker_args = [user, command, args.raw,]
        if user_password:
            worker_args += [user_password,]

	for host in hosts.strip().split("\n"):
		results.append(pool.apply_async(worker, [host.split()[0]] + worker_args))
		#print result.get(timeout=5)

	# if you uncomment these, it will cause the main process to block
	#pool.close()
	#pool.join()



	for result in results:
		try:
			r = result.get(timeout=args.timeout)
		except (multiprocessing.TimeoutError, SSHKeyNotLoaded) as e:
			if e.__class__ == SSHKeyNotLoaded:
				print "SSH Key not found.  Please load ssh-agent, and specify user if necessary using -u."
				sys.exit(1)
			elif e.__class__ == multiprocessing.TimeoutError:
				print "Timed out waiting for operation"
			else:
				print "Unknown error."

		#print "host: %(host)s, command: %(command)s, result: %(result)s" % ({"host": r[0], "command": r[1], "result": r[2]})
		try:
			if args.greppable:
				print "host: %-48s result: %s" % (r[0], " ".join(r[1].split("\n")))
			elif args.raw:
				print r
			else:
				print "host: %-48s result: %s" % (r[0], textwrap.fill(r[1], width=90, initial_indent="", subsequent_indent="    "))
			#print "host: %-48s result: %s" % (r[0], r[1])
		except:
			pass


##############################################
# Main Processing
##############################################

if __name__ == '__main__':
	main()
