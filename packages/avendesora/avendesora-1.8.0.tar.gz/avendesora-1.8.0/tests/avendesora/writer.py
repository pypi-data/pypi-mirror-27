# Abraxas Password Writers
# encoding: utf8
#
# Given a secret (password or passphrase) the writer is responsible for getting 
# it to the user in a reasonably secure manner.

# License {{{1
# Copyright (C) 2016-17 Kenneth S. Kundert
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.

# Imports {{{1
from . import cursor
from .config import get_setting
from .error import PasswordError
from .dialog import show_list_dialog
from .preferences import INITIAL_AUTOTYPE_DELAY
from shlib import Run
from inform import (
    Color,
    codicil, cull, error, log, output, warn, indent, os_error,
    ddd, ppp, vvv
)
from time import sleep
from textwrap import dedent
import string
import re

# Globals {{{1
LabelColor = Color(
    color=get_setting('label_color'),
    scheme=get_setting('color_scheme'),
    enable=Color.isTTY()
)
KEYSYMS = {
    '!': 'exclam',
    '"': 'quotedbl',
    '#': 'numbersign',
    '$': 'dollar',
    '%': 'percent',
    '&': 'ampersand',
    "'": 'apostrophe',
    '(': 'parenleft',
    ')': 'parenright',
    '*': 'asterisk',
    '+': 'plus',
    ',': 'comma',
    '-': 'minus',
    '.': 'period',
    '/': 'slash',
    ' ': 'space',
    ':': 'colon',
    ';': 'semicolon',
    '<': 'less',
    '=': 'equal',
    '>': 'greater',
    '?': 'question',
    '@': 'at',
    '[': 'bracketleft',
    '\\': 'backslash',
    ']': 'bracketright',
    '^': 'asciicircum',
    '_': 'underscore',
    '`': 'grave',
    '{': 'braceleft',
    '|': 'bar',
    '}': 'braceright',
    '~': 'asciitilde',
    '\n': 'Return',
    '\t': 'Tab',
}

# Writer selection {{{1
def get_writer(tty=None, clipboard=False, stdout=False):
    if clipboard:
        return ClipboardWriter()
    if stdout:
        return StdoutWriter()
    if tty is True:
        return TTY_Writer()
    if tty is False:
        return KeyboardWriter()
    if Color.isTTY():
        return TTY_Writer()
    else:
        return KeyboardWriter()

# Writer base class {{{1
class Writer(object):

    @staticmethod
    def render_script(account, field):

        # if field was not given
        if not field:
            name, key = account.split_field(field)
            field = '.'.join(cull([name, key]))

        # treat field as name rather than script if it there are not attributes
        if '{' not in field:
            name, key = account.split_field(field)
            value = account.get_scalar(name, key)
            is_secret = account.is_secret(name, key)
            label = account.combine_field(name, key)
            try:
                alt_name = value.get_key()
                if alt_name:
                    label += ' (%s)' % alt_name
            except AttributeError:
                pass
            return dedent( str(value)).strip(), is_secret, label
        script = field

        # Run the script
        regex = re.compile(r'({[\w. ]+})')
        out = []
        is_secret = False
        for term in regex.split(script):
            if term and term[0] == '{' and term[-1] == '}':
                # we have found a command
                cmd = term[1:-1].lower()
                if cmd == 'tab':
                    out.append('\t')
                elif cmd == 'return':
                    out.append('\n')
                elif cmd.startswith('sleep '):
                    pass
                else:
                    name, key = account.split_field(cmd)
                    value = account.get_scalar(name, key)
                    out.append(dedent(str(value)).strip())
                    if account.is_secret(name, key):
                        is_secret = True
            else:
                out.append(term)
        return ''.join(out), is_secret, None


# TTY_Writer class {{{1
class TTY_Writer(Writer):
    """Writes output to the user's TTY."""

    def display_field(self, account, field):
        # get string to display
        value, is_secret, name, desc = tuple(account.get_value(field))
        label = '%s (%s)' % (name, desc) if desc else name

        # indent multiline outputs
        sep = ' '
        if '\n' in value:
            if is_secret:
                warn('secret contains newlines, will not be fully concealed.')
            else:
                value = indent(dedent(value), get_setting('indent')).strip('\n')
                sep = '\n'

        if label:
            text = LabelColor(label.replace('_', '-') + ':') + sep + value
        else:
            text = value
            label = field
        log('Writing to TTY:', label)

        if is_secret:
            if Color.isTTY():
                # Write only if output is a TTY. This is a security feature.
                # The ideas is that when the TTY writer is called it is because
                # the user is expecting the output to go to the tty. This
                # eliminates the chance that the output can be intercepted and
                # recorded by replacing Avendesora with an alias or shell
                # script. If the user really want the output to go to something
                # other than the TTY, the user should use the --stdout option.
                try:
                    cursor.write(text)
                    cursor.conceal()
                    sleep(get_setting('display_time'))
                except KeyboardInterrupt:
                    pass
                cursor.reveal()
                cursor.clear()
            else:
                error('output is not a TTY.')
                codicil(
                    'Use --stdout option if you want to send secret',
                    'to a file or a pipe.'
                )
        else:
            output(text)


