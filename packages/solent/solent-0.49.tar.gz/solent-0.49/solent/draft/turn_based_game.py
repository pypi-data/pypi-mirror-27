#!/usr/bin/python
#
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
# demo_experience. This is old, pre-nearcast code. Consider this heavily
# deprecated. It was originally intende dto exercise the console code. It
# turned into a proof-of-concept for a turn-based scheduling algorithm.
#

from .turnlib.algobunny_mind import algobunny_mind_new
from .turnlib.cursor import cursor_new
from .turnlib.menu import menu_new
from .turnlib.player_mind import player_mind_new
from .turnlib.rogue_interaction import rogue_interaction_new
from .turnlib.rogue_plane import rogue_plane_new
from .turnlib.initiative import initiative_new

from solent import solent_cpair
from solent import solent_keycode
from solent import SolentQuitException
from solent import uniq
from solent.console import e_boxtype
from solent.console import Cgrid
from solent.console import Console

from collections import deque
import os
import sys
import time
import traceback

ESC_KEY_ORD = 27

C_GAME_WIDTH = 78
C_GAME_HEIGHT = 25


# --------------------------------------------------------
#   :game
# --------------------------------------------------------
T_WHITE = solent_cpair('white')

def make_box(rogue_plane, se_nail, width, height, cpair=T_WHITE, box_type=e_boxtype.line):
    '''
    Box type indicates the kind of corners the box should have.
    '''
    (s_nail, e_nail) = se_nail
    hori = width+2
    for i in range(hori):
        if (i, box_type) in [(0, e_boxtype.edge), (hori-1, e_boxtype.void)]:
            rogue_plane.create_terrain(
                s=s_nail,
                e=e_nail+i,
                c='/',
                cpair=cpair)
            rogue_plane.create_terrain(
                s=s_nail+height+1,
                e=e_nail+i,
                c='\\',
                cpair=cpair)
        elif (i, box_type) in [(hori-1, e_boxtype.edge), (0, e_boxtype.void)]:
            rogue_plane.create_terrain(
                s=s_nail,
                e=e_nail+i,
                c='\\',
                cpair=cpair)
            rogue_plane.create_terrain(
                s=s_nail+height+1,
                e=e_nail+i,
                c='/',
                cpair=cpair)
        else:
            if box_type == e_boxtype.hash:
                c = '#'
            elif box_type == e_boxtype.stop:
                c = '.'
            else:
                c = '-'
            rogue_plane.create_terrain(
                s=s_nail,
                e=e_nail+i,
                c=c,
                cpair=cpair)
            rogue_plane.create_terrain(
                s=s_nail+height+1,
                e=e_nail+i,
                c=c,
                cpair=cpair)
    for i in range(height):
        if box_type == e_boxtype.hash:
            c = '#'
        elif box_type == e_boxtype.stop:
            c = '.'
        else:
            c = '|'
        rogue_plane.create_terrain(
            s=s_nail+i+1,
            e=e_nail,
            c=c,
            cpair=cpair)
        rogue_plane.create_terrain(
            s=s_nail+i+1,
            e=e_nail+width+1,
            c=c,
            cpair=cpair)

def create_origin_plane():
    rogue_plane = rogue_plane_new()
    #
    # // terrain: walls
    make_box(
        rogue_plane=rogue_plane,
        se_nail=(-5, -8),
        width=30,
        height=14,
        box_type=e_boxtype.stop)
    make_box(
        rogue_plane=rogue_plane,
        se_nail=(6, 3),
        width=1,
        height=1)
    make_box(
        rogue_plane=rogue_plane,
        se_nail=(-2, -17),
        width=3,
        height=3,
        cpair=solent_cpair('teal'),
        box_type=e_boxtype.edge)
    make_box(
        rogue_plane=rogue_plane,
        se_nail=(-2, 10),
        width=3,
        height=3,
        cpair=solent_cpair('teal'),
        box_type=e_boxtype.void)
    make_box(
        rogue_plane=rogue_plane,
        se_nail=(4, 10),
        width=3,
        height=3,
        cpair=solent_cpair('teal'),
        box_type=e_boxtype.stop)
    make_box(
        rogue_plane=rogue_plane,
        se_nail=(-4, 28),
        width=3,
        height=3,
        box_type=e_boxtype.hash)
    make_box(
        rogue_plane=rogue_plane,
        se_nail=(4, 28),
        width=3,
        height=3,
        box_type=e_boxtype.stop)
    #
    # // terrain: boulder
    rogue_plane.create_terrain(
        s=-1,
        e=-3,
        c='o')
    #
    # // terrain: standing stones
    rogue_plane.create_terrain(
        s=-2,
        e=-2,
        c='i',
        cpair=solent_cpair('white'))
    rogue_plane.create_terrain(
        s=-3,
        e=0,
        c='i',
        cpair=solent_cpair('white'))
    rogue_plane.create_terrain(
        s=-2,
        e=2,
        c='i',
        cpair=solent_cpair('white'))
    rogue_plane.create_terrain(
        s=0,
        e=-3,
        c='i',
        cpair=solent_cpair('white'))
    rogue_plane.create_terrain(
        s=0,
        e=3,
        c='i',
        cpair=solent_cpair('white'))
    rogue_plane.create_terrain(
        s=2,
        e=-2,
        c='i',
        cpair=solent_cpair('white'))
    rogue_plane.create_terrain(
        s=3,
        e=0,
        c='i',
        cpair=solent_cpair('white'))
    rogue_plane.create_terrain(
        s=2,
        e=2,
        c='i',
        cpair=solent_cpair('white'))
    #
    # // scrap
    rogue_plane.create_meep(
        s=3,
        e=-4,
        c=':',
        cpair=solent_cpair('yellow'))
    return rogue_plane

