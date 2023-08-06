# encoding: utf-8
'''
Created on 22Jun.,2017

@author: Matthew Rademaker
@email: matthew@acctv.com.au

Model of nodes and attribute used by the Tools On Air
broadcast API.
'''
import xml.etree.cElementTree as ElementTree
from datetime import datetime, timedelta
import time
import messages
import re
import os
from pymediainfo import MediaInfo
import sys

# There are lots of videos in a day, all stored in a tree - I wish I were writing Haskell
sys.setrecursionlimit(25000)


FPS = 25
VIDEO_REPOSITORY = ''
GRAPHICS_REPOSITORY = ''
_MIN_YEAR = 1900
_XML_DIR = os.path.dirname(__file__) + '/xml/'
_FILE_NOT_EXIST_ERR = 2
_AUTO_TIMEOUT = True

###############
# TOA Classes #
###############

class Node(ElementTree.ElementTree):
    """Generic node"""


    def __init__(self, path=None, xml=None, element=None,
                 nid=None, nclass=None, flags=None, parent_node=None):
        # Use the xml directory as a template to create this object
        super(Node, self).__init__(file=_XML_DIR + type(self).__name__ + '.xml')
        # Can create this from a file, xml, or an ElementTree node
        if path:
            eletree = ElementTree.ElementTree(file=path).getroot()
            if True or self._check_structure(eletree):
                self._setroot(eletree)
            else:
                raise Exception('xml in file is not correct for this type')
        elif xml:
            eletree = ElementTree.fromstring(xml)
            if True or self._check_structure(eletree):
                self._setroot(eletree)
            else:
                raise Exception('xml is not correct for this type')
        elif element is not None:
            if True or self._check_structure(element):
                self._setroot(element)
            else:
                raise Exception('element is not the correct type')

        self.parent_node = parent_node
        self.outstanding_updates = True

        root = self.getroot()
        if root is not None:
            self.nid = str(nid or root.get('id'))
            self.nclass = str(nclass or root.get('class'))
            self.flags = str(flags or root.get('flags'))
            # Make the attributes in the underlying xml available as
            # properties of the object
            for att in root.findall('attribute'):
                self.__dict__[att.get('key')] = att_types[int(att.get('type'))](text=get_text(att))


    def _check_structure(self, element):
        """Ensure the given element has the correct attributes
        and properties for this node type. It only makes sense
        to call this straight after creating the node from a template :: bool
        """

        ele_atts = [(att.get('key'), att.get('type')) for att in element.findall('attribute')]
        my_atts = [(att.get('key'), att.get('type')) for att in self.getroot().findall('attribute')]

        props = ('id' in element.keys() and
                 'class' in element.keys() and
                 str(self.nclass) == element.get('class'))

        return set(my_atts) == set(ele_atts) and props

    def _just_playify(self):
        """Cast all values of attributes to just_play types"""
        root = self.getroot()
        if root is not None:
            for att in root.findall('attribute'):
                set_text(att, str(att_types[int(att.get('type'))](text=get_text(att))))
            for node in root.findall('node'):
                Node(element=node)._just_playify()

    def __getattr__(self, name):
        # Non-XML attributes
        if name == 'outstanding_updates' or name == 'parent_node':
            return super(Node, self).__getattr__(name)
        try:
            root = self.getroot()
        except:
            return super(Node, self).__getattr__(name)
        # XML attributes
        if root is not None:
            if name == 'nid' or name == 'nclass' or name == 'flags':
                return root.get(name.lstrip('n'))
            else:
                for att in root.findall('attribute'):
                    if att.get('key') == name:
                        return att_types[int(att.get('type'))](text=get_text(att))


    def __setattr__(self, name, value):
        # Non-XML attributes
        if (name == '_root' or
            name == 'outstanding_updates' or
            name == 'parent_node'):
            super(Node, self).__setattr__(name, value)
            return
        else:
            root = self.getroot()


        # XML attribute
        previous = self.__getattr__(name)
        if root is not None:
            if name == 'nid' or name == 'nclass' or name == 'flags':
                root.set(name.lstrip('n'), str(value) if value else '')
            elif isinstance(value, JTList):
                self.__dict__[name] = value
            else:
                for att in root.findall('attribute'):
                    if att.get('key') == name:
                        set_text(att, str(value))
                        if isinstance(value, att_types[int(att.get('type'))]):
                            self.__dict__[att.get('key')] = value
                        else:
                            self.__dict__[att.get('key')] = \
                            att_types[int(att.get('type'))](str(value))
                        break

        if name != 'end':
            self.calculate_end()

        # If the start or duration changes, we wanna time it out
        if value != previous:
            global _AUTO_TIMEOUT
            if _AUTO_TIMEOUT and name == 'toaStart' or name == 'toaDuration':
                self.time_out()


    def __eq__(self, other):
        return self.nclass == other.nclass and self.nid == other.nid


    def __str__(self):
        self._just_playify()
        return ElementTree.tostring(self.getroot())


    def get_attributes(self):
        """Get all the attribute nodes of this xml node"""
        if self.getroot() is None:
            return []

        return [att.get('key') for att in self.getroot().findall('attribute')]

    def update(self):
        """Update this node in TOA"""

        node = messages.request_update(self)
        if node.nid == self.nid and node.nclass == self.nclass:
            self = node
            self.outstanding_updates = False
            return

        raise Exception('failed to update node: ' + str(self.nid))

    def find_adam(self):
        """Return the top-level ancestor of the node"""

        if not self.parent_node:
            return self
        else:
            return self.parent_node.find_adam()

    def time_out(self):
        """Align start times and end times of sub and parent nodes"""
        # Recurse up if possible, otherwise recurse down
        if self.parent_node:
            self.parent_node.time_out()
        else:
            self.static_time_out()

    def static_time_out(self):
        # Recurse down
        global _AUTO_TIMEOUT
        saved_timeout_setting = _AUTO_TIMEOUT
        _AUTO_TIMEOUT = False
        for node in self.getroot().findall('node'):
            classes[int(node.get('class'))](element=node.getroot()).static_time_out()
        _AUTO_TIMEOUT = saved_timeout_setting


    def calculate_end(self):
        """Save the user the trouble and automatically add the
        duration to the start and store it as a property"""

        if self.toaDuration and self.toaStart:
            duration_time = self.toaDuration - _YEAR_ZERO
            end = toaTimecode.fromdatetime(self.toaStart + duration_time)
            super(Node, self).__setattr__('end', end)


    def set_attrib(self, attrib, value):
        """Set the text of the underlying xml attribute
        node."""

        if self.getroot():
            for sub in self.getroot():
                if sub.get('key') == attrib:
                    set_text(sub, str(value))
                    break


    def find_by_property(self, prop, value):
        """Find the first child of an element whose property matches
        a value.
        """

        for sub in self.getroot():
            if sub.get(prop) == str(value):
                return sub


    def findall_by_property(self, prop, value):
        """Find all the children of an element whose property matches
        a value.
        """

        matches = []
        if self.getroot():
            for sub in self.getroot():
                if sub.get(prop) == str(value):
                    matches.append(sub)

        return matches


