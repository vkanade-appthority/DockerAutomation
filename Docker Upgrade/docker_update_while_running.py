#!/usr/bin/env python

from argparse import ArgumentParser
from argparse import ArgumentError
from docker import Client
import sys
import os

def main():
  program = sys.argv[0].strip(' .\/')

  parser = ArgumentParser(prog=program,usage='%(prog)s [OPTIONS] COMMAND [arg...]',epilog='Run \'%(prog)s COMMAND --help\' for more information on a command.')
  parser.add_argument('--version', action='version', version='%(prog)s 0.0.3')
  parser.add_argument('-c','--containers',dest='container',default='*',nargs='?',help='list of containers to execute separated by comma either container id or name, default: \'*\' for all containers')
  parser.add_argument('--host',dest='host',default='unix:///var/run/docker.sock',help='docker host address unix://SOCK_PATH or http://HOST:PORT')

  subparsers = parser.add_subparsers(prog=program,title='Available Commands',description=None,metavar='')

  # Create update parser
  parser_update = subparsers.add_parser('update', usage='%(prog)s [OPTIONS]',description='Update container packages e.g. perform apt-get upgrade',help='Update linux packages')
  parser_update.add_argument('-p','--packages',dest='package',default='*',nargs='*',help='list of packages to updated separated by space')
  parser_update.set_defaults(command='update')

  # Create exec parser
  parser_exec = subparsers.add_parser('exec', usage='%(prog)s "[CMD]"',description='Execute a single command, equivilant to docker exec CONTAINER COMMAND',help='Execute a command inside the container')
  parser_exec.add_argument('cmd',default='date',nargs='?',help='the command to execute should be quoted if the command has arguments')
  #parser_exec.add_argument('-s','--stream',dest='stream',action='store_true',help='Return command result as streaming response')
  parser_exec.set_defaults(command='exec')

  args = None
  try:
    args = parser.parse_args()
  except:
    print("Error while parsing arguments")
    sys.exit(1)

  process_command(args)


def process_command(args):
  c = Client(base_url=args.host)
  try:
    result = c.ping()
    if "OK" == result:
      run_command(c,args)
      return
  except:
    pass

  c = Client(base_url='unix://tmp/docker.sock')
  try:
    result = c.ping()
    if "OK" == result:
      run_command(c,args)
      return
  except:
    pass
  
  print('Cannot connect to docker: %s'%(result))
  sys.exit(1)
  
def run_command(client, args):
  #print(args)
  containers = None
  if "*" == args.container:
    containers = client.containers()
  else:
    containers = args.container.split(",")

  for container in containers:
    c = None
    c_name = None
    if isinstance(container,str):
      c = container
      c_name = container
    else:
      c = container['Id']
      # Ignore the current container where docker-run is executed
      hostname = os.getenv('HOSTNAME','')
      if len(hostname) > 0 and c.startswith(hostname):
        continue
      c_name = container['Names'][0].strip(' \/')

    print("*** %s ***\n"%(c_name))
    if args.command == 'update':
      client.execute(c,"apt-get update")
      if "*" == args.package:
        print(client.execute(c,"apt-get -y upgrade "))
      else:
        print(client.execute(c,"apt-get -y upgrade %s"%(" ".join(args.package))))
    elif args.command == 'exec':
      print(client.execute(c,['/bin/bash','-c',args.cmd])) #stream=args.stream))

if __name__ == '__main__':
  main()