#!/usr/bin/env python

import time

def imprimeTempo(tabela):
    t0 = time.clock()
    tf = time.clock()
    for process in tabela:
        while (tf - t0 < process[0]):
            tf = time.clock()
        
        print "Cheguei no tempo {} inicio do processo {}".format(tf-t0, process[1])