class Day(Node):
    """TOA Day node"""

    def __init__(self, date=None, *args, **kwargs):
        if date is not None:
            day = messages.request_node(date)
            super(Day, self).__init__(nclass=1, element=day.getroot(), *args, **kwargs)
        else:
            super(Day, self).__init__(nclass=1, *args, **kwargs)
        self.playlists = JTList(nclass=2, parent_node=self)
        self.adjusted_start = self.toaStart

    def _check_structure(self, element):
        good_atts = super(Day, self)._check_structure(element)
        good_pls = True
        for node in element.findall('node'):
            good_pls = good_pls and Playlist()._check_structure(node)

        return good_atts and good_pls


    def __setattr__(self, name, value):
        if name == 'toaStart':
            self.adjusted_start = value
        if name == 'adjusted_start':
            self.__dict__[name] = value
        else:
            super(Day, self).__setattr__(name, value)

    def __getattr__(self, name):
        if name == 'adjusted_start':
            return self.__dict__[name]
        else:
            super(Day, self).__getattr__(name)

    def time_out(self):
        global _AUTO_TIMEOUT
        saved_timeout_setting = _AUTO_TIMEOUT
        _AUTO_TIMEOUT = False
        next_start = self.adjusted_start
        i = 0
        for playlist in self.playlists:
            playlist.toaStart = next_start
            playlist.static_time_out()
            next_start = playlist.end
            i += 1
        _AUTO_TIMEOUT = saved_timeout_setting

    def update(self):
        """Update the day. Note that TOA changes the IDs of every sub node of a day."""
        response = messages.request_update(self)

        self.playlists = response.playlists
        self.outstanding_updates = False


class Playlist(Node):

    def __init__(self, *args, **kwargs):
        super(Playlist, self).__init__(nclass=2, *args, **kwargs)
        self.graphic_tracks = JTList(nclass=3, parent_node=self)
        self.video_tracks = JTList(nclass=4, parent_node=self)

    def _check_structure(self, element):
        good_atts = super(Playlist, self)._check_structure(element)
        good_g_tracks = True
        good_v_tracks = True
        for node in element.findall('node'):
            if node.get('class') == '3':
                good_g_tracks = good_g_tracks and GraphicTrack()._check_structure(node)
            elif node.get('class') == '4':
                good_v_tracks = good_v_tracks and VideoTrack()._check_structure(node)
            else:
                return False

        return good_atts and good_g_tracks and good_v_tracks

    def refresh(self, auto_update=True):
        """Check existence of resource files in plays,
        duration, fps etc.
        """
        result = True
        for track in self.graphic_tracks:
            for play in track.plays:
                if not play.check_exists():
                    result = False
                    print 'missing file: ' + play.resource[1]
                else:
                    if play.refresh(auto_update):
                        if auto_update and play.outstanding_updates:
                            play.update()

        for track in self.video_tracks:
            for play in track.plays:
                if not play.check_exists():
                    result = False
                    print 'missing file: ' + play.resource[1]
                else:
                    if play.refresh(auto_update):
                        if auto_update and play.outstanding_updates:
                            play.update()

        if auto_update and self.outstanding_updates:
            self.update()

        return result


    def static_time_out(self):

        global _AUTO_TIMEOUT
        saved_timeout_setting = _AUTO_TIMEOUT
        _AUTO_TIMEOUT = False
        greatest_duration = 0
        for track in self.graphic_tracks:
            track.static_time_out(self.toaStart)
            try:
                track_duration = (track.plays[-1].end - self.toaStart).total_seconds()
            except IndexError:
                track_duration = 0
            if track_duration > greatest_duration:
                greatest_duration = track_duration

        for track in self.video_tracks:
            track.static_time_out(self.toaStart)
            try:
                track_duration = (track.plays[-1].end - self.toaStart).total_seconds()
            except IndexError:
                track_duration = 0
            if track_duration > greatest_duration:
                greatest_duration = track_duration

        split = str(greatest_duration).split('.')
        seconds = int(split[0])
        microseconds = (int(float('0.' + split[1]) * 10 ** 6)
                        if len(split) > 1 else 0)

        self.toaDuration = toaTimecode.fromdatetime(
            (_YEAR_ZERO + timedelta(seconds=seconds, microseconds=microseconds)))
        _AUTO_TIMEOUT = saved_timeout_setting


