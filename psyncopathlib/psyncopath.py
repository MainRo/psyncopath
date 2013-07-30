import sys
import os
import string
from subprocess import *

config = {}

exclude_patterns = ['*.swp']

class Sync(object):
   def __init__(self):
      self.local_path = ""
      self.remote_path = ""
      self.host = None
      self.temp_dir = None
      self.preserve_permissions = True

   def setMode(self, mode):
      if mode== 'smb':
         self.preserve_permissions = False
         if self.temp_dir == None
            self.temp_dir = '/tmp/rsync'

   def setPath(self, local, remote):
      self.local_path = string.replace(local, " ", "\ ")
      self.remote_path = string.replace(remote, " ", "\ ")

   def setHost(self, host):
      self.host = host

   '''
      Sets a local directory for filesystems that do not support mkstemp
   '''
   def setTempDir(self, temp_dir):
      os.mkdir(temp_dir)
      self.temp_dir = temp_dir

   def getExcludeParam(self):
      exclude_param = ""
      for pattern in exclude_patterns:
         exclude_param += '--exclude \'' + pattern + '\' '
      return exclude_param


   def push(self):
      rsync_cmd = "rsync -vaz --delete "
      if self.preserve_permissions == False:
         rsync_cmd += "--no-p "
      if self.temp_dir != None:
         rsync_cmd += "--temp-dir=" + self.temp_dir + " "
      rsync_cmd += self.getExcludeParam()
      rsync_cmd += '--backup --backup-dir=\''
      rsync_cmd += self.remote_path + '/deleted/\' '
      rsync_cmd += '\'' + self.local_path + "/\' "

      rsync_cmd += '\''
      if self.host != None:
         rsync_cmd += self.host + ":"
      rsync_cmd += self.remote_path + "/sync/"
      rsync_cmd += '\' '

      print "executing " + rsync_cmd
      p = Popen(rsync_cmd, shell=True)
      p.wait()

   def pull(self):
      rsync_cmd = "rsync -vaz --delete "

      rsync_cmd += '\''
      if self.host != None:
         rsync_cmd += self.host + ":"
      rsync_cmd += self.remote_path + "/sync/"
      rsync_cmd += '\' '

      rsync_cmd += '\'' + self.local_path + "/\' "

      print "executing " + rsync_cmd
      p = Popen(rsync_cmd, shell=True)
      p.wait()

def usage():
   print "Psyncopath 1.1"
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

   for key in config[workspace]:
      if key == 'mode':
         synchronizer.setMode(config[workspace][key])
      elif key == 'temp_dir':
         synchronizer.setTempDir(config[workspace][key])
      elif key == 'server':
         synchronizer.setHost(config[workspace][key])

   if way == "push":
      synchronizer.push()
   else:
      synchronizer.pull()


