import sys
import os
from subprocess import *

config = {}

class Sync(object):
   def __init__(self):
      self.local_path = ""
      self.remote_path = ""
      self.host = ""

   def setPath(self, local, remote):
      self.local_path = local
      self.remote_path = remote

   def setHost(self, host):
      self.host = host

   def push(self):
      rsync_cmd = "rsync -vaz --delete --backup --backup-dir="
      rsync_cmd += self.remote_path + "/deleted/ "
      rsync_cmd += self.local_path + "/ "
      rsync_cmd += self.host + ":"
      rsync_cmd += self.remote_path + "/sync/ "

      print "executing " + rsync_cmd
      p = Popen(rsync_cmd, shell=True)
      p.wait()

   def pull(self):
      rsync_cmd = "rsync -vaz --delete "
      rsync_cmd += self.host + ":"
      rsync_cmd += self.remote_path + "/sync/ "
      rsync_cmd += self.local_path

      print "executing " + rsync_cmd
      p = Popen(rsync_cmd, shell=True)
      p.wait()

def usage():
   print "Psyncopath 1.0"
   print "Usage:"
   print "psynchopath [workspace] [way]"
   print "\tworkspace : workspace configuration name"
   print "\tway : push or pull"

def main():
   config_file = os.environ['HOME'] + '/.psyncopath'
   if os.path.exists(config_file ) == False:
      usage()
      sys.exit("no config file found.")

   if len(sys.argv) != 3:
      usage()
      sys.exit("invalid argument.")

   workspace = sys.argv[1]
   way = sys.argv[2]

   if way != "push" and way != "pull":
      usage()
      sys.exit("invalid way")

   execfile(config_file)
   synchronizer = Sync()

   synchronizer.setPath(config[workspace]['local_path'], config[workspace]['remote_path'])
   synchronizer.setHost(config[workspace]['server'])
   if way == "push":
      synchronizer.push()
   else:
      synchronizer.pull()


