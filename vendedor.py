import subprocess

class Vendedor(object):
    def get_vendedor(self,mac):
        subprocess.call(["oui",mac], shell=True)

