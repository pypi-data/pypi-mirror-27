"""
The Node.py command-line interface.
"""

from nodepy.utils import path
from nodepy.loader import PythonModule
import argparse
import code
import functools
import os
import pathlib2 as pathlib
import pdb
import nodepy
import six
import sys

try:
  from urllib.parse import urlparse
except ImportError:
  from urlparse import urlparse

VERSION = 'nodepy {}\n[{} {}]'.format(
  nodepy.__version__, nodepy.runtime.implementation, sys.version.replace('\n', ''))

parser = argparse.ArgumentParser()
parser.add_argument('request', nargs='...')
parser.add_argument('-c')
parser.add_argument('--maindir')
parser.add_argument('--version', action='store_true')
parser.add_argument('--pymain', action='store_true')
parser.add_argument('--pmd', action='store_true')
parser.add_argument('--keep-arg0', action='store_true')
parser.add_argument('--nodepy-path', action='append', default=[])
parser.add_argument('--python-path', action='append', default=[])


class ReplModule(nodepy.loader.PythonModule):

  def set_exec_handler(self, handler):
    self._exec_code = lambda code: handler()

  def _load_code(self):
    return None

  def _init_extensions(self, code):
    pass


def check_pmd_envvar():
  """
  Checks the value of the `NODEPY_PMD` environment variable. If it's an
  integer, it will be decrement by one. If the value falls below one, then
  the variable is unset so that future child processes can't inherit it.
  If the value is anything other than a string, it will be left unchanged.
  """

  value = os.environ.get('NODEPY_PMD', '')
  try:
    level = int(value)
  except ValueError:
    level = None

  if level is not None and level <= 0:
    value = ''
  elif level is not None and level <= 1:
    os.environ.pop('NODEPY_PMD', '')
  elif level is not None:
    os.environ['NODEPY_PMD'] = str(level - 1)

  return bool(value)


def install_pmd(ctx):
  """
  Installs the post-mortem debugger which calls #Context.breakpoint().
  """

  @functools.wraps(sys.excepthook)
  def wrapper(type, value, traceback):
    ctx.breakpoint(traceback)
    return wrapper.__wrapped__(type, value, traceback)

  sys.excepthook = wrapper


def main(argv=None):
  args = parser.parse_args(argv)
  args.nodepy_path.insert(0, '.')
  if args.version:
    print(VERSION)
    return 0

  args.pmd = check_pmd_envvar() or args.pmd
  sys.argv = [sys.argv[0]] + args.request[1:]

  maindir = pathlib.Path(args.maindir) if args.maindir else pathlib.Path.cwd()
  ctx = nodepy.context.Context(maindir)

  # Updat the module search path.
  args.nodepy_path.insert(0, ctx.modules_directory)
  ctx.resolver.paths.extend(x for x in map(pathlib.Path, args.nodepy_path) if x.is_dir())
  ctx.localimport.path.extend(args.python_path)

  # Create the module in which we run the REPL or the command
  # specified via -c.
  if args.c or not args.request:
    filename = nodepy.utils.path.VoidPath('<repl>')
    directory = pathlib.Path.cwd()
    repl_module = ReplModule(ctx, None, filename, directory)
    repl_module.init()

  with ctx.enter():
    if args.pmd:
      install_pmd(ctx)
    if args.c:
      repl_module.set_exec_handler(lambda: six.exec_(args.c, vars(repl_module.namespace)))
      repl_module.load()
    if args.request:
      try:
        filename = path.urlpath.make(args.request[0])
      except ValueError:
        filename = args.request[0]
      ctx.main_module = ctx.resolve(filename)
      if not args.keep_arg0:
        sys.argv[0] = str(ctx.main_module.filename)
      ctx.main_module.init()
      if args.pymain:
        ctx.main_module.namespace.__name__ = '__main__'
      ctx.load_module(ctx.main_module, do_init=False)
    elif not args.c:
      ctx.main_module = repl_module
      repl_module.set_exec_handler(lambda: code.interact('', local=vars(repl_module.namespace)))
      repl_module.load()


if __name__ == '__main__':
  sys.exit(main())