class ChannelTrack():

    def __init__(self, id, name, master, slave=None):
        self.id = id
        self.name = name
        self.master = master
        self.slave = slave

    @classmethod
    def fromxml(cls, text):
        eletree = ElementTree.fromstring(text)
        id = eletree.find('identifier').text
        name = eletree.find('name').text
        master = eletree.find('master').text
        slave = eletree.find('slave').text

        return cls(id, name, master, slave)



class Track(Node):

    def __init__(self, *args, **kwargs):
        super(Track, self).__init__(*args, **kwargs)
        self.plays = JTList(nclass=5, parent_node=self)
        self.track_id = self.__getattr__('track_id')

    def _check_structure(self, element):
        good_atts = super(Track, self)._check_structure(element)
        good_ps = True
        for node in element.findall('node'):
            good_ps = good_ps and Play()._check_structure(node)

        return good_atts and good_ps

    def __getattr__(self, name):
        if name == 'track_id':
            return self.getroot().get('trackId') if self.getroot() is not None else None

        return super(Track, self).__getattr__(name)

    def __setattr__(self, name, value):
        if name == 'track_id':
            if self.getroot() is not None:
                self.getroot().set('trackId', value)

        super(Track, self).__setattr__(name, value)

    def static_time_out(self, start_at=None):
        global _AUTO_TIMEOUT
        saved_timeout_setting = _AUTO_TIMEOUT
        _AUTO_TIMEOUT = False
        if start_at:
            next_start = start_at
        else:
            try:
                next_start = self.plays[0].toaStart
            except IndexError:
                return
        for play in self.plays:
            play.toaStart = next_start
            next_start = play.end
        _AUTO_TIMEOUT = saved_timeout_setting

class GraphicTrack(Track):

    def __init__(self, *args, **kwargs):
        super(GraphicTrack, self).__init__(nclass=3, *args, **kwargs)

class VideoTrack(Track):

    def __init__(self, *args, **kwargs):
        super(VideoTrack, self).__init__(nclass=4, *args, **kwargs)


class Play(Node):

    def __init__(self, *args, **kwargs):
        super(Play, self).__init__(nclass=5, *args, **kwargs)
        self.triggers = JTList(nclass=6, parent_node=self)
        if self.getroot():
            resource = self.getroot().find('resource')
            self.resource = (int(resource.get('type')), get_text(resource))

    def __setattr__(self, name, value):
        if name != 'resource':
            super(Play, self).__setattr__(name, value)
        else:
            if self.getroot():
                resource = self.getroot().find('resource')
                resource.set('type', str(value[0]))
                if value[0] != 2:
                    set_text(resource, str(value[1]))
            self.__dict__['resource'] = value

    def _check_structure(self, element):
        good_atts = super(Play, self)._check_structure(element)
        good_trigs = True
        for node in element.findall('node'):
            good_trigs = good_trigs and Trigger()._check_structure(node)

        return good_atts and good_trigs

    def check_exists(self):
        #Check existence
        repo = (VIDEO_REPOSITORY if self.resource[0] == 0 else GRAPHICS_REPOSITORY) \
               if not self.resource[1].startswith('/') else ''
        path = repo + '/' + self.resource[1]
        if os.path.exists(path):
            return path
        else:
            return None


    def refresh(self, auto_update=True):
        """Check existence of resource file, set duration, fps etc.
        Note that this will set the duration back to the natural duration,
        the in point to the start and the outpoint to the end.
        """

        path = self.check_exists()


        media_info = MediaInfo.parse(path)
        media_info.to_data()

        # Check stats for videos
        if self.resource[0] == 0:
            try:
                aspect_ratio_map = {
                    '4:3': (1, 1440, 1080),
                    '16:9': (2, 1920, 1080),
                    '1.778': (2, 1920, 1080),
                    '1.85:1': (2, 1920, 1080),
                    None: (2, 1440, 1080)
                }

                self.toaAspectRatio = aspect_ratio_map[media_info.tracks[1].display_aspect_ratio][0]
                self.toaCodec = media_info.tracks[1].codec
                if self.resource[1].endswith('.mov'):
                    self.toaCodec = '1635148593'
                    self.toaCodecString = 'avc1'
                elif self.resource[1].endswith('mpg'):
                    self.toaCodec = '0'
                    self.toaCodecString = 'MPEG-2'

                # Keep out point relative to the end, just in case the duration changes.
                # It would be silly to leave the outpoint at the end of the old duration.
                outpoint_from_end = self.toaNaturalDuration - self.toaOutPoint
                duration = float(media_info.tracks[0].duration)
                seconds = duration / 1000
                self.toaNaturalDuration = int(seconds * FPS)
                self.toaOutPoint = toaNaturalDuration - outpoint_from_end

                # enforce toaInPoint <= toaOutPoint <= toaNaturalDuration
                if self.toaOutPoint > self.toaNaturalDuration:
                    self.toaOutPoint = self.toaNaturalDuration
                if self.toaInPoint > self.toaOutPoint:
                    self.toaInPoint = self.toaOutPoint
                self.toaDuration = toaTimecode.fromdatetime(
                    _YEAR_ZERO + (self.toaOutPoint - self.toaInPoint))

                if self.resource[1].endswith('.mpg'):
                    self.toaInvertFields = True
                    self.toaFieldOrder = 1
                elif self.resource[1].endswith('.mov'):
                    self.toaInvertFields = False
                    self.toaFieldOrder = 0

                self.toaAudioTracks = media_info.tracks[2].channel_s

                fps = {23.98: 0,
                       24.00: 1,
                       25.00: 2,
                       29.97: 3,
                       30.00: 4,
                       50.00: 5,
                       59.94: 6,
                       60.00: 7}
                try:
                    self.toaFrameRate = fps[round(float(media_info.tracks[1].frame_rate), 2)]
                except KeyError:
                    self.toaFrameRate = 8

                self.toaDisplayHeight = int(media_info.tracks[1].height)
                self.toaDisplayWidth = int(media_info.tracks[1].width)

            except:
                pass

        if auto_update and self.outstanding_updates:
            self.update()
            return False
        else:
            return self.outstanding_updates


