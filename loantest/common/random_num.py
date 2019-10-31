#-*-coding: UTF-8 -*-
'''
Created on 2019年10月23日
@author: LIJY
'''

import random

  
def rand_phone():
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152","153", "155", "156", "157", "158", "159", "186", "187", "188"]
    num = ''.join([random.choice('0123456789') for i in range(0,8)])
    randpre = random.choice(prelist)
    phone = randpre+num
    return phone