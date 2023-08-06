#!/usr/bin/python
# -*- coding: utf-8 -*-
# Github: https://github.com/SarbazVatan/py2pyc
# Email: soldier.of.iran.dev@gmail.com
# Coded By @Soldier_of_iran
# [Sarbaz_Vatan]


import sys
import py_compile
import os

reload(sys)
sys.setdefaultencoding("utf-8")


class STEPS:
    def __init__(self):
        pass

    @staticmethod
    def step1(path):
        if os.path.isfile(path):
            return True
        else:
            return False

    @staticmethod
    def step2(path):
        py_list = ['py', 'PY', 'pY', 'Py']
        if str(os.path.basename(path)).split('.')[len(str(os.path.basename(path)).split('.')) - 1] in py_list:
            return True
        else:
            return False

    @staticmethod
    def step3(path):
        soruce = open(path, 'r').readlines()
        coded = ''

        for word in soruce:
            coded += str(word).encode('hex')

        final = 'exec str("' + str(coded) + '").decode("hex")'
        return final

    @staticmethod
    def step4(source):
        result = r'exec str(unichr(10)'
        for wd in source:
            bb = int(ord(str(wd)))
            cc = ' + unichr({})'.format(bb)
            result += cc
        result += ')'
        return result


class COMPILE:
    def __init__(self, path):
        go_steps = STEPS()
        print '\n[+]Filename: %s' % (os.path.basename(path))+'\n\n'+'#'*50+'\n\n'

        if path != '':
            stp1 = go_steps.step1(path)
            if stp1 == True:
                stp2 = go_steps.step2(path)
                if stp2 == True:
                    stp3 = go_steps.step3(path)
                    stp4 = go_steps.step4(stp3)
                    new_name = 'Compiled_%s' % (os.path.basename(path))
                    with open(new_name, 'w') as fp:
                        fp.write(stp4)
                    fp.close()
                    py_compile.compile(new_name)
                    os.remove(new_name)
                    os.renames(str(new_name)+'c', new_name)
                    print(str('\n[+]Status: [Compiled]\n\n[+]Result Saved: %s\n' % (new_name)))
                    quit()
                else:
                    print('\n\n[-]ERROR: Python_File')
                    quit()
            else:
                print('\n\n[-]ERROR: File')
                quit()
        else:
            print('\n\n[-]ERROR: Dir')
            quit()
