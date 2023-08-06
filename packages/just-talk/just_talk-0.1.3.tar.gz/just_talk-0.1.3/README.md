## Author ##
Matthew Rademaker

matthew@acctv.com.au

## Context ##
To provide a python model of the Tools On Air Broadcast API For use with the Tools On Air suite of programs.

## Usage ##
The three pieces of functionality that make your life easier are:
 1. Child nodes can be accessed as a list e.g. a_day.playlists, a_playlist.video_tracks
 2. Adding a Playlist to a Day, a Track to a Playlist, or a Play to a Track will timeout EVERYTHING
    in the model - it will search up the tree as far as it can and time everything out. Slow, yes,
    but do you want to do it yourself? Do you want it to NOT be timed out properly?
 3. Changing the start or duration of a play or playlist will automatically calculate a field called
    'end'

One quirk of implementation (which may be fixed in the future) is that only data stored in the actual
underlying xml will persist. For example, if you have a Day object, and do the following:
    Day.playlists[0].new_field = 'test'
    
Then try this:
    print Day.playlists[0].new_field
    
The result will be blank. This is because all gets and sets are interacting with the underlying xml,
NOT with the python object. Objects and attributes in the model are created each time they are
accessed from the xml itself, and the xml is created from a template file stored in the xml folder
in the just_talk package. These xml files correspond to the Just:Talk implementation, and only
fields in there will be accepted by Just:Talk, so it is probably a good thing that new fields can't
be added.

## Design ##
The just_talk package has low-level communications for connecting to the playout system (comms.py),
functions to call the various messages (messages.py) and a model of all the data types and objects
used by the playout system, specifically Just:Play (model.py).

Most of the complexity is in just_talk.model. Just:Talk objects (days, playlists etc.) are classes,
all deriving from a 'Node', which in turn is an xml object, since Just:Talk uses xml for its playlists.
