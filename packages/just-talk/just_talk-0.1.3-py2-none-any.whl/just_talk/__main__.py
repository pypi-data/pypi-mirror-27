# encoding: utf-8
'''
Created on 22Jun.,2017

@author: Matt
'''
import comms
import model
import messages

if __name__ == '__main__':
    try:
        comms.connect('127.0.0.1', 5520, 'Matt')
        model.FPS = messages.request_format()[1]


    finally:
        comms.disconnect()
