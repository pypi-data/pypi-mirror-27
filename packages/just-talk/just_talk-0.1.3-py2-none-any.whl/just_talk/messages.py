# encoding: utf-8
'''
Created on 22Jun.,2017

@author: Matt
'''

import xml.etree.cElementTree as ElementTree
import model
import comms

__last_message_result = False

def request_node(date):
    """Return the day node for the given date"""
    request = '<requestNode date="' + str(model.toaTimecode.fromdatetime(date)) + '" />'
    response = comms.send_xml_message(request)
    day = model.Day(xml=get_xml(response))
    __update_result(day.toaStart.year == date.year and
                    day.toaStart.month == date.month and
                    day.toaStart.day == date.day)

    return day


def request_insert(node, parent_id, before_id=None, exists=False, set_start=False):
    if not node.getroot():
        __update_result(False)
        return

    request = ('<requestInsert parentId="' + parent_id + '" ' +
               ('beforeId="' + before_id + '" ' if before_id else '') +
               'exists="' + ('T' if exists else 'F') + '" '
               'setStart="' + ('T' if set_start else 'F') + '">' +
               str(node) + '</requestInsert>\x00')
    response = comms.send_xml_message(request)
    # The response will be the sub-nodes of a day, so
    # put them into a temporary day object
    day = model.Day(xml=get_xml('<node id="x" class="1">' + response + '</node>'))

    # Pick the constructor based on the class number
    nodes = [model.classes[int(n.get('class'))](element=n)
             for n in day.getroot().iter('node')]

    found = False
    for n in nodes:
        found = found or n.nid == node.nid

    __update_result(found)
    return nodes


def request_update(node):
    if not node.getroot():
        __update_result(False)
        return

    __update_result(False)
    request = '<requestUpdate>' + str(node) + '</requestUpdate>\x00'
    print request
    response = comms.send_xml_message(request)
    # The response will include all the subnodes of the given node, so
    # return a new node of the same class with all the subnodes. This
    # is especially necessary for updating a day, since all subnodes
    # will be given new ids by TOA
    xml = get_xml(response)
    new_node = model.classes[int(node.getroot().get('class'))](xml=xml)

    __update_result(True)
    return new_node


def request_delete(nodes):
    """Return the nodes that were deleted and whether all were
    deleted successfully :: (Bool, [Node])
    """
    request = '<requestDelete>'
    for n in nodes:
        if n.nid is not None:
            request += '<id>' + str(n.nid) + '</id>'
    request += '</requestDelete>'
    response = ElementTree.fromstring(comms.send_xml_message(request))
    deleted = [n.text for n in response.iter('id')]

    __update_result(set(deleted) == set([n.nid for n in nodes]))
    return deleted

def request_format():
    """Return the channel's format, along with its FPS :: (str, float)"""
    response = comms.send_message('requestFormat', True)
    channel_format = response[len('retRequestFormat '):]
    return channel_format

def request_attribute(attr, value, ids):
    """Returns the list of node ids if the update was successful"""
    type = str({v: k for k, v in model.att_types.items()}[attr])
    text = '<requestAttribute><attribute key="' + attr.__name__ + '" type="' + type + '">'
    text += str(value) + '</attribute>'
    text = text.join(['<node>' + str(id) + '</node>' for id in ids]) + '</requestAttribute>'
    response = get_xml(comms.send_xml_message(text))
    if response.getnode().get('success') == 'T':
        return [node.text for node in response.findall('node')]
    else:
        raise Exception('requestAttribute failed')

def request_remove_attribute(node, attribute):
    request = '<requestRemoveAttribute node="' + node + '" key="' + attribute + '" />'
    expected_response = '<retRequestRemoveAttribute node="' + node + '" key="' + attribute + '" />'
    return comms.send_message(request, True) == expected_response


def request_warnings(from_time, to_time):
    request = ('<requestWarnings from="' + str(from_time) + '" to="' + str(to_time) + '" />')
    response = get_xml(comms.send_xml_message(request))
    return [line[len('<warning>'):-len('</warning>')] for line in response.split('\n') if line != '']

def request_real_time_container():
    pass

def request_tracks():
    response = get_xml(comms.send_message('requestTracks', True))
    return [model.ChannelTrack.fromxml(track) for track in response.iter('track')]

def playtrack(track_id):
    comms.send_message('playtrack ' + track_id, False)

def cuedtrack(track_id):
    comms.send_message('cuedtrack ' + track_id, False)

def nexttrack(track_id):
    comms.send_message('nexttrack ' + track_id, False)

_NXT_ACT_DO_NOTHING = 0
_NXT_ACT_PLAY_NEXT = 1
_NXT_ACT_CUE_NEXT = 2
_NXT_ACT_HOLD_LAST = 3
_NXT_ACT_RELOAD = 4
_NXT_ACT_RECUE = 5
_NXT_ACT_HOLD_AND_CUE_NEXT = 6
_NXT_ACT_HOLD_AND_PLAY_NEXT = 7

def skiptrack(track_id, next_action=None):
    comms.send_message('skiptrack ' + track_id + (' ' + next_action if next_action else ''))

def playingNode():
    playing = None
    while True:
        messages = comms.read_messages()
        for mes in messages:
            if mes.startswith('<playingNode'):
                playing = ElementTree.fromstring(mes)
                break

    node = playing.get('id')
    audio_tracks = int(playing.find('audioTracks').text)
    start = model.toaTimecode(playing.find('timecode').text)
    node_uid = playing.find('nodeUID').text
    track_id = playing.find('trackID').text

    requestAttribute(node, 'toaStart', start)

    return {node, audio_tracks, start, node_uid, track_id}

def finishedNode():
    pass

def stopFrameNode():
    pass

def triggerNode():
    pass

def heartbeat():
    while True:
        messages = comms.read_messages()
        for mes in messages:
            if mes.startswith('heartbeat'):
                return model.toaTimecode(mes[10:21])


def engineLost():
    while True:
        messages = comms.read_messages()
        for mes in messages:
            if mes.startswith('<engineLost'):
                return mes[12:-13]

def unblockTime():
    pass


def get_xml(request):
    """Strips the request tag from a response and returns the xml"""
    open_tag_end = request.find('>')
    close_tag_start = request.rfind('</')
    return request[open_tag_end + 1:close_tag_start]


def __update_result(result):
    global __last_message_result
    if type(result) == bool:
        __last_message_result = result
    else:
        raise TypeError('result can only be set to a bool')

def last_result():
    global __last_message_result
    return __last_message_result


