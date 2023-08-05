# encoding: UTF-8

import cmd
import csv
import os
import shutil
import string
import sys
import platform
import subprocess


from flyshare.backtest.analysis import backtest_analysis_start
from flyshare.util import log_info, Setting, util_mongo_initial, util_mongo_make_index
from flyshare import (save_stock_list, save_stock_min, save_stock_xdxr, save_stock_block, save_stock_info,
                      save_stock_day, save_index_day, save_index_min, save_etf_day, save_etf_min,
                      update_stock_day)

from flyshare import *
from flyshare import __version__


class CLI(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'flyshare> '    # 定义命令行提示符

    def do_shell(self, arg):
        "run a shell commad"
        print (">", arg)
        sub_cmd = subprocess.Popen(arg,shell=True, stdout=subprocess.PIPE)
        print (sub_cmd.communicate()[0])

    def do_version(self, arg):
        log_info(__version__)

    def help_version(self):
        print("syntax: version [message]",)
        print("-- prints a version message")

    #@click.command()
    #@click.option('--e', default=1, help='Number of greetings.')
    def do_examples(self, arg):
        log_info('flyshare example')
        now_path = os.getcwd()
        project_dir = os.path.dirname(os.path.abspath(__file__))
        file_dir = ''
        log_info('Copy a example strategy from :  ' + project_dir)
        if platform.system() == 'Windows':
            file_dir = project_dir + '\\backtest_example.py'
        elif platform.system() in ['Linux', 'Darwin']:
            file_dir = project_dir + '/backtest_example.py'

        shutil.copy(file_dir, now_path)

        log_info('Successfully generate a example strategy in :  ' + now_path)

    def help_examples(self):
        print('make a sample backtest framework')

    def do_drop_database(self, arg):
        util_mongo_initial()

    def help_drop_database(self):
        print('drop flyshare\'s databases')

    def do_make_index(self, arg):
        util_mongo_make_index()

    def help_make_index(self):
        print('make index for flyshare databases')

    def do_quit(self, arg):
        sys.exit(1)

    def help_quit(self):
        print("syntax: quit",)
        print("-- terminates the application")

    def do_clean(self, arg):
        try:
            if platform.system() == 'Windows':
                os.popen('del back*csv')
                os.popen('del *log')
            else:
                os.popen('rm -rf back*csv')
                os.popen('rm -rf  *log')

        except:
            pass

    def help_clean(self):
        log_info('Clean the old backtest reports and logs')

    def do_exit(self, arg):     # 定义quit命令所执行的操作
        sys.exit(1)

    def help_exit(self):
        print('syntax: exit')
        print("-- terminates the application")

    def do_save(self, arg):
        # 仅仅是为了初始化才在这里插入用户,如果想要注册用户,要到webkit底下注册
        if arg == '':
            print(
                "Usage: save all|X|x|day|min|insert_user|stock_day|stock_xdxr|stock_min|index_day|index_min|etf_day|etf_min|stock_list|stock_block")
        else:
            arg = arg.split(' ')
            if len(arg) == 1 and arg[0] == 'all':
                Setting.client.flyshare.user_list.insert(
                    {'username': 'admin', 'password': 'admin'})
                save_stock_day('tdx')
                save_stock_xdxr('tdx')
                #save_stock_min('tdx')
                save_index_day('tdx')
                #save_index_min('tdx')
                #save_etf_day('tdx')
                #save_etf_min('tdx')
                save_stock_list('tdx')
                save_stock_block('tdx')
                #save_stock_info('tdx')
            elif len(arg) == 1 and arg[0] == 'day':
                Setting.client.flyshare.user_list.insert(
                    {'username': 'admin', 'password': 'admin'})
                save_stock_day('tdx')
                save_stock_xdxr('tdx')
                #save_stock_min('tdx')
                save_index_day('tdx')
                #save_index_min('tdx')
                save_etf_day('tdx')
                #save_etf_min('tdx')
                save_stock_list('tdx')
                save_stock_block('tdx')
            elif len(arg) == 1 and arg[0] == 'min':
                Setting.client.flyshare.user_list.insert(
                    {'username': 'admin', 'password': 'admin'})
                #save_stock_day('tdx')
                save_stock_xdxr('tdx')
                save_stock_min('tdx')
                #save_index_day('tdx')
                save_index_min('tdx')
                #save_etf_day('tdx')
                save_etf_min('tdx')
                save_stock_list('tdx')
                save_stock_block('tdx')
            elif len(arg) == 1 and arg[0] in ['X','x']:
                Setting.client.flyshare.user_list.insert(
                    {'username': 'admin', 'password': 'admin'})
                save_stock_day('tdx')
                save_stock_xdxr('tdx')
                save_stock_min('tdx')
                save_index_day('tdx')
                save_index_min('tdx')
                save_etf_day('tdx')
                save_etf_min('tdx')
                save_stock_list('tdx')
                save_stock_block('tdx')
                #save_stock_info('tdx')
            else:
                for i in arg:
                    if i == 'insert_user':
                        if Setting.client.flyshare.user_list.find({'username': 'admin'}).count() == 0:
                            Setting.client.flyshare.user_list.insert(
                                {'username': 'admin', 'password': 'admin'})
                    else:
                        eval("save_%s('tdx')" % (i))

    def help_save(self):
        log_info('Save all the stock data from pytdx')

    def do_fn(self, arg):
        try:
            log_info(eval(arg))
        except:
            print(Exception)

    def help(self):
        log_info('fn+methods name')


def sourcecpy(src, des):
    src = os.path.normpath(src)
    des = os.path.normpath(des)
    if not os.path.exists(src) or not os.path.exists(src):
        print("folder is not exist")
        sys.exit(1)
    # 获得原始目录中所有的文件，并拼接每个文件的绝对路径
    os.chdir(src)
    src_file = [os.path.join(src, file) for file in os.listdir()]
    for source in src_file:
        # 若是文件
        if os.path.isfile(source):
            shutil.copy(source, des)  # 第一个参数是文件，第二个参数目录
        # 若是目录
        if os.path.isdir(source):
            p, src_name = os.path.split(source)
            des = os.path.join(des, src_name)
            shutil.copytree(source, des)  # 第一个参数是目录，第二个参数也是目录

# 创建CLI实例并运行
def flyshare_cmd():
    cli = CLI()
    cli.cmdloop()
