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

from solent import Engine
from solent import log
from solent import ns
from solent import solent_cpair
from solent import solent_keycode
from solent import SolentQuitException
from solent import uniq
from solent.console import Cgrid
from solent.console import RailMenu
from solent.util import SpinSelectionUi

from collections import deque
import os
import random
import sys
import time
import traceback


# --------------------------------------------------------
#   :game
# --------------------------------------------------------
APP_NAME = 'draw'

def create_spot(drop, rest):
    return (drop, rest)

class RailDrawSurface:
    def __init__(self):
        self.cs_draw_surface_clear = ns()
        self.cs_draw_surface_write = ns()
        #
        self.b_started = False
    def call_draw_surface_clear(self, rail_h):
        self.cs_draw_surface_clear.rail_h = rail_h
        self.cb_draw_surface_clear(
            cs_draw_surface_clear=self.cs_draw_surface_clear)
    def call_draw_surface_write(self, rail_h, drop, rest, s, cpair):
        self.cs_draw_surface_write.rail_h = rail_h
        self.cs_draw_surface_write.drop = drop
        self.cs_draw_surface_write.rest = rest
        self.cs_draw_surface_write.s = s
        self.cs_draw_surface_write.cpair = cpair
        self.cb_draw_surface_write(
            cs_draw_surface_write=self.cs_draw_surface_write)
    def zero(self, rail_h, height, width, cb_draw_surface_clear, cb_draw_surface_write):
        self.rail_h = rail_h
        self.height = height
        self.width = width
        self.cb_draw_surface_clear = cb_draw_surface_clear
        self.cb_draw_surface_write = cb_draw_surface_write
        #
        self.b_started = True
        #
        self.spots = []
    def tick(self):
        pass
    def render(self):
        self.call_draw_surface_clear(
            rail_h=self.rail_h)
        for spot in self.spots:
            (drop, rest) = spot
            self.call_draw_surface_write(
                rail_h=self.rail_h,
                drop=drop,
                rest=rest,
                s='@',
                cpair=solent_cpair('yellow'))
    def flip(self, drop, rest):
        spot = create_spot(drop, rest)
        if spot in self.spots:
            self.spots.remove(spot)
        else:
            self.spots.append(spot)


# --------------------------------------------------------
#   :containment
# --------------------------------------------------------
#
# Containment consists of a menu system, a terminal, and a cog that
# encapsulates the game.
#
I_CONTAINMENT_NEARCAST_SCHEMA = '''
    i message h
        i field h

    message prime_console
        field console_type
        field height
        field width
    message init

    message quit

    message keystroke
        field keycode
    message tselect
        # mouse or gollop selection from the term
        field drop
        field rest

    message game_focus
    message game_new
    message game_input
        field keycode
    message game_plot
        field drop
        field rest

    message term_clear
    message term_write
        field drop
        field rest
        field s
        field cpair

    message menu_focus
    message menu_title
        field text
    message menu_item
        field menu_keycode
        field text
    message menu_select
        field menu_keycode
'''

class TrackPrimeConsole:
    def __init__(self, orb):
        self.orb = orb
    def on_prime_console(self, console_type, height, width):
        self.console_type = console_type
        self.height = height
        self.width = width

MENU_KEYCODE_NEW_GAME = solent_keycode('n')
MENU_KEYCODE_CONTINUE = solent_keycode('c')
MENU_KEYCODE_QUIT = solent_keycode('q')

def t100():
    return time.time() * 100

class TrackContainmentMode:
    '''
    Tracks whether we are in the menu or not.
    '''
    def __init__(self, orb):
        self.orb = orb
        #
        self.b_in_menu = True
    #
    def on_menu_focus(self):
        self.b_in_menu = True
    def on_game_focus(self):
        self.b_in_menu = False
    #
    def is_focus_on_menu(self):
        return self.b_in_menu
    def is_focus_on_game(self):
        return not self.b_in_menu

