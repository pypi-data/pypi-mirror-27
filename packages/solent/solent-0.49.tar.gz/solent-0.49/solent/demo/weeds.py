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
# Nearcast that is contains a simple roguelike game.

from solent import Engine
from solent import log
from solent import solent_cpair
from solent import solent_keycode
from solent import SolentQuitException
from solent import uniq
from solent.console import Cgrid
from solent.console import RailMenu
from solent.rogue import spin_message_feed_new
from solent.rogue.simple_00_weed_the_garden import spin_simple_new
from solent.util import SpinSelectionUi

from collections import deque
import os
import random
import sys
import time
import traceback

MTU = 1500

# Containment consists of a menu system, a terminal, and cogs that
# encapsulate games.
I_CONTAINMENT_NEARCAST_SCHEMA = '''
    i message h
        i field h

    message prime_console
        field console_type
        field console_height
        field console_width
    message init

    message quit

    message keystroke
        field keycode

    message term_clear
    message term_write
        field drop
        field rest
        field s
        field cpair

    message menu_focus
    message menu_select
        field menu_keycode

    message directive
        field directive_h
        field description
    message keycode_to_directive
        field control_scheme_h
        field keycode
        field directive_h

    message o_game_new
    message x_game_ready
    message x_game_grid
    message x_game_mail
    message x_game_over
    message o_game_focus
    message o_game_keycode
        field keycode
'''

class TrackPrimeConsole:
    def __init__(self, orb):
        self.orb = orb
        #
        self.ctype = None
        self.height = None
        self.width = None
    def on_prime_console(self, console_type, console_height, console_width):
        self.ctype = console_type
        self.height = console_height
        self.width = console_width

CONTROL_SCHEME_H_GOLLOP = 'gollop'
CONTROL_SCHEME_H_KEYPAD = 'keypad'
CONTROL_SCHEME_H_VI = 'vi'

CONSOLE_HEIGHT = 28
CONSOLE_WIDTH = 76

GAME_NAME = 'Weed the Garden'

MENU_KEYCODE_NEW_GAME = solent_keycode('n')
MENU_KEYCODE_CONTINUE = solent_keycode('c')
MENU_KEYCODE_QUIT = solent_keycode('q')

ROGUEBOX_ORIGIN_DROP = 0
ROGUEBOX_ORIGIN_REST = 0

ROGUEBOX_GAMEBOX_HEIGHT = CONSOLE_HEIGHT
ROGUEBOX_GAMEBOX_WIDTH = CONSOLE_WIDTH
ROGUEBOX_GAMEBOX_NAIL = (0, 0)
ROGUEBOX_GAMEBOX_PERI = (CONSOLE_HEIGHT, CONSOLE_WIDTH)

