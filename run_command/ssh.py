import sys
import os
import subprocess
import re
import shlex
from .rcexceptions import SSHKeyNotLoaded

def worker(host, user, command, raw=False, password=None, debug=0):

        if password:
            passwordprompts = 1
        else:
            passwordprompts = 0

        ssh_command = "setsid /usr/bin/ssh"
        ssh_command += " -o numberofpasswordprompts=%s" % passwordprompts 
        ssh_command += " -o connecttimeout=2 -o stricthostkeychecking=no" 
        ssh_command += " %s@%s" % (user,host,)
        ssh_command += " -- "
        ssh_command += command
        print ssh_command
        ssh_command = shlex.split(ssh_command)

        #output = subprocess.Popen(["setsid", "/usr/bin/ssh", "-o", "numberofpasswordprompts=%s" % passwordprompts, "-o", "connecttimeout=2", "-o", "stricthostkeychecking=no", "%s@%s" % (user, host), "--", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        output = subprocess.Popen(ssh_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

	if re.match("^Permission denied", output[1]):
		raise SSHKeyNotLoaded("SSH Key not loaded through agent.")


        if raw:
                if debug:
                        return output[0].strip() + output[1].strip()
                else:
                        if not output[0] and output[1]:
                                return output[1].strip()
                        else:
                                return output[0].strip()
        else:
                if debug:
                        return host, output[0].strip() + output[1].strip()
                else:
                        if not output[0] and output[1]:
                                return host, output[1].strip()
                        else:
                                return host, output[0].strip()