class Trigger(Node):

    def __init__(self, *args, **kwargs):
        super(Trigger, self).__init__(nclass=6, *args, **kwargs)


class RTPlaylist(Node):

    def __init__(self, *args, **kwargs):
        super(RTPlaylist, self).__init__(nclass=7, *args, **kwargs)

class RTPlay(Node):

    def __init__(self, *args, **kwargs):
        super(RTPlay, self).__init__(nclass=8, *args, **kwargs)

#######################
# TOA Attribute Types #
#######################

class toaString(str):

    def __new__(self, text=None, *args, **kwargs):
        txt_pat = re.compile(r'\S')
        if re.match(txt_pat, text or ''):
            return str.__new__(toaString, text, *args, **kwargs)
        else:
            return str.__new__(toaString, *args, **kwargs)

    def __add__(self, other):
        return toaString(str(self) + other)

class toaInteger(int):

    def __new__(self, text=None, *args, **kwargs):
        txt_pat = re.compile(r'\S')
        if isinstance(text, str) and re.match(txt_pat, text or ''):
            try:
                return int.__new__(toaInteger, int(text), *args, **kwargs)
            except ValueError:
                return int.__new__(toaInteger, *args, **kwargs)
        elif text is None:
            return int.__new__(toaInteger, *args, **kwargs)
        else:
            return int.__new__(toaInteger, text, *args, **kwargs)


    def __add__(self, other):
        return toaInteger(int(self).__add__(other))

    def __sub__(self, other):
        return toaInteger(int(self).__sub__(other))

    def __mul__(self, other):
        return toaInteger(int(self).__mul__(other))

    def __floordiv__(self, other):
        return toaInteger(int(self).__floordiv__(other))

    def __mod__(self, other):
        return toaInteger(int(self).__mod__(other))

    def __divmod__(self, other):
        return toaInteger(int(self).__divmod__(other))

    def __pow__(self, other, modulo=None):
        return toaInteger(int(self).__pow__(other, modulo))

    def __lshift__(self, other):
        return toaInteger(int(self).__lshift__(other))

    def __rshift__(self, other):
        return toaInteger(int(self).__rshift__(other))

    def __and__(self, other):
        return toaInteger(int(self).__and__(other))

    def __xor__(self, other):
        return toaInteger(int(self).__xor__(other))

    def __or__(self, other):
        return toaInteger(int(self).__or__(other))


