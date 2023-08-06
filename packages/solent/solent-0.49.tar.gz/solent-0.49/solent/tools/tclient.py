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
#
# // overview
# Simple tcp client tool. You could think of it as being similar to netcat.
# The motive for writing it is that I do not have something to hand on
# Windows, and I'm working through the engine scenarios for that platform.
# For the moment I'm just hard-coding it to pygame. If you're in unix,
# you probably have something else handy.

from solent import Engine
from solent import hexdump_bytes
from solent import log
from solent import init_network_logging
from solent import solent_cpair
from solent import solent_keycode
from solent import SolentQuitException
from solent import RailLineFinder
from solent.util import SpinSelectionUi

import sys
import time
import traceback


# --------------------------------------------------------
#   model
# --------------------------------------------------------
I_NEARCAST_SCHEMA = '''
    i message h
        i field h

    message init
        field addr
        field port

    message net_connect
    message net_condrop
        field message
    message net_recv
        field bb
    message net_send
        field bb
'''

QUIT_KEYCODES = (
    solent_keycode('etx'),
    solent_keycode('dc1'))

#CONSOLE_TYPE = 'pygame'
CONSOLE_TYPE = 'curses'
CONSOLE_WIDTH = 78
CONSOLE_HEIGHT = 24

if CONSOLE_TYPE == 'curses':
    from solent.console.curses import curses_async_get_keycode

class CogTcpClient:
    def __init__(self, cog_h, orb, engine):
        self.cog_h = cog_h
        self.orb = orb
        self.engine = engine
        #
        self.client_sid = None
    def orb_close(self):
        if None != self.client_sid:
            self.engine.close_tcp_client(
                client_sid=self.client_sid)
    #
    def on_init(self, addr, port):
        self.engine.open_tcp_client(
            addr=addr,
            port=port,
            cb_tcp_client_connect=self.cb_tcp_client_connect,
            cb_tcp_client_condrop=self.cb_tcp_client_condrop,
            cb_tcp_client_recv=self.cb_tcp_client_recv)
    def on_net_send(self, bb):
        self.engine.send(
            sid=self.client_sid,
            bb=bb)
    #
    def cb_tcp_client_connect(self, cs_tcp_client_connect):
        engine = cs_tcp_client_connect.engine
        client_sid = cs_tcp_client_connect.client_sid
        addr = cs_tcp_client_connect.addr
        port = cs_tcp_client_connect.port
        #
        self.client_sid = client_sid
        self.nearcast.net_connect()
    def cb_tcp_client_condrop(self, cs_tcp_client_condrop):
        engine = cs_tcp_client_condrop.engine
        client_sid = cs_tcp_client_condrop.client_sid
        message = cs_tcp_client_condrop.message
        #
        self.client_sid = None
        self.nearcast.net_condrop(
            message=message)
    def cb_tcp_client_recv(self, cs_tcp_client_recv):
        engine = cs_tcp_client_recv.engine
        client_sid = cs_tcp_client_recv.client_sid
        bb = cs_tcp_client_recv.bb
        #
        self.nearcast.net_recv(
            bb=bb)

