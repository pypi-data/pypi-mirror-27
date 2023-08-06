# coding:utf-8
"""
chechsum --hash md5 ./__main__.py
"""
import sys
from checksum import main_argv

__author__ = 'cupen'
__email__ = 'cupen@foxmail.com'

if __name__ == '__main__':
    exit(main_argv(sys.argv[1:]))
    pass
