#!/usr/bin/env python
import sys
import argparse

import npu_compiler
from npu_compiler.config import Config
from npu_compiler.ops_dict import OpsDict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='gxnpuc', description='NPU Compiler')
    parser.add_argument('-V', '--version', action='version', version='gxnpuc %s' % Config.VERSION)
    parser.add_argument('-L', '--list', action="store_true", help='list supported ops')
    parser.add_argument('config_filename', nargs='?', help='config file')
    args = parser.parse_args()
    if args.list:
        print("Supported OPs:")
        ops = OpsDict.get_tf_ops()
        ops.sort()
        for op in ops:
            print("\t -  %s" % op)
        sys.exit()
    if args.config_filename:
        npu_compiler.run(args.config_filename)
        sys.exit()
    else:
        parser.print_help()

