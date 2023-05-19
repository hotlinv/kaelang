
import argparse, os, sys
import kae
from shutil import copyfile

def cli():
    """
    命名程序入口
    """
    parser = argparse.ArgumentParser(prog='ka', description='kae工具箱')
    subparsers = parser.add_subparsers(
        title='kae command',
        metavar='command')

    # workspace
    status_parser = subparsers.add_parser(
        'apphere',
        help='在本目录创建新应用')
    status_parser.set_defaults(handle=handle_apphere)

    # compile
    add_parser = subparsers.add_parser(
        'compile',
        help='编译文本')
    add_parser.add_argument(
        'source',
        help='要编译的源码',
        nargs='*')
    add_parser.set_defaults(handle=handle_compile)

    # run
    add_parser = subparsers.add_parser(
        'run',
        help='运行文本')
    add_parser.add_argument(
        'source',
        help='要编译运行的源码',
        nargs='*')
    add_parser.set_defaults(handle=handle_run)

    args = parser.parse_args()
    if hasattr(args, 'handle'):
        args.handle(args)
    else:
        parser.print_help()


def handle_apphere(args):
    """
    处理 apphere 命令
    """
    nowdir = os.path.abspath(".")
    kaedir = os.path.split(kae.__file__)[0]
    kaepdir = os.path.split(kaedir)[0]
    conff = os.path.join(kaepdir, "urlmap.yml")
    tarf = os.path.join(nowdir, "kappcnf.yml")
    copyfile(conff, tarf)
    print("new app", nowdir, kaedir)

def handle_compile(args):
    """
    处理 compile 命令
    """
    print("compile", args.source)

def handle_run(kae, args):
    """
    处理 run 命令
    """
    print("run", args.source)