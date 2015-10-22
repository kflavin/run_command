import argparse
import sys

parser = argparse.ArgumentParser(description='Run a command against a list of machines.  The list of machines is a new line delimited file.  You must have your SSH key loaded into the ssh-agent prior to running.')
parser.add_argument('file', metavar='file', type=file, nargs=1, help='file to read from')
parser.add_argument('command', metavar='command', type=str, nargs=1, help='command to run')
parser.add_argument('--sudo', action='store_true', help='run with sudo')
parser.add_argument('--debug', action='store_true', help='debug mode')
parser.add_argument('--timeout', default=5, type=int, help='Set timeout.  Default is 5 seconds.  You may need to set it higher for long running commands.')
parser.add_argument('-g', dest="greppable", action='store_true', help='greppable output')
parser.add_argument('-r', dest="raw", action='store_true', help='raw output')
parser.add_argument('-u', dest="user", help='run as a user other than the active one')
parser.add_argument('-p', dest="password", action="store_true", help='specify a fallback password')

try:
	args = parser.parse_args()
except IOError as e:
	print "File does not exist.  Please enter the name of a valid file with fully qualified host names."
	sys.exit(1)
except Exception as e:
	print "Unknown error."
	sys.exit(1)

debug = args.debug

