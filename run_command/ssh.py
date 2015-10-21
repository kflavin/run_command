import sys
import subprocess
import re
from .rcexceptions import SSHKeyNotLoaded

def worker(host, user, command, raw=False, debug=0):
        output = subprocess.Popen(["/usr/bin/ssh", "-o", "NumberOfPasswordPrompts=0", "-o", "ConnectTimeout=2", "-o", "StrictHostKeyChecking=no", "%s@%s" % (user, host), "--", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

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