class CogTerm:
    def __init__(self, cog_h, orb, engine):
        self.cog_h = cog_h
        self.orb = orb
        self.engine = engine
        #
        self.spin_term = None
        self.rail_line_finder = None
        self.drop = None
        self.rest = None
    #
    def on_init(self, addr, port):
        if CONSOLE_TYPE == 'curses':
            log('yes')
            # We deliberately set this high, because we are only waiting on things
            # that are selectable (network and stdin). We would not want to
            # implement this with pygame as the ui, because that does not use file
            # decriptors for input.
            self.engine.set_default_timeout(2.0)
            self.engine.add_custom_fd_read(
                cfd_h='curses',
                fd=sys.stdin,
                cb_eng_custom_fd_read=self.cb_eng_custom_fd_read)
        else:
            log('no')
        #
        self.spin_term = self.engine.init_spin(
            construct=SpinSelectionUi,
            console_type=CONSOLE_TYPE,
            cb_selui_keycode=self.cb_selui_keycode,
            cb_selui_lselect=self.cb_selui_lselect)
        self.spin_term.open_console(
            width=CONSOLE_WIDTH,
            height=CONSOLE_HEIGHT)
        self.drop = 0
        self.rest = 0
        self.spin_term.refresh_console()
    def on_net_connect(self):
        self.rail_line_finder = RailLineFinder()
        self.rail_line_finder.zero(
            rail_h='line_finder.only',
            cb_line_finder_event=self.cb_line_finder_event)
        #
        self.spin_term.clear()
        self.spin_term.write(
            drop=0,
            rest=0,
            s='Connected',
            cpair=solent_cpair('red'))
        self.drop = 1
        self.rest = 0
        self.spin_term.refresh_console()
    def on_net_condrop(self, message):
        self.rail_line_finder = None
        #
        self.spin_term.clear()
        self.spin_term.write(
            drop=0,
            rest=0,
            s=message,
            cpair=solent_cpair('red'))
        self.drop = 1
        self.rest = 0
        self.spin_term.refresh_console()
    def on_net_recv(self, bb):
        hexdump_bytes(bb)
        for keycode in bb:
            self._print(
                keycode=keycode,
                cpair=solent_cpair('grey'))
        self.spin_term.refresh_console()
    #
    def cb_eng_custom_fd_read(self, cs_eng_custom_fd_read):
        cfd_h = cs_eng_custom_fd_read.cfd_h
        fd = cs_eng_custom_fd_read.fd
        #
        if cfd_h == 'curses':
            keycode = curses_async_get_keycode()
        else:
            raise Exception("Not sure what to do this (%s)."%(cfd_h))
        #
        self._received_keycode(
            keycode=keycode)
    def cb_selui_keycode(self, cs_selui_keycode):
        keycode = cs_selui_keycode.keycode
        #
        self._received_keycode(
            keycode=keycode)
    def cb_selui_lselect(self, cs_selui_lselect):
        # This will never be called in curses mode, because the term is
        # subverted by the custom fd we are registering with the engine.
        drop = cs_selui_lselect.drop
        rest = cs_selui_lselect.rest
        c = cs_selui_lselect.c
        cpair = cs_selui_lselect.cpair
        #
        pass
    def cb_line_finder_event(self, cs_line_finder_event):
        rail_h = cs_line_finder_event.rail_h
        line = cs_line_finder_event.msg
        #
        self.nearcast.net_send(
            bb=bytes('%s\n'%line, 'utf8'))
    #
    def _received_keycode(self, keycode):
        if keycode in QUIT_KEYCODES:
            raise SolentQuitException()
        #
        if None == self.rail_line_finder:
            return
        #
        cpair = solent_cpair('orange')
        # This backspace mechanism is far from perfect.
        if keycode == solent_keycode('backspace'):
            self.rail_line_finder.backspace()
            s = self.rail_line_finder.get()
            idx = len(s)%CONSOLE_WIDTH
            s = s[-1*idx:]
            self.spin_term.write(
                drop=self.drop,
                rest=0,
                s='%s '%s,
                cpair=cpair)
            self.rest = len(s)
        else:
            self.rail_line_finder.accept_bytes([keycode])
            self._print(
                keycode=keycode,
                cpair=cpair)
        self.spin_term.refresh_console()
    def _print(self, keycode, cpair):
        if keycode == solent_keycode('backspace') and self.rest > 0:
            self.rest -= 1
            self.spin_term.write(
                drop=self.drop,
                rest=self.rest,
                s=' ',
                cpair=cpair)
            return
        if keycode == solent_keycode('newline'):
            self.rest = 0
            self.drop += 1
        else:
            self.spin_term.write(
                drop=self.drop,
                rest=self.rest,
                s=chr(keycode),
                cpair=cpair)
            self.rest += 1
        if self.rest == CONSOLE_WIDTH:
            self.rest = 0
            self.drop += 1
        while self.drop >= CONSOLE_HEIGHT:
            self.spin_term.scroll()
            self.drop -= 1

def init_nearcast(engine, net_addr, net_port):
    orb = engine.init_orb(
        i_nearcast=I_NEARCAST_SCHEMA)
    orb.add_log_snoop()
    orb.init_cog(CogTcpClient)
    orb.init_cog(CogTerm)
    #
    bridge = orb.init_autobridge()
    bridge.nearcast.init(
        addr=net_addr,
        port=net_port)
    #
    return bridge


# --------------------------------------------------------
#   launch
# --------------------------------------------------------
MTU = 1492

def usage():
    print('Usage:')
    print('  %s addr port'%sys.argv[0])
    sys.exit(1)

def main():
    if 3 != len(sys.argv):
        usage()
    #
    engine = Engine(
        mtu=MTU)
    try:
        net_addr = sys.argv[1]
        net_port = int(sys.argv[2])
        #
        init_nearcast(
            engine=engine,
            net_addr=net_addr,
            net_port=net_port)
        engine.event_loop()
    except KeyboardInterrupt:
        pass
    except SolentQuitException:
        pass
    except:
        traceback.print_exc()
    finally:
        engine.close()

if __name__ == '__main__':
    main()