class Game(object):
    def __init__(self, console, initiative):
        self.console = console
        self.initiative = initiative
        #
        self.rogue_plane = create_origin_plane()
        self.player_meep = self.rogue_plane.create_meep(
            s=0,
            e=0,
            c='@',
            cpair=solent_cpair('red'))
        #
        self.rogue_interaction = rogue_interaction_new(
            console=console,
            cursor=cursor_new(
                fn_s=lambda: self.player_meep.coords.s,
                fn_e=lambda: self.player_meep.coords.e,
                fn_c=lambda: self.player_meep.c,
                fn_cpair=lambda: self.player_meep.cpair))
        #
        # algobunny
        self.algobunny_meep = self.rogue_plane.create_meep(
            mind=algobunny_mind_new(),
            overhead=3,
            s=3,
            e=3,
            c='"',
            cpair=solent_cpair('white'))
        self.initiative.add_meep(
            meep=self.algobunny_meep)
        #
        # player
        self.player_mind = player_mind_new(
            console=console,
            rogue_interaction=self.rogue_interaction)
        self.player_meep.mind = self.player_mind
        self.initiative.add_meep(
            meep=self.player_meep)
    def accept_key(self, key):
        if key in (None, ''):
            return
        if len(key) != 1:
            print('!! weird value in var key: [%s] [%s]'%(
                '/'.join([str(ord(k)) for k in key]),
                key))
            return
        self.player_mind.add_key(key)
    def turn(self):
        activity = self.initiative.dispatch_next_tick()
        #
        plane_type = self.player_meep.plane.get_plane_type()
        if plane_type == 'RoguePlane':
            self.rogue_interaction.render(
                rogue_plane=self.rogue_plane)
        else:
            raise Exception('unsupported plane_type [%s]'%plane_type)
        #
        return activity

def game_new(console):
    initiative = initiative_new(
        accelerated_time=True)
    ob = Game(
        console=console,
        initiative=initiative)
    return ob


# --------------------------------------------------------
#   :husk
# --------------------------------------------------------
#
# The husk is the thing that contains the game. The husk exposes new game and
# load game and save game.
#
CPAIR_MENU_BORDER = solent_cpair('black_info')
CPAIR_MENU_TEXT = solent_cpair('white')
CPAIR_TITLE = solent_cpair('white')

