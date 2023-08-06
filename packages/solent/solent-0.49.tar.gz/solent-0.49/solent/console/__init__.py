# // license
# Copyright 2016, Free Software Foundation.
#
# This file is part of Solent.
#
# Solent is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# Solent is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# Solent. If not, see <http://www.gnu.org/licenses/>.

from .iconsole import iconsole_new
from .keystream import keystream_new

from .cgrid import Cgrid

from .rail_menu import RailMenu

import enum

class e_boxtype(enum.Enum):
    line          = 2000
    edge          = 2001
    void          = 2002
    hash          = 2003
    stop          = 2004

CONSOLE_TYPE_ANDROID = 'android'
CONSOLE_TYPE_APPLE = 'apple_ios'
CONSOLE_TYPE_CURSES = 'curses'
CONSOLE_TYPE_HAIKU = 'haiku'
CONSOLE_TYPE_PYGAME = 'pygame'
CONSOLE_TYPE_WAYLAND = 'wayland'
CONSOLE_TYPE_WINDOWS = 'windows'
CONSOLE_TYPE_WSOCKET = 'websockets'

# This is a function masquerading as an object. It constructs an
# object internally. The reason for this design is that it makes it
# easy to switch apps between pygame/curses/etc through changing only
# a string within the user's code.
def Console(console_type, height, width, **kwargs):
    '''
    Import the console type you want to use from the package. e.g.
    CONSOLE_TYPE_CURSES. This mechanism allows us the codebase to run even if
    some dependencies are missing. For example, you want to be able to run
    apps on windows (where curses is not available). And you want to be able
    to run curses mode, even when pygame isn't installed.
    '''
    if console_type == CONSOLE_TYPE_ANDROID:
        raise Exception("Not yet implemented.")
    elif console_type == CONSOLE_TYPE_APPLE:
        raise Exception("Not yet implemented.")
    elif console_type == CONSOLE_TYPE_CURSES:
        import solent.console.curses as m
        return m.create(
            width=width,
            height=height)
    elif console_type == CONSOLE_TYPE_PYGAME:
        import solent.console.pygame as m
        return m.create(
            width=width,
            height=height)
    elif console_type == CONSOLE_TYPE_WAYLAND:
        raise Exception("Not yet implemented.")
    elif console_type == CONSOLE_TYPE_WINDOWS:
        import solent.console.windows as m
        return m.console_new(
            width=width,
            height=height)
        raise Exception("Not yet implemented.")
    elif console_type == CONSOLE_TYPE_WSOCKET:
        raise Exception("Not yet implemented.")
    else:
        raise Exception("Unrecognised console type [%s]"%(console_type))

