# encoding: utf-8
'''
Created on 22Jun.,2017

@author: Matthew Rademaker
@email: matthew@acctv.com.au

Functions to communicate with the TOA system. Can send
and receive plain and xml messages.

Note that the _TIMEOUT setting can affect whether
messages are sent or received correctly. It should be as
low as possible, but not lower. Ping the TOA server from the machine you are
running your app from, and put the timeout just a bit higher than
the longest ping e.g. 0.5 if the longest ping was 400ms. If your app seems to block,
try increasing it. If you get lots of "half-message" exceptions, try decreasing it. '''
import socket
import model
from datetime import datetime, timedelta
import time
import hashlib

sock = None
_TIMEOUT = 0.5

def _connect():
    '''Performs the handshake with TOA using stored connection details.
    Returns a list of response messages :: [str]
    '''
    global sock, _TIMEOUT
    comp_name = socket.gethostname()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(_TIMEOUT)
    sock.connect((_connect.ip, _connect.port))
    send_message('handshake', 'handshake')
    send_message('host ' + comp_name + '')
    send_message('ipv4 ' + _connect.ip + '')
    send_message('appID ' + _connect.app + '')
    response = send_message('user ' + _connect.user + '', 'authorized')
    if not response and send_message('user ' + _connect.user + '', 'passwordRequired'):
        if not _connect.password:
            raise Exception('password required')
        return send_message('password ' + _connect.password + '', 'authorized')

    return response

def connect(ip, port, user, app='just:play', password=None):
    '''(ip :: str, port :: int, user :: str, app :: str, [password] :: str)
    Connect to TOA with the given details. Returns a dictionary of
    connection details e.g. repository locations, channel format :: dict
    '''
    # Store the connection details in the _connect function
    # for easy reconnects
    _connect.ip = ip
    _connect.port = port
    _connect.user = user
    _connect.app = app
    _connect.password = sha_digest(password) if password else None
    response = _connect()
    chann_details = {}
    if 'channelConnected' in response:
        for x in response:
            if x.startswith('videoRepository'):
                chann_details['videoRepository'] = x[x.find(' ') + 1:]
            if x.startswith('graphicRepository'):
                chann_details['graphicRepository'] = x[x.find(' ') + 1:]
            if x.startswith('playlistRepository'):
                chann_details['playlistRepository'] = x[x.find(' ') + 1:]
            if x.startswith('format'):
                chann_details['format'] = x[x.find(' ') + 1:]
                chann_details['fps'] = fps[chann_details['format']]
        return chann_details
    elif 'notAuthorized' in response:
        raise Exception('incorrect user name or password')
    else:
        disconnect()
        time.sleep(3)
        return connect(ip, port, user, app, password)

def disconnect():
    '''Close the connection to TOA.'''
    global sock
    sock.close()

def reconnect():
    '''Restore the connection to TOA.'''
    global sock
    disconnect()
    time.sleep(3)
    _connect()

def send(message):
    '''Send text to TOA.'''
    global sock
    print 'message: ' + message
    while True:
        try:
            sock.sendall(message + '\x00')
        except socket.timeout:
            continue
        except Exception, e:
            if e.errno == 54 or e.errno == 32 or e.errno == 104:
                reconnect()
            else:
                raise
        else:
            break

def send_message(message, response_prefix=None):
    '''Send a message to TOA, and return the response if appropriate.'''
    send(message)
    if response_prefix:
        messages = []
        found_start = False
        responses = read_messages()
        for message in responses:
            if found_start:
                messages.append(message)
            elif message.startswith(response_prefix):
                found_start = True
                print 'response: ' + message
                messages.append(message)

        return messages

def send_xml_message(message, expect_response=True):
    '''(message :: str, expect_response :: bool)
    Send a message to the connected app, and return the xml of the response if
    appropriate. :: str
    '''
    first_space = message.find(' ')
    first_close_caret = message.find('>')
    if first_space < 0:
        end_of_tag = first_close_caret
    elif first_close_caret < 0:
        end_of_tag = first_space
    else:
        end_of_tag = min(first_space, first_close_caret)

    res_tag = message[1:end_of_tag]
    res_tag = 'ret' + res_tag[0].upper() + res_tag[1:]
    send(message)
    if expect_response:
        i = 0
        while True:
            try:
                response = read_xml_message(tag=res_tag)
            except Exception, e:
                if not e or e.errno == 1 or e.errno == 54 or e.errno == 32 or e.errno == 104:
                    'xml message error: reconnecting and resending'
                    reconnect()
                    return send_xml_message(message, expect_response)
                else:
                    raise
            if response:
                print response
                return response
            # Keep trying until we get our response
            else:
                time.sleep(0.1 * i)
                if i == 100:
                    reconnect()
                    send(message)
                if i == 200:
                    raise Exception('could not get desired response')
            i += 1

def read_messages():
    '''Read all waiting messages and return them in a list'''
    global sock
    stream = ''
    while True:
        try:
            bytes = sock.recv(4096)
        except socket.timeout:
            break
        except socket.error:
            print 'socket error'
            break
        if bytes.startswith('!bin!') or bytes.startswith('heartbeat'):
            break
        stream += bytes
        if bytes == '':
            print 'empty bytes'
            break

    return [message for message in stream.split('\x00') if message != '' and
            not message.startswith('heartbeat') and not message.startswith('!bin!')]

def read_xml_message(tag=''):
    '''Churn through messages to find the xml delimited by the given tag.'''
    start_tag = tag
    messages = read_messages()
    for msg in messages:
        text = ''
        in_tag = False
        for char in msg:
            if tag == '':
                if in_tag:
                    if char == ' ' or char == '/' or char == '>':
                        tag = text
                        text = '<' + text + char
                    else:
                        text += char
                elif char == '<':
                    in_tag = True
            elif text.endswith(tag) and text != '<' + tag:
                if text.startswith('<' + start_tag):
                    return text + char
                else:
                    exc = Exception('caught half the return message')
                    exc.errno = 1
                    raise exc
            else:
                text += char

def sha_digest(text):
    '''Return the hexadecimal SHA1 digest of the given text.'''
    return hashlib.sha1(text).hexdigest()

#Map of formats to their framerate
fps = {'SD PAL' : 25.0,
       'SD NTSC' : 29.97,
       'SD NTSC 23.98' : 23.98,
       'HD 720p50' : 50.0,
       'HD 720p60' : 60.0,
       'HD 1080i25' : 25.0,
       'HD 1080i29.97' : 29.97,
       'HD 1080i30' : 30.0,
       'HD 1080p24' : 24.0,
       'HD 1080p23.98' : 23.98,
       'HD 720p24' : 24.0,
       'HD 720p23.98' : 23.98,
       'HD 720p59.94' : 59.94}