ROGUEBOX_MFEED_HEIGHT = CONSOLE_HEIGHT
ROGUEBOX_MFEED_WIDTH = 57
ROGUEBOX_MFEED_NAIL = (0, 23)
ROGUEBOX_MFEED_PERI = (24, 80)

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
    def on_o_game_focus(self):
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
        self.d_directive = {}
    def on_quit(self):
        raise SolentQuitException('Quit message on stream')
    def on_directive(self, directive_h, description):
        self.d_directive[directive_h] = description
        #
        if directive_h == 'nw':
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_GOLLOP,
                keycode=solent_keycode('q'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_KEYPAD,
                keycode=solent_keycode('n7'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_VI,
                keycode=solent_keycode('y'),
                directive_h=directive_h)
        elif directive_h == 'nn':
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_GOLLOP,
                keycode=solent_keycode('w'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_KEYPAD,
                keycode=solent_keycode('n8'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_VI,
                keycode=solent_keycode('k'),
                directive_h=directive_h)
        elif directive_h == 'ne':
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_GOLLOP,
                keycode=solent_keycode('e'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_KEYPAD,
                keycode=solent_keycode('n9'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_VI,
                keycode=solent_keycode('u'),
                directive_h=directive_h)
        elif directive_h == 'sw':
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_GOLLOP,
                keycode=solent_keycode('z'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_KEYPAD,
                keycode=solent_keycode('n1'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_VI,
                keycode=solent_keycode('b'),
                directive_h=directive_h)
        elif directive_h == 'ss':
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_GOLLOP,
                keycode=solent_keycode('x'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_KEYPAD,
                keycode=solent_keycode('n2'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_VI,
                keycode=solent_keycode('j'),
                directive_h=directive_h)
        elif directive_h == 'se':
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_GOLLOP,
                keycode=solent_keycode('c'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_KEYPAD,
                keycode=solent_keycode('n3'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_VI,
                keycode=solent_keycode('n'),
                directive_h=directive_h)
        elif directive_h == 'ww':
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_GOLLOP,
                keycode=solent_keycode('a'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_KEYPAD,
                keycode=solent_keycode('n4'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_VI,
                keycode=solent_keycode('h'),
                directive_h=directive_h)
        elif directive_h == 'ee':
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_GOLLOP,
                keycode=solent_keycode('d'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_KEYPAD,
                keycode=solent_keycode('n6'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_VI,
                keycode=solent_keycode('l'),
                directive_h=directive_h)
        elif directive_h == 'a':
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_GOLLOP,
                keycode=solent_keycode('s'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_KEYPAD,
                keycode=solent_keycode('n5'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_VI,
                keycode=solent_keycode('space'),
                directive_h=directive_h)
        elif directive_h == 'b':
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_GOLLOP,
                keycode=solent_keycode('r'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_KEYPAD,
                keycode=solent_keycode('n0'),
                directive_h=directive_h)
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_VI,
                keycode=solent_keycode('slash'),
                directive_h=directive_h)
        elif directive_h == 'help':
            self.nearcast.keycode_to_directive(
                control_scheme_h=CONTROL_SCHEME_H_VI,
                keycode=solent_keycode('qmark'),
                directive_h=directive_h)
        else:
            raise Exception('Unhandled directive %s'%(directive.h))
    def on_keystroke(self, keycode):
        if self.track_containment_mode.is_focus_on_menu():
            if keycode == solent_keycode('tab'):
                self.b_in_menu = False
                self.nearcast.o_game_focus()
            else:
                self.nearcast.menu_select(
                    menu_keycode=keycode)
        else:
            if keycode == solent_keycode('tab'):
                self.b_in_menu = True
                self.nearcast.menu_focus()
            else:
                self.nearcast.o_game_keycode(
                    keycode=keycode)

class CogTerm:
    def __init__(self, cog_h, engine, orb):
        self.cog_h = cog_h
        self.engine = engine
        self.orb = orb
        #
        self.track_prime_console = orb.track(TrackPrimeConsole)
        #
        self.spin_term = None
    def on_init(self):
        self.spin_term = self.engine.init_spin(
            construct=SpinSelectionUi,
            console_type=self.track_prime_console.ctype,
            cb_selui_keycode=self.cb_selui_keycode,
            cb_selui_lselect=self.cb_selui_lselect)
        self.spin_term.open_console(
            width=self.track_prime_console.width,
            height=self.track_prime_console.height)
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
        pass

class CogMenu:
    def __init__(self, cog_h, engine, orb):
        self.cog_h = cog_h
        self.engine = engine
        self.orb = orb
        #
        self.track_prime_console = orb.track(TrackPrimeConsole)
        #
        self.rail_menu = RailMenu()
    def on_init(self):
        rail_h = '%s/menu'%(self.cog_h)
        self.rail_menu.zero(
            rail_h=rail_h,
            cb_menu_asks_display_to_clear=self.cb_menu_asks_display_to_clear,
            cb_menu_asks_display_to_write=self.cb_menu_asks_display_to_write,
            cb_menu_selection=self.cb_menu_selection,
            height=self.track_prime_console.height,
            width=self.track_prime_console.width,
            title=GAME_NAME)
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
    def on_o_game_new(self):
        if not self.rail_menu.has_menu_keycode(MENU_KEYCODE_CONTINUE):
            self.rail_menu.add_menu_item(
                menu_keycode=MENU_KEYCODE_CONTINUE,
                text='continue')
    #
    def cb_menu_selection(self, cs_menu_selection):
        rail_h = cs_menu_selection.rail_h
        keycode = cs_menu_selection.keycode
        text = cs_menu_selection.text
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
        self.nearcast.o_game_new()
        self.nearcast.o_game_focus()
    def _mi_continue(self):
        self.nearcast.o_game_focus()
    def _mi_quit(self):
        raise SolentQuitException()

class CogRoguebox:
    '''
    Contains a roguelike game, and offers controls. The roguelike itself
    is contained to a 23x23 box in the top-left sector.
    Logging is offered in a box next to that.
    '''
    def __init__(self, cog_h, engine, orb):
        self.cog_h = cog_h
        self.engine = engine
        self.orb = orb
        #
        self.track_prime_console = orb.track(TrackPrimeConsole)
        self.track_containment_mode = orb.track(TrackContainmentMode)
        #
        self.spin_roguelike = None
        self.spin_message_feed = None
        self.cgrid_last = None
        self.cgrid_next = None
        self.d_keycode_to_directive = {}
        self.d_control_scheme = {} # (control_scheme_h, directive_h) = keycode
        #
        self.b_game_started = False
        self.b_mail_waiting = False
        self.b_refresh_needed = False
    def orb_turn(self, activity):
        if None == self.spin_roguelike:
            return
        if not self.track_containment_mode.is_focus_on_game():
            return
        if self.b_mail_waiting:
            activity.mark(
                l=self,
                s='mail processing')
            for message in self.spin_roguelike.retrieve_mail():
                self.spin_message_feed.accept(
                    message=message,
                    turn=self.spin_roguelike.get_turn())
            self.b_mail_waiting = False
            self.b_refresh_needed = True
        #
        if self.b_refresh_needed:
            self._diff_display_refresh()
            self.b_refresh_needed = False
    #
    def on_init(self):
        console_height = self.track_prime_console.height
        console_width = self.track_prime_console.width
        #
        if console_height < ROGUEBOX_GAMEBOX_HEIGHT:
            raise Exception("console height %s too small for game height %s."%(
                console_height, ROGUEBOX_GAMEBOX_HEIGHT))
        if console_width < ROGUEBOX_GAMEBOX_WIDTH:
            raise Exception("console width %s too small for game width %s."%(
                console_width, ROGUEBOX_GAMEBOX_WIDTH))
        self.spin_roguelike = spin_simple_new(
            engine=self.engine,
            grid_height=ROGUEBOX_GAMEBOX_HEIGHT,
            grid_width=ROGUEBOX_GAMEBOX_WIDTH,
            cb_ready_alert=self._rl_ready_alert,
            cb_grid_alert=self._rl_grid_alert,
            cb_mail_alert=self._rl_mail_alert,
            cb_over_alert=self._rl_over_alert)
        self.spin_message_feed = spin_message_feed_new(
            height=ROGUEBOX_MFEED_HEIGHT,
            width=ROGUEBOX_MFEED_WIDTH,
            cpair_new=solent_cpair('teal'),
            cpair_old=solent_cpair('blue'))
        self.cgrid_last = Cgrid(
            width=console_width,
            height=console_height)
        self.cgrid_next = Cgrid(
            width=console_width,
            height=console_height)
        #
        # sequence the possible directives in the game to the core. this will
        # give this outer core the opportunity to match directives it
        # recognises to keycodes. in the future, you could imagine being able
        # to configure user keystrokes using this data.
        for directive in self.spin_roguelike.get_supported_directives():
            self.nearcast.directive(
                directive_h=directive.h,
                description=directive.description)
    def on_keycode_to_directive(self, control_scheme_h, keycode, directive_h):
        self.d_keycode_to_directive[keycode] = directive_h
        self.d_control_scheme[ (control_scheme_h, directive_h) ] = keycode
    def on_x_game_ready(self):
        self.b_game_started = True
        self.nearcast.o_game_focus()
    def on_o_game_new(self):
        self.spin_message_feed.clear()
        self.spin_roguelike.new_game()
    def on_x_game_mail(self):
        self.b_mail_waiting = True
    def on_x_game_grid(self):
        self.b_refresh_needed = True
    def on_o_game_keycode(self, keycode):
        if keycode not in self.d_keycode_to_directive:
            return
        directive_h = self.d_keycode_to_directive[keycode]
        self.spin_roguelike.directive(
            directive_h=directive_h)
        self.spin_message_feed.scroll_past(
            turn=self.spin_roguelike.get_turn()-3)
        self.b_refresh_needed = True
    def on_o_game_focus(self):
        if not self.b_game_started:
            self.nearcast.menu_focus()
            return
        self._full_display_refresh()
    #
    def _rl_ready_alert(self):
        self.nearcast.x_game_ready()
    def _rl_grid_alert(self):
        self.nearcast.x_game_grid()
    def _rl_mail_alert(self):
        self.nearcast.x_game_mail()
    def _rl_over_alert(self):
        self.nearcast.x_game_over()
    #
    def _full_display_refresh(self):
        self.nearcast.term_clear()
        self.cgrid_last.clear()
        self._diff_display_refresh()
    def _diff_display_refresh(self):
        self.spin_roguelike.get_cgrid(
            cgrid=self.cgrid_next,
            nail=ROGUEBOX_GAMEBOX_NAIL,
            peri=ROGUEBOX_GAMEBOX_PERI)
        for idx, message in enumerate(self.spin_message_feed.list_messages()):
            self.cgrid_next.put(
                drop=idx,
                rest=0,
                s=message,
                cpair=solent_cpair('white'))
        #
        for drop in range(self.track_prime_console.height):
            for rest in range(self.track_prime_console.width):
                (old_c, old_cpair) = self.cgrid_last.get(
                    drop=drop,
                    rest=rest)
                (c, cpair) = self.cgrid_next.get(
                    drop=drop,
                    rest=rest)
                if c == old_c and cpair == old_cpair:
                    continue
                self.nearcast.term_write(
                    drop=drop,
                    rest=rest,
                    s=c,
                    cpair=cpair)
        #
        self.cgrid_last.blit(
            src_cgrid=self.cgrid_next)

def game(console_type):
    engine = None
    try:
        engine = Engine(
            mtu=MTU)
        engine.set_default_timeout(0.04)
        #engine.debug_eloop_on()
        #
        orb = engine.init_orb(
            i_nearcast=I_CONTAINMENT_NEARCAST_SCHEMA)
        #orb.add_log_snoop()
        orb.init_cog(CogInterpreter)
        orb.init_cog(CogTerm)
        orb.init_cog(CogMenu)
        orb.init_cog(CogRoguebox)
        #
        bridge = orb.init_autobridge()
        bridge.nearcast.prime_console(
            console_type=console_type,
            console_height=CONSOLE_HEIGHT,
            console_width=CONSOLE_WIDTH)
        bridge.nearcast.init()
        #
        engine.event_loop()
    except SolentQuitException:
        pass
    except:
        traceback.print_exc()
    finally:
        if engine != None:
            engine.close()

def main():
    console_type = 'curses'
    game(
        console_type=console_type)

if __name__ == '__main__':
    main()