# ClipboardWriter class {{{1
class ClipboardWriter(Writer):
    """Writes output to the system clipboard."""

    def display_field(self, account, field):

        # get string to display
        value, is_secret, name, desc, = tuple(account.get_value(field))

        # Use 'xsel' to put the information on the clipboard.
        # This represents a vulnerability, if someone were to replace xsel they
        # could steal my passwords. This is why I use an absolute path. I tried
        # to access the clipboard directly using GTK but I cannot get the code
        # to work.
        base_cmd = Run.split(get_setting('xsel_executable'))

        log('Writing to clipboard.')
        try:
            Run(base_cmd + ['-i'], 'soeW', stdin=value+'\n')
        except OSError as e:
            raise PasswordError(os_error(e))

        if is_secret:
            # produce count down
            try:
                for t in range(get_setting('display_time'), -1, -1):
                    cursor.write(str(t))
                    sleep(1)
                    cursor.clear()
            except KeyboardInterrupt:
                cursor.clear()

            # clear the clipboard
            try:
                Run(base_cmd + ['-c'], 'soew')
            except OSError as e:
                raise PasswordError(os_error(e))

        # Use Gobject Introspection (GTK) to put the information on the
        # clipboard (for some reason I cannot get this to work).
        #try:
        #    from gi.repository import Gtk, Gdk
        #
        #    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        #    clipboard.set_text(text, len(text))
        #    clipboard.store()
        #    sleep(self.wait)
        #    clipboard.clear()
        #except ImportError:
        #    error('Clipboard is not supported.')


# StdoutWriter class {{{1
class StdoutWriter(Writer):
    """Writes to the standard output."""

    def display_field(self, account, field):
        # get string to display
        value = account.get_value(field)

        # don't use inform otherwise password shows up in logfile
        print(str(value))
        log('writing secret to standard output.')


# KeyboardWriter class {{{1
class KeyboardWriter(Writer):
    """Writes output via pseudo-keyboard."""

    def _autotype(self, text):
        # Split the text into individual key strokes and convert the special
        # characters to their xkeysym names

        def run_xdotool(args):
            try:
                #[get_setting('xdotool_executable'), 'getactivewindow'] +
                Run(get_setting('xdotool_executable').split() + args, 'soeW')
            except OSError as e:
                raise PasswordError(os_error(e))

        keysyms = []
        for char in text:
            if char in string.ascii_letters + string.digits:
                keysym = char
            else:
                keysym = KEYSYMS.get(char)
            if not keysym:
                error('cannot map to keysym, unknown.', culprit=char)
            else:
                keysyms.append(keysym)
        run_xdotool('key --clearmodifiers'.split() + keysyms)

    def display_field(self, account, field):
        # get string to display
        value = account.get_value(field)

        log('writing secret to keyboard writer.')
        self._autotype(str(value))

    def run_script(self, account, script, dryrun):

        # Create the default script if a script was not given
        if script is True:
            # this bit of trickery gets the name of the default field
            name, key = account.split_field(None)
            name = account.combine_field(name, key)
            script = "{%s}{return}" % name

        # Run the script
        out = []
        scrubbed = []
        sleep(INITIAL_AUTOTYPE_DELAY)
        regex = re.compile(r'({[\w. ]+})')
        for term in regex.split(script):
            if term and term[0] == '{' and term[-1] == '}':
                # we have found a command
                cmd = term[1:-1].lower()
                if cmd == 'tab':
                    out.append('\t')
                    scrubbed.append('\t')
                elif cmd == 'return':
                    out.append('\n')
                    scrubbed.append('\n')
                elif cmd.startswith('sleep '):
                    cmd = cmd.split()
                    try:
                        assert cmd[0] == 'sleep'
                        assert len(cmd) == 2
                        if out:
                            # drain the buffer before sleeping
                            if not dryrun:
                                self._autotype(''.join(out))
                            out = []
                        sleep(float(cmd[1]))
                        scrubbed.append('<sleep %s>' % cmd[1])
                    except TypeError:
                        raise PasswordError(
                            'syntax error in keyboard script.', culprit=term
                        )
                else:
                    name, key = account.split_field(cmd)
                    try:
                        value = account.get_scalar(name, key)
                    except PasswordError as e:
                        if e.is_collection and len(e.collection):
                            # is composite value, ask user which one is desired
                            choices = e.collection
                            if len(choices) == 1:
                                choice = choices.keys()[0]
                            else:
                                choice = show_list_dialog(
                                    'Choose from %s' % name,
                                    sorted(choices.keys())
                                )
                            key = choices[choice]
                            value = account.get_scalar(name, key)
                        else:
                            raise
                    value = dedent(str(value)).strip()
                    out.append(value)
                    if account.is_secret(name, key):
                        scrubbed.append('<%s>' % cmd)
                    else:
                        scrubbed.append(value)
            elif term:
                out.append(term)
                scrubbed.append(term)

        scrubbed = ''.join(scrubbed).replace('\t', '→').replace('\n', '↲')
        log('Autotyping "%s"%s.' % (scrubbed, ' -- dry run' if dryrun else ''))
        if dryrun:
            output(account.get_name(), scrubbed, sep=': ')
        else:
            self._autotype(''.join(out))