class toaDouble(float):

    def __new__(self, mini=None, maxi=None, text=None, *args, **kwargs):
        txt_pat = re.compile(r'\S')
        if re.match(txt_pat, text or ''):
            min_pat = re.compile(r'(<min>)(.+)(</min>)')
            max_pat = re.compile(r'(<max>)(.+)(</max>)')
            val_pat = re.compile(r'(<value>)(.+)(</value>)')
            for mat in re.findall(min_pat, text):
                try:
                    self.mini = float(mat[1])
                    break
                except ValueError:
                    continue
            for mat in re.findall(max_pat, text):
                try:
                    self.maxi = float(mat[1])
                    break
                except ValueError:
                    continue
            for mat in re.findall(val_pat, text):
                try:
                    return float.__new__(toaDouble, float(mat[1]), *args, **kwargs)
                except ValueError:
                    continue

            flt_pat = re.compile(r'(>)(.+)(<)')

            nums = re.findall(flt_pat, text)
            if nums:
                try:
                    return float.__new__(toaDouble, float(nums[0][1]), *args, **kwargs)
                except ValueError:
                    pass

            self.mini = mini
            self.maxi = maxi
            return float.__new__(toaDouble, *args, **kwargs)
        else:
            self.mini = mini
            self.maxi = maxi
            return float.__new__(toaDouble, *args, **kwargs)


    def __str__(self):
        text = ''
        if self.mini:
            text += '<min>' + '{0:.1f}'.format(self.mini) + '</min>'
        if self.maxi:
            text += '<max>' + '{0:.1f}'.format(self.maxi) + '</max>'
        value = str(super(toaDouble, self).__str__())
        if self.mini or self.maxi:
            return text + '<value>' + '{0:.1f}'.format(float(value)) + '</value>'

        return value

    def __add__(self, other):
        return toaDouble(float(self).__add__(other))

    def __sub__(self, other):
        return toaDouble(float(self).__sub__(other))

    def __mul__(self, other):
        return toaDouble(float(self).__mul__(other))

    def __floordiv__(self, other):
        return toaDouble(float(self).__floordiv__(other))

    def __mod__(self, other):
        return toaDouble(float(self).__mod__(other))

    def __divmod__(self, other):
        return toaDouble(float(self).__divmod__(other))

    def __pow__(self, other, modulo=None):
        return toaDouble(float(self).__pow__(other, modulo))

    def __lshift__(self, other):
        return toaDouble(float(self).__lshift__(other))

    def __rshift__(self, other):
        return toaDouble(float(self).__rshift__(other))

    def __and__(self, other):
        return toaDouble(float(self).__and__(other))

    def __xor__(self, other):
        return toaDouble(float(self).__xor__(other))

    def __or__(self, other):
        return toaDouble(float(self).__or__(other))

class toaBool(int):

    def __new__(self, text=None, *args, **kwargs):
        txt_pat = re.compile(r'\S')
        if re.match(txt_pat, text or ''):
            return int.__new__(toaBool, True if text[0] == 'T' else False, *args, **kwargs)
        else:
            return int.__new__(toaBool, *args, **kwargs)

    def __nonzero(self):
        return self

    def __str__(self):
        return 'T' if self else 'F'


class toaIndex(int):

    def __new__(self, values=None, maxi=None, text=None, *args, **kwargs):
        self.maxi = maxi
        self.values = values
        txt_pat = re.compile(r'\S')
        if re.match(txt_pat, text or ''):
            vals_pat = re.compile(r'(<values>)(.+)(</values>)')
            max_pat = re.compile(r'(<max>)(.+)(</max>)')
            val_pat = re.compile(r'(<value>)(.+)(</value>)')
            for mat in re.findall(vals_pat, text):
                str_pat = re.compile(r'(<string>)(.+)(</string>)')
                self.values = []
                for str_mat in re.findall(str_pat, mat[1]):
                    self.values.append(str_mat[1])
                break
            for mat in re.findall(max_pat, text):
                self.maxi = int(mat[1])
                break
            for mat in re.findall(val_pat, text):
                if self.values:
                    super(toaIndex, self).__init__(int(mat[1]), *args, **kwargs)
                    return
                else:
                    raise Exception('toaIndex missing values')
            try:
                return int.__new__(toaIndex, int(text), *args, **kwargs)
            except ValueError:
                return int.__new__(toaIndex, *args, **kwargs)
        else:
            return int.__new__(toaIndex, *args, **kwargs)

    def __str__(self):
        text = ''
        value = super(toaIndex, self).__str__()
        if self.maxi or self.values:
            if self.values:
                text += '<values>'
                text.join(['<string>' + '{0:.1f}'.format(v) + '</string>'
                           for v in self.values])
                text += '</values>'
            if self.maxi:
                text += '<max>' + '{0:.1f}'.format(self.maxi) + '</max>'
            return text + '<value>' + value + '</value>'
        else:
            return value

    def __add__(self, other):
        return toaIndex(int(self).__add__(other))

    def __sub__(self, other):
        return toaIndex(int(self).__sub__(other))

    def __mul__(self, other):
        return toaIndex(int(self).__mul__(other))

    def __floordiv__(self, other):
        return toaIndex(int(self).__floordiv__(other))

    def __mod__(self, other):
        return toaIndex(int(self).__mod__(other))

    def __divmod__(self, other):
        return toaIndex(int(self).__divmod__(other))

    def __pow__(self, other, modulo=None):
        return toaIndex(int(self).__pow__(other, modulo))

    def __lshift__(self, other):
        return toaIndex(int(self).__lshift__(other))

    def __rshift__(self, other):
        return toaIndex(int(self).__rshift__(other))

    def __and__(self, other):
        return toaIndex(int(self).__and__(other))

    def __xor__(self, other):
        return toaIndex(int(self).__xor__(other))

    def __or__(self, other):
        return toaIndex(int(self).__or__(other))


class toaDictionary(): pass

