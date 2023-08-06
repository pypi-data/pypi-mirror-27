#!/usr/bin/env python

'''
.. module:: robolearn
    :platform: Unix, Windows
    :synopsis: Python API to interact with Robolearn
    :noindex:
'''
import urllib2

class Robolearn:

    def __init__(self, url='http://127.0.0.1:9000'):
        self.server = url

    def forward(self):
        self.__server_rpc('forward')

    def rotate(self):
        self.__server_rpc('rotate')

    def __server_rpc(self, action):
        urllib2.urlopen('%s/api/%s' % (self.server, action)).read()