class Husk(object):
    def __init__(self, console, cgrid, title):
        self.console = console
        self.cgrid = cgrid
        self.title = title
        #
        self.b_menu_active = True
        self.game = None
        #
        # Later on we could use something like pyfiglet for this. Better would
        # be a single distinct font, similar to what Gollop did with rebelstar.
        self.title_cgrid = Cgrid(
            width=len(self.title),
            height=1)
        self.title_cgrid.put(
            drop=0,
            rest=0,
            s=self.title,
            cpair=CPAIR_TITLE)
        #
        self.menu = menu_new()
        self.menu_cgrid = None
    #
    def _generate_menu_content(self):
        def mi_new_game():
            print('xxx new game')
            self.game = game_new(
                console=self.console)
            self.b_menu_active = False
        def mi_load_game():
            print('xxx __mi_load_game')
        def mi_continue_game():
            print('xxx continue game')
            self.b_menu_active = False
        def mi_save_game():
            print('xxx __mi_save_game')
        def mi_quit():
            raise SolentQuitException()
        self.menu.clear()
        if None != self.game:
            self.menu.add('c', 'continue', mi_continue_game)
            self.menu.add('s', 'save', mi_save_game)
        self.menu.add('l', 'load', mi_load_game)
        self.menu.add('n', 'new', mi_new_game)
        self.menu.add('q', 'quit', mi_quit)
    def _allocate_menu_cgrid(self):
        '''
        xxx it's garbagey to repreatedly recreate this. create an issue.
        better solution: plot the menu directly to the main cgrid, rather than
        having separate cgrids for title and menu.
        '''
        lines = self.menu.get_lines()
        longest_line = 0
        for l in lines:
            longest_line = max( [longest_line, len(l)] )
        #
        # prepare the menu border
        self.menu_cgrid = Cgrid(
            width=longest_line+4,
            height=len(lines)+2)
        horiz = ' '*(longest_line+4)
        menu_border_height = len(lines)+2
        for idx in range(menu_border_height):
            if idx in (0, menu_border_height-1):
                self.menu_cgrid.put(
                    drop=idx,
                    rest=0,
                    s=horiz,
                    cpair=CPAIR_MENU_BORDER)
            else:
                line = lines[idx-1]
                self.menu_cgrid.put(
                    drop=idx,
                    rest=0,
                    s=' ',
                    cpair=CPAIR_MENU_BORDER)
                self.menu_cgrid.put(
                    drop=idx,
                    rest=1,
                    s=' %s%s '%(line, ' '*(longest_line-len(line))),
                    cpair=CPAIR_MENU_TEXT)
                self.menu_cgrid.put(
                    drop=idx,
                    rest=longest_line+3,
                    s=' ',
                    cpair=CPAIR_MENU_BORDER)
    def _render_title(self):
        self.cgrid.blit(
            src_cgrid=self.title_cgrid,
            nail=(0, 0))
    def _render_menu(self):
        menu_drop = int((self.cgrid.height / 2) - (self.menu_cgrid.height / 2))
        menu_rest = int((self.cgrid.width / 2) - (self.menu_cgrid.width / 2))
        nail = (menu_drop, menu_rest)
        self.cgrid.blit(
            src_cgrid=self.menu_cgrid,
            nail=nail)
    def _render(self):
        self._generate_menu_content()
        self._allocate_menu_cgrid()
        self._render_title()
        self._render_menu()
        self.console.screen_update(
            cgrid=self.cgrid)
    #
    def event_loop(self):
        self._render()
        while True:
            #
            # Defensive
            if self.game == None:
                self.b_menu_active = True
            #
            # Input
            if self.b_menu_active:
                keycode = self.console.block_get_keycode()
            elif self.game != None and self.game.player_mind.is_blocking():
                keycode = self.console.block_get_keycode()
            else:
                keycode = self.console.async_get_keycode()
            b_key = True
            if keycode == None:
                b_key = False
            #
            # Menu
            if self.b_menu_active:
                if b_key:
                    if keycode == solent_keycode('tab') and self.game != None:
                        self.b_menu_active = False
                        keycode = None
                    elif self.menu.has_key(chr(keycode)):
                        fn = self.menu.get_callback(chr(keycode))
                        fn()
                        keycode = None
            else:
                if b_key:
                    if keycode == solent_keycode('tab'):
                        self.b_menu_active = True
                        keycode = None
                        self._render()
                        continue
                    else:
                        self.game.accept_key(
                            key=chr(keycode))
                        keycode = None
            #
            # Update display.
            if self.b_menu_active:
                self._render()
            else:
                activity = self.game.turn()
                if activity:
                    time.sleep(0.05)
                if not activity:
                    time.sleep(0.1)


# --------------------------------------------------------
#   :rest
# --------------------------------------------------------
TITLE = 'sample game (solent.client)'

def main():
    if '--curses' in sys.argv:
        console_type = 'curses'
    elif '--pygame' in sys.argv:
        console_type = 'pygame'
    else:
        print('ERROR: specify either --curses or --pygame')
        sys.exit(1)
    #
    console = None
    try:
        console = Console(
            console_type=console_type,
            width=C_GAME_WIDTH,
            height=C_GAME_HEIGHT)
        #
        cgrid = Cgrid(
            width=console.width,
            height=console.height)
        husk = Husk(
            console=console,
            cgrid=cgrid,
            title=TITLE)
        #
        # event loop
        husk.event_loop()
    except SolentQuitException:
        pass
    except:
        traceback.print_exc()
    finally:
        if None != console:
            console.close()

if __name__ == '__main__':
    main()