class toaArray(list):

    def __init__(self, atype=None, text=None, *args, **kwargs):
        self.atype = atype
        txt_pat = re.compile(r'\S')
        if re.match(txt_pat, text or ''):
            arr_pat = re.compile(r'(<array>)(.+)(</array>)')
            for mat in re.findall(arr_pat, text):
                dub_pat = re.compile(r'(<double>)(.+)(</double>)')
                tim_pat = re.compile(r'(<timecode>)(.+)(</timecode>)')
                self.values = []
                for dub_mat in re.findall(dub_pat, mat[1]):
                    self.values.append(float(dub_mat[1]))
                if self.values:
                    self.atype = toaDouble
                    break
                for tim_mat in re.findall(tim_pat, mat[1]):
                    self.values.append(toaTimecode(text=tim_mat[1]))
                if self.values:
                    self.atype = toaTimecode
                else:
                    self.atype = None
        else:
            super(toaArray, self).__init__(*args, **kwargs)

    def __str__(self):
        if self.atype:
            tag = 'double' if self.atype == toaDouble else 'timecode'
            return '<array>'.join(['<' + tag + '>' + '{0:.1f}'.format(v) + '</' + tag + '>'
                                   for v in self.values]) + '</array>'

        return ''

class toaTimecode(datetime):

    def __new__(cls, text=None, *args, **kwargs):
        if text == 'None':
            return
        txt_pat = re.compile(r'\S')
        if re.match(txt_pat, text or ''):
            try:
                dt = datetime.strptime(text, '%Y-%m-%d %H:%M:%S.%f')
                return datetime.__new__(
                    toaTimecode, year=dt.year, month=dt.month, day=dt.day,
                    hour=dt.hour, minute=dt.minute, second=dt.second,
                    microsecond=dt.microsecond)
            except ValueError:
                pass
            try:
                tm = time.strptime(text, '%H:%M:%S.%f')
                return datetime.__new__(
                    toaTimecode, year=_MIN_YEAR, month=1, day=1,
                    hour=tm.hour, minute=tm.minute, second=tm.second,
                    microsecond=tm.microsecond)
            except ValueError:
                pass
            try:
                dt = datetime.strptime(text, '%Y-%m-%d %H:%M:%S')
                return datetime.__new__(
                    toaTimecode, year=dt.year, month=dt.month, day=dt.day,
                    hour=dt.hour, minute=dt.minute, second=dt.second,
                    microsecond=dt.microsecond)
            except ValueError:
                pass
            split = str(text).split(' ')
            if len(split) == 2:
                date = split[0]
                frames = split[1]
                day = int(date[:2].rstrip('.'))
                date = date[2:].lstrip('.')

                month = int(date[:2].rstrip('.'))
                date = date[2:].lstrip('.')

                year = int(date[:4])

                seconds = float(frames) / FPS
                small_units = str(seconds).split('.')
                total_seconds = int(small_units[0])
                microseconds = (int(float('0.' + small_units[1]) * 10 ** 6)
                                if len(small_units) > 1 else 0)

                dt = datetime(year=year, month=month, day=day)
                dt += timedelta(seconds=total_seconds,
                                microseconds=microseconds)

                return datetime.__new__(
                    toaTimecode, year=dt.year, month=dt.month, day=dt.day,
                    hour=dt.hour, minute=dt.minute, second=dt.second,
                    microsecond=dt.microsecond)

            if split:
                seconds = float(split[0]) / FPS
                small_units = str(seconds).split('.')
                total_seconds = int(small_units[0])
                microseconds = (int(float('0.' + small_units[1]) * 10 ** 6)
                                if len(small_units) > 1 else 0)
                dt = _YEAR_ZERO + timedelta(seconds=total_seconds, microseconds=microseconds)

                return datetime.__new__(
                    toaTimecode, year=dt.year, month=dt.month,
                    day=dt.day, hour=dt.hour, minute=dt.minute,
                    second=dt.second, microsecond=dt.microsecond)

        if not args and not kwargs:
            return datetime.__new__(toaTimecode, year=_MIN_YEAR, month=1, day=1)

        return datetime.__new__(toaTimecode, *args, **kwargs)

    @classmethod
    def fromdatetime(cls, dt):
        return cls(year=dt.year, month=dt.month, day=dt.day, hour=dt.hour,
                   minute=dt.minute, second=dt.second,
                   microsecond=dt.microsecond, tzinfo=dt.tzinfo)

    def todatetime(self):
        return datetime(year=self.year, month=self.month, day=self.day,
                        hour=self.hour, minute=self.minute, second=self.second,
                        microsecond=self.microsecond, tzinfo=self.tzinfo)


    def __add__(self, other):
        if isinstance(other, timedelta):
            return self.fromdatetime(super(toaTimecode, self).__add__(other))

        return super(toaTimecode, self).__add__(other)

    def __sub__(self, other):
        if isinstance(other, timedelta):
            return self.fromdatetime(super(toaTimecode, self).__sub__(other))

        return super(toaTimecode, self).__sub__(other)

    #IMPLEMENT OTHER DATETIME ARITHMETIC OPERATIONS

    def __str__(self):
        # Don't check against the full date of year zero, just the year,
        # since the rest of the time is stored in the other values
        if self.year == _MIN_YEAR:
            seconds = self.hour * 60 * 60 + self.minute * 60 + self.second
            return str((seconds + float(self.microsecond) / 10 ** 6) * FPS)

        day = str(self.day)[:1] if int(self.day) < 10 else str(self.day)
        month = str(self.month)[:1] if int(self.month) < 10 else str(self.month)
        seconds = self.hour * 60 * 60 + self.minute * 60 + self.second
        frames = str((seconds + float(self.microsecond) / 10 ** 6) * FPS)

        return day + '.' + month + '.' + str(self.year) + ' ' + str(frames)