class CogInterpreter:
    '''
    Coordinates high-level concepts such as whether we are in a menu or in the
    game.
    '''
    def __init__(self, cog_h, engine, orb):
        self.cog_h = cog_h
        self.engine = engine
        self.orb = orb
        #
        self.track_containment_mode = orb.track(TrackContainmentMode)
    def on_quit(self):
        raise SolentQuitException('Quit message on stream')
    def on_keystroke(self, keycode):
        if self.track_containment_mode.is_focus_on_menu():
            if keycode == solent_keycode('tab'):
                self.b_in_menu = False
                self.nearcast.game_focus()
            else:
                self.nearcast.menu_select(
                    menu_keycode=keycode)
        else:
            if keycode == solent_keycode('tab'):
                self.b_in_menu = True
                self.nearcast.menu_focus()
            else:
                self.nearcast.game_input(
                    keycode=keycode)
    def on_tselect(self, drop, rest):
        if self.track_containment_mode.is_focus_on_game():
            self.nearcast.game_plot(
                drop=drop,
                rest=rest)

class CogToTerm:
    def __init__(self, cog_h, engine, orb):
        self.cog_h = cog_h
        self.engine = engine
        self.orb = orb
        #
        self.track_prime_console = orb.track(TrackPrimeConsole)
        #
        self.spin_term = None
    #
    def on_init(self):
        width = self.track_prime_console.width
        height = self.track_prime_console.height
        #
        self.spin_term = self.engine.init_spin(
            construct=SpinSelectionUi,
            console_type=self.track_prime_console.console_type,
            cb_selui_keycode=self.cb_selui_keycode,
            cb_selui_lselect=self.cb_selui_lselect)
        self.spin_term.open_console(
            width=width,
            height=height)
    def on_term_clear(self):
        self.spin_term.clear()
    def on_term_write(self, drop, rest, s, cpair):
        self.spin_term.write(
            drop=drop,
            rest=rest,
            s=s,
            cpair=cpair)
    #
    def cb_selui_keycode(self, cs_selui_keycode):
        keycode = cs_selui_keycode.keycode
        #
        self.nearcast.keystroke(
            keycode=keycode)
    def cb_selui_lselect(self, cs_selui_lselect):
        drop = cs_selui_lselect.drop
        rest = cs_selui_lselect.rest
        c = cs_selui_lselect.c
        cpair = cs_selui_lselect.cpair
        #
        # user makes a selection
        self.nearcast.tselect(
            drop=drop,
            rest=rest)

class CogToMenu:
    def __init__(self, cog_h, engine, orb):
        self.cog_h = cog_h
        self.engine = engine
        self.orb = orb
        #
        self.track_prime_console = orb.track(TrackPrimeConsole)
        #
        self.rail_menu = RailMenu()
    def on_init(self):
        console_type = self.track_prime_console.console_type
        height = self.track_prime_console.height
        width = self.track_prime_console.width
        #
        rail_h = '%s/menu'%(self.cog_h)
        self.rail_menu.zero(
            rail_h=rail_h,
            cb_menu_selection=self.cb_menu_selection,
            cb_menu_asks_display_to_clear=self.cb_menu_asks_display_to_clear,
            cb_menu_asks_display_to_write=self.cb_menu_asks_display_to_write,
            height=self.track_prime_console.height,
            width=self.track_prime_console.width,
            title=APP_NAME)
        self.rail_menu.add_menu_item(
            menu_keycode=MENU_KEYCODE_NEW_GAME,
            text='new game')
        self.rail_menu.add_menu_item(
            menu_keycode=MENU_KEYCODE_QUIT,
            text='quit')
        self.nearcast.menu_focus()
    def on_menu_focus(self):
        self.rail_menu.render_menu()
    def on_menu_select(self, menu_keycode):
        d = { MENU_KEYCODE_NEW_GAME: self._mi_new_game
            , MENU_KEYCODE_CONTINUE: self._mi_continue
            , MENU_KEYCODE_QUIT: self._mi_quit
            }
        if menu_keycode not in d:
            return
        fn = d[menu_keycode]
        fn()
    def on_game_new(self):
        if not self.rail_menu.has_menu_keycode(MENU_KEYCODE_CONTINUE):
            self.rail_menu.add_menu_item(
                menu_keycode=MENU_KEYCODE_CONTINUE,
                text='continue')
    #
    def cb_menu_selection(self, cs_menu_selection):
        rail_h = cs_menu_selection.rail_h
        keycode = cs_menu_selection.keycode
        #
        self.nearcast.menu_select(
            menu_keycode=keycode)
    def cb_menu_asks_display_to_clear(self, cs_menu_asks_display_to_clear):
        rail_h = cs_menu_asks_display_to_clear.rail_h
        #
        self.nearcast.term_clear()
    def cb_menu_asks_display_to_write(self, cs_menu_asks_display_to_write):
        rail_h = cs_menu_asks_display_to_write.rail_h
        drop = cs_menu_asks_display_to_write.drop
        rest = cs_menu_asks_display_to_write.rest
        s = cs_menu_asks_display_to_write.s
        #
        self.nearcast.term_write(
            drop=drop,
            rest=rest,
            s=s,
            cpair=solent_cpair('blue'))
    #
    def _mi_new_game(self):
        self.nearcast.game_new()
        self.nearcast.game_focus()
    def _mi_continue(self):
        self.nearcast.game_focus()
    def _mi_quit(self):
        raise SolentQuitException()

