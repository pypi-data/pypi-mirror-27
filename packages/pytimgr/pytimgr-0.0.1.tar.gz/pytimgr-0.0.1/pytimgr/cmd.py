"""pytimgr - Python Tidy Container Lifecycle Manager"""
import argparse

import pytimgr.tipd
import pytimgr.tikv
import pytimgr.tidb

def main():
  parser = argparse.ArgumentParser(prog='pytimgr',
  description='Python Tidy Container Lifecycle Manager',
  epilog="MORE INFO: pytimgr {codis|tipd|tikv|tidb} --help")

  parser.add_argument("-v", "--verbosity", help="set logging verbosity" , action="count", default=0)

  subparsers = parser.add_subparsers(help='sub-commands')

  parser_tipd = subparsers.add_parser('tipd', help='tipd container management')
  parser_tipd.add_argument("-p", "--prestart",
  help="run prestart health checks", action="store_true")
  parser_tipd.add_argument("-c", "--changed",
  help="handle lifecycle changes", action="store_true")
  
  parser_tikv = subparsers.add_parser('tikv', help='tikv container management')
  parser_tikv.add_argument("-p", "--prestart",
  help="run prestart health checks", action="store_true")
  
  parser_tidb = subparsers.add_parser('tidb', help='tidb container management')
  parser_tidb.add_argument("-p", "--prestart",
  help="run prestart health checks", action="store_true")
  
  args = parser.parse_args()