class toaColor():

    def __init__(self, hexa=None, red=0.0, green=0.0, blue=0.0, alpha=0.0, text=None):
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha
        txt_pat = re.compile(r'\S')
        if re.match(txt_pat, text or ''):
            if text[0] == '#':
                hexa = text
            else:
                num_pat = re.compile(r'\d+\.\d+')
                num_mat = re.findall(num_pat, text)
                if num_mat:
                    self.red = float(num_mat[0])
                    self.green = float(num_mat[1])
                    self.blue = float(num_mat[2])
                    self.alpha = float(num_mat[3])
                    return
        if hexa:
            if len(hexa) >= 3:
                self.red = float(hex_to_int(hexa[1:3]))
            if len(hexa) >= 5:
                self.green = float(hex_to_int(hexa[3:5]))
            if len(hexa) >= 7:
                self.blue = float(hex_to_int(hexa[5:7]))
            if len(hexa) >= 9:
                self.alpha = float(hex_to_int(hexa[7:9]))



    def __str__(self):
        hexa = '#' + (int_to_hex(int(self.red)) +
                      int_to_hex(int(self.green)) +
                      int_to_hex(int(self.blue)) +
                      int_to_hex(int(self.alpha)))
        if ('00000000' + hexa[1:])[-8:] == '00000000':
            return '#00'
        else:
            return hexa

##################
# Helper classes #
##################

class JTList():
    """A list structure used to model a set of sub nodes. This acts
    similar to a normal list, but it is always tied to a node and
    manipulates the underlying xml.
    """

    def __init__(self, nclass, parent_node, *args):
        self._index = 0
        if parent_node is None:
            raise Exception('JTList must have a parent')
        if nclass is None:
            raise Exception('JTList must have an nclass')
        self.nclass = nclass
        self.parent_node = parent_node
        for node in args:
            self.append(node)

    def tolist(self):
        return [x for x in self]

    @classmethod
    def fromlist(cls, nodes, nclass, parent_node):
        ls = cls(nclass, parent_node)
        for node in nodes:
            ls.append(node)
        return ls

    def __len__(self):
        return len(self.parent_node.findall_by_property('class', self.nclass))

    def __getitem__(self, key):
        i = 0
        nodes = self.parent_node.findall_by_property('class', self.nclass)
        key = key if key >= 0 else len(nodes) + key
        for node in nodes:
            if i == key:
                return classes[int(self.nclass)](element=node,
                                                 parent_node=self.parent_node)
            i += 1
        raise IndexError

    def check_start(self, item, parent):
        """Check that the given item starts on the same day
        as the JTList's parent node.
        """

        if (item and parent and parent.toaStart and item.toaStart) and \
            not (item.toaStart.year == parent.toaStart.year and
                 item.toaStart.month == parent.toaStart.month and
                 item.toaStart.day == parent.toaStart.day):
            raise ValueError('day of ' + str(item.nid) + ' must match day of '
                             'parent node ' + str(parent.nid) +
                             '(toaStart: ' + str(parent.toaStart) + ')')

    def __setitem__(self, key, value):
        self.check_start(value, self.parent_node if self.parent_node.toaStart
                         else self.parent_node.parent_node)
        root = self.parent_node.getroot()
        if root is not None:
            del root[key]
            root[key] = value.getroot()
        self.parent_node.time_out()

    def append(self, item):
        root = self.parent_node.getroot()
        if root is not None:
            try:
                self.check_start(item, self.parent_node if self.parent_node.toaStart
                                 else self.parent_node.parent_node)
            except ValueError:
                raise
            else:
                root.append(item.getroot())
                item.parent_node = self.parent_node
                self.parent_node.time_out()


    def remove(self, item):
        root = self.parent_node.getroot()
        if root is not None:
            i = 0
            for node in self.parent_node.findall_by_property('class', self.nclass):
                if node.get('id') == str(item.nid):
                    root.remove(node)
                    item.parent_node = None
                    self.parent_node.time_out()
                    return
                i += 1


    def extend(self, jt_list):
        if jt_list:
            if jt_list.nclass != self.nclass:
                raise TypeError(
                    'extending list must have same nclass as this list')
            for e in jt_list:
                self.append(e)

    def insert(self, key, value):
        pass

    def pop(self, i=-1):
        x = self[i]
        self.remove(i)
        return x

    def reverse(self):
        current_length = len(self)
        for i in xrange(current_length - 2, 0):
            self.append(self[i])

        for i in xrange(0, current_length - 2):
            del self[i]



    def sort(self):
        pass

    def __add__(self, jt_list):
        new_list = JTList(nclass=self.nclass, parent_node=self.parent_node)
        new_list.extend(jt_list)
        return new_list



    def __radd__(self, other):
        pass

    def __iadd__(self, other):
        pass

    def __mul__(self, other):
        pass

    def __rmul__(self, other):
        pass

    def __imul__(self, other):
        pass

    def __contains__(self, item):
        for node in self:
            if node.nid == item.nid and node.nclass == item.nclass:
                return True
        return False

    def index(self, item):
        i = 0
        for node in self:
            if node.nid == item.nid and node.nclass == item.nclass:
                return i
            i += 1
        raise ValueError(str(item.nid) + ' is not in list')

    def count(self, item):
        i = 0
        for node in self:
            if node.nid == item.nid and node.nclass == item.nclass:
                i += 1
        return i

    def __delitem__(self, key):
        self.remove(self[key])

    def clear(self):
        root = self.parent_node.getroot()
        if root is not None:
            nodes = [n for n in self.parent_node.findall_by_property('class', self.nclass)]
            for node in nodes:
                root.remove(node)

        self.parent_node.time_out()

    def __repr__(self):
        if self:
            return '[' + ''.join([(str(n.nid) or "''") + ', ' for n in self])[:-2] + ']'
        else:
            return '[]'