class CogToDrawSurface:
    def __init__(self, cog_h, engine, orb):
        self.cog_h = cog_h
        self.engine = engine
        self.orb = orb
        #
        self.track_prime_console = orb.track(TrackPrimeConsole)
        self.track_containment_mode = orb.track(TrackContainmentMode)
        #
        self.rail_draw_surface = RailDrawSurface()
        self.tick_t100 = None
    #
    def orb_turn(self, activity):
        if self.rail_draw_surface == None:
            return
    #
    def on_game_new(self):
        rail_h = '%s/draw_surface'%(self.cog_h)
        self.rail_draw_surface.zero(
            rail_h=rail_h,
            height=self.track_prime_console.height,
            width=self.track_prime_console.width,
            cb_draw_surface_clear=self.cb_draw_surface_clear,
            cb_draw_surface_write=self.cb_draw_surface_write)
    def on_game_input(self, keycode):
        log('xxx game input %s'%keycode)
    def on_game_focus(self):
        if not self.rail_draw_surface.b_started:
            self.nearcast.menu_focus()
            return
        self.rail_draw_surface.render()
    def on_game_plot(self, drop, rest):
        self.rail_draw_surface.flip(
            drop=drop,
            rest=rest)
        self.rail_draw_surface.render()
    #
    def cb_draw_surface_clear(self, cs_draw_surface_clear):
        #
        self.nearcast.term_clear()
    def cb_draw_surface_write(self, cs_draw_surface_write):
        drop = cs_draw_surface_write.drop
        rest = cs_draw_surface_write.rest
        s = cs_draw_surface_write.s
        cpair = cs_draw_surface_write.cpair
        #
        self.nearcast.term_write(
            drop=drop,
            rest=rest,
            s=s,
            cpair=cpair)

def init_nearcast(engine):
    engine.default_timeout = 0.05
    #
    orb = engine.init_orb(
        i_nearcast=I_CONTAINMENT_NEARCAST_SCHEMA)
    orb.add_log_snoop()
    orb.init_cog(CogInterpreter)
    orb.init_cog(CogToTerm)
    orb.init_cog(CogToMenu)
    orb.init_cog(CogToDrawSurface)
    #
    bridge = orb.init_autobridge()
    bridge.nearcast.prime_console(
        console_type='pygame',
        height=24,
        width=78)
    bridge.nearcast.init()
    #
    return bridge


# --------------------------------------------------------
#   loader
# --------------------------------------------------------
MTU = 1500

def main():
    engine = Engine(
        mtu=MTU)
    try:
        init_nearcast(
            engine=engine)
        #
        engine.event_loop()
    except KeyboardInterrupt:
        pass
    except SolentQuitException:
        pass
    finally:
        engine.close()

if __name__ == '__main__':
    main()