####################
# Helper functions #
####################


def get_text(elem):
    """Get the xml text of a node, but formatted correctly"""

    # See if this is a double
    min_text = ''
    max_text = ''
    val_text = ''
    min_node = elem.find('min')
    if min_node is not None:
        min_text = ascii(min_node.text)
    max_node = elem.find('max')
    if max_node is not None:
        max_text = ascii(max_node.text)
    value_node = elem.find('value')
    if value_node is not None:
        val_text = ascii(value_node.text)

    if min_text and max_text and val_text:
        return ('<min>' + min_text + '</min>' +
                '<max>' + max_text + '</max>' +
                '<value>' + val_text + '</value>')

    return ascii(elem.text)

def ascii(text):
    """Convert text to ascii-only characters"""

    try:
        return ''.join(i if ord(i) < 128 else '' for i in text)
    except:
        return str(text)

def set_text(elem, text):
    """Set the xml text of a node, but format it correctly"""

    min_pat = re.compile(r'(<min>)(.+)(</min>)')
    max_pat = re.compile(r'(<max>)(.+)(</max>)')
    val_pat = re.compile(r'(<value>)(.+)(</value>)')
    min_txt = ''
    max_txt = ''
    val_txt = ''
    for mat in re.findall(min_pat, text):
        min_txt = mat[1]
        break
    for mat in re.findall(max_pat, text):
        max_txt = mat[1]
        break
    for mat in re.findall(val_pat, text):
        val_txt = mat[1]
        break

    if min_txt or max_txt or val_txt:
        min_elem = elem.find('min') or ElementTree.Element('min')
        if min_txt:
            min_elem.text = min_txt
            if elem.find('min') is None:
                elem.append(min_elem)
        else:
            try:
                elem.remove(min_elem)
            except:
                pass
        max_elem = elem.find('max') or ElementTree.Element('max')
        if max_txt:
            max_elem.text = max_txt
            if elem.find('max') is None:
                elem.append(max_elem)
        else:
            try:
                elem.remove(max_elem)
            except:
                pass
        val_elem = elem.find('value') or ElementTree.Element('value')
        if val_txt:
            val_elem.text = val_txt
            if elem.find('value') is None:
                elem.append(val_elem)
        else:
            try:
                elem.remove(val_elem)
            except:
                pass
    else:
        to_remove = [sub for sub in list(elem)]
        for sub in to_remove:
            elem.remove(sub)
        elem.text = str(text)

def hex_to_int(hexa):
    """Convert a hexadecimal string to an int"""

    vals = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}
    num = 0
    power = 0
    for d in hexa[::-1]:
        try:
            num += int(d) * 16 ** power
        except ValueError:
            num += vals[d] * 16 ** power
        power += 1

    return num


def int_to_hex(num):
    """Convert an int to a hexadecimal string"""
    num = int(num)
    vals = { 10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}
    if num < 0:
        sign = '-'
        num = -num
    else:
        sign = ''
    if num < 10:
        return sign + str(num)
    if num < 16:
        return sign + vals[num]

    return sign + int_to_hex(num / 16) + int_to_hex(num % 16)


###########
# Lookups #
###########

_YEAR_ZERO = datetime(_MIN_YEAR, 1, 1, 0, 0, 0, 0)

classes = {1: Day,
           2: Playlist,
           3: GraphicTrack,
           4: VideoTrack,
           5: Play,
           6: Trigger,
           7: RTPlaylist,
           8: RTPlay}

att_types = {0: toaString,
             1: toaInteger,
             2: toaDouble,
             3: toaBool,
             4: toaIndex,
             5: toaDictionary,
             6: toaArray,
             7: toaTimecode,
             8: toaColor}

resource_types = {0: 'QuickTime Movie',
                  1: 'Composition Builder / Quartz Composer Graphic',
                  2: 'Live Input',
                  3: 'Image',
                  4: 'Graphic Movie',
                  5: 'Gap',
                  6: 'JavaScript Event',
                  7: 'Graphic based on TOA graphic template',
                  8: 'Graphic Movie based on TOA graphic template',
                  9: 'Placeholder',
                  10: 'Audio',
                  11: 'Workflow'}

