# Account
# API for an account

# License {{{1
# Copyright (C) 2016-17 Kenneth S. Kundert
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see http://www.gnu.org/licenses/.


# Imports {{{1
from .browsers import StandardBrowser
from .collection import Collection
from .config import get_setting
from .error import PasswordError
from .obscure import ObscuredSecret
from .preferences import TOOL_FIELDS
from .recognize import Recognizer
from .secrets import GeneratedSecret
from inform import (
    Color, codicil, conjoin, cull, debug, is_collection, is_str, log,
    notify, output, warn, indent,
    ddd, ppp, vvv
)
from textwrap import dedent
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import re


# Globals {{{1
VECTOR_PATTERN = re.compile(r'\A(\w+)\[(\w+)\]\Z')
LabelColor = Color(
    color=get_setting('label_color'),
    scheme=get_setting('color_scheme'),
    enable=Color.isTTY()
)


# Utilities {{{1
def canonicalize(name):
    return name.replace('-', '_').lower()


# AccountValue class {{{1
class AccountValue:
    """An account value.

    This is the object returned by :meth:`avendesora.Account.get_value` and
    :meth:`avendesora.Account.get_values`.
    It contains information about a single account value. Specifically, it
    provides the following attributes: *value*, *is_secret*, *name*, *key*,
    *field*, and *desc*.
    """
    def __init__(self, value, is_secret, name=None, key=None, desc=None):
        self.value = value
        self.is_secret = is_secret
        self.name = name
        self.key = str(key) if key is not None else key
        self.field = '.'.join(cull([name, self.key]))
        self.desc = desc

    def __str__(self):
        "Returns value as string."
        if hasattr(self.value, 'entropy'):
            entropy = round(self.value.entropy)
            log('entropy of {} = {} bits'.format(self.name, entropy))
        return str(self.value)

    def render(self, fmts=('{f} ({d}): {v}', '{f}: {v}')):
        """Return value formatted as a string.

        Args:
            fmts (collection of strings):
                *fmts* contains a sequence of format strings that are tried in
                sequence.  The first one for which all keys are known is used.
                The possible keys are:

                | n -- name (identifier for the first level of a field)
                | k -- key (identifier for the second level of a field)
                | f -- field (name.key)
                | d -- description
                | v -- value

                If none work, the value alone is returned.
        Returns:
            The value rendered as a string.
        """
        value = str(self.value)
        if '\n' in value:
            value = '\n'+indent(dedent(value), get_setting('indent')).strip('\n')
        if is_str(fmts):
            fmts = fmts,

        # build list of arguments, deleting any that is not set
        args = {
            k: v for k, v in [
                ('f', self.field),
                ('k', self.key),
                ('n', self.name),
                ('d', self.desc),
                ('v', value)
            ] if v
        }

        # format the arguments, use first format sting that works
        for fmt in fmts:
            try:
                return fmt.format(**args)
            except KeyError:
                pass

        # nothing worked, just return the value
        return value

    def __iter__(self):
        "Cast AccountValue to a tuple to get value, is_secret, name, and desc."
        for each in [str(self), self.is_secret, self.name, self.desc]:
            yield each


# Script class {{{1
class Script:
    """Script

    Takes a string that contains attributes. Those attributes are expanded
    before being output. For example::

        Script('username: {username}, password: {passcode}')

    In this case, *{username}* and *{passcode}* are replaced by with the value
    of the corresponding account attribute. In addition to the account
    attributes, *{tab}* and *{return}* are replaced by a tab or carriage return
    character.

    Args:
        script (str):  The script.

    Raises:
        :exc:`avendesora.PasswordError`: attribute not found.
    """
    def __init__(self, script='username: {username}, password: {passcode}'):
        self.script = script
        self.is_secret = False
        self.account = None

    def initialize(self, account, field_name=None, field_key=None):
        self.account = account

    def __str__(self):
        regex = re.compile(r'({[\w. ]+})')
        out = []
        self.is_secret = False
        for term in regex.split(self.script):
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
                    name, key = self.account.split_field(cmd)
                    value = self.account.get_scalar(name, key)
                    out.append(dedent(str(value)).strip())
                    if self.account.is_secret(name, key):
                        self.is_secret = True
            else:
                out.append(term)
        return ''.join(out)

    def __repr__(self):
        return '%s(%r)' % (self.__class__.__name__, self.script)


# Account class {{{1
class Account(object):
    """Class that holds all the information specific to an account.

    Add desired account information as attributes of the class.
    """

    __NO_MASTER = True
        # prevents master seed from being added to this base class
    _accounts = {}

    # all_accounts() {{{2
    @classmethod
    def all_accounts(cls):
        for sub in cls.__subclasses__():
            # do not yield the base StealthAccount
            if sub != StealthAccount:
                yield sub
            for each in sub.all_accounts():
                yield each

    # get_account() {{{2
    @staticmethod
    def get_account(name):
        canonical = canonicalize(name)
        try:
            return Account._accounts[canonical]
        except KeyError:
            raise PasswordError('account not found.', culprit=name)

    # get_name() {{{2
    @classmethod
    def get_name(cls):
        """Get account name.

        Returns:
            Returns the primary account name. This is generally the class name
            converted to lower case unless it was overridden with the NAME
            attribute.
        """

        try:
            return cls.NAME
        except AttributeError:
            # consider converting lower to upper case transitions in __name__ to
            # dashes.
            return cls.__name__.lower()

    # get_seed() {{{2
    @classmethod
    def get_seed(cls):
        try:
            return cls.seed
        except AttributeError:
            return cls.get_name()

    # override_master() {{{2
    @classmethod
    def request_seed(cls):
        return getattr(cls, '_interactive_seed', False)

    # preprocess() {{{2
    @classmethod
    def preprocess(cls, master, fileinfo, seen):

        # return if this account has already been processed
        if hasattr(cls, '_file_info'):
            return  # don't override on those accounts where it was already set

        # add fileinfo
        cls._file_info = fileinfo

        # add master seed
        if master and not hasattr(cls, '_%s__NO_MASTER' % cls.__name__):
            if not hasattr(cls, 'master'):
                cls.master = master
                cls._master_source = 'file'
            else:
                cls._master_source = 'account'

        # convert aliases to a list
        if hasattr(cls, 'aliases'):
            aliases = list(Collection(cls.aliases))
            cls.aliases = aliases
        else:
            aliases = []

        # canonicalize names and look for duplicates
        new = {}
        account_name = cls.get_name()
        path = cls._file_info.path
        for name in [account_name] + aliases:
            canonical = canonicalize(name)
            Account._accounts[canonical] = cls
            if canonical in seen:
                if name == account_name:
                    warn('duplicate account name.', culprit=name)
                else:
                    warn('alias duplicates existing name.', culprit=name)
                codicil('Seen in %s in %s.' % seen[name])
                codicil('And in %s in %s.' % (account_name, path))
                break
            else:
                new[canonical] = (account_name, path)
        seen.update(new)
            # this two step approach to updating seen prevents us from
            # complaining about aliases that duplicate the account name,
            # or duplicate aliases, both of which are harmless

    # id_contains() {{{2
    @classmethod
    def id_contains(cls, target):
        target = target.lower()
        if target in cls.get_name().lower():
            return True
        try:
            for alias in cls.aliases:
                if target in alias.lower():
                    return True
        except AttributeError:
            pass
        return False

    # account_contains() {{{2
    @classmethod
    def account_contains(cls, target):
        if cls.id_contains(target):
            return True
        target = target.lower()
        for key, value in cls.items():
            try:
                if is_collection(value):
                    for k, v in Collection(value).items():
                        if target in v.lower():
                            return True
                elif target in value.lower():
                    return True
            except AttributeError:
                pass
        return False

    # recognize() {{{2
    @classmethod
    def recognize(cls, data, verbose):
        # try the specified recognizers
        discovery = getattr(cls, 'discovery', ())
        for recognizer in Collection(discovery):
            if isinstance(recognizer, Recognizer):
                script = recognizer.match(data, cls, verbose)
                name = getattr(recognizer, 'name', None)
                if script:
                    yield name, script
        if discovery:
            return

        # If no recognizers specified, just check the urls
        for url in Collection(cls.get_scalar('urls', default=[])):
            url = url if '//' in url else ('//'+url)
            url_components = urlparse(url)
            if url_components.scheme:
                protocol = url_components.scheme
            else:
                protocol = get_setting('default_protocol')
            host = url_components.netloc
            if host == data.get('host'):
                if (protocol == data.get('protocol')):
                    if verbose:
                        log('    %s: matches.' % cls.get_name())
                    yield None, True
                    return
                else:
                    msg = 'url matches, but uses wrong protocol.'
                    notify(msg)
                    raise PasswordError(msg, culprit=cls.get_name())

    # initialize() {{{2
    @classmethod
    def initialize(cls, interactive_seed=False, stealth_name=None):
        cls._interactive_seed = interactive_seed
        log('initializing account:', cls.get_name())
        try:
            if cls.master.is_secure():
                if not cls._file_info.encrypted:
                    warn(
                        'high value master seed not contained in encrypted',
                        'account file.', culprit=cls.get_name()
                    )
        except AttributeError:
            pass
        for bad, good in get_setting('commonly_mistaken_attributes').items():
            if hasattr(cls, bad):
                warn(
                    '{} attribute found,'.format(bad),
                    'should probably be {}.'.format(good),
                    culprit=cls.get_name()
                )

        # do some more error checking
        if isinstance(getattr(cls, 'master', None), GeneratedSecret):
            raise PasswordError(
                'master must not be a subclass of GeneratedSecret.',
                culprit=cls.get_name()
            )

    # keys() {{{2
    @classmethod
    def fields(cls, all=False):
        for field in sorted(cls.__dict__):
            if not field.startswith('_') and (all or field not in TOOL_FIELDS):
                yield field

    # items() {{{2
    @classmethod
    def items(cls, all=False):
        for field in cls.fields(all):
            yield field, getattr(cls, field)

    # get_fields() {{{2
    @classmethod
    def get_fields(cls, all=False):
        """Iterate through fields.

        Iterates through the field names.

        Example::

            for name, keys in account.get_fields():
                if keys:
                    display(name + ':')
                    for key, value in account.get_values(name):
                        display(indent(
                            value.render(('{k}) {d}: {v}', '{k}: {v}'))
                        ))
                else:
                    value = account.get_value(name)
                    display(value.render('{n}: {v}'))

        Args:
            all (bool):
                If False, ignore the tool fields.

        Returns:
            A pair (2-tuple) that contains both field name and the key names.
            None is returned for the key names if the field holds a scalar value.
        """
        for field in sorted(cls.__dict__):
            if not field.startswith('_') and (all or field not in TOOL_FIELDS):
                value = getattr(cls, field)
                if is_collection(value):
                    yield field, Collection(value).keys()
                else:
                    yield field, None

    # get_scalar() {{{2
    @classmethod
    def get_scalar(cls, name, key=None, default=False):
        """Get field Value given a field name and key.

        A lower level interface than *get_value()* that given a name and perhaps
        a key returns a scalar value.  Also takes an optional default value that is
        returned if the value is not found. Unlike *get_value()*, the actual value
        is returned, not a object that contains multiple facets of the value.

        The *name* is the field name, and the *key* would identity which value is
        desired if the field is a composite. If default is False, an error is raised
        if the value is not present, otherwise the default value itself is returned.

        Args:
            name (str):
                The name of the field.
            key (str or int)
                The key for the desired value (should be None for scalar values).
            default:
                The value to return if the requested value is not available.

        Returns:
            The requested value.
        """
        value = getattr(cls, name, None)
        if value is None:
            if name == 'NAME':
                return cls.get_name()
            if default is False:
                raise PasswordError(
                    'field not found.',
                    culprit=(cls.get_name(), cls.combine_field(name, key))
                )
            return default

        if key is None:
            if is_collection(value):
                choices = {}
                for k, v in Collection(value).items():
                    try:
                        desc = v.get_description()
                    except AttributeError:
                        desc = None
                    if desc:
                        choices['   %s: %s' % (k, desc)] = k
                    else:
                        choices['   %s:' % k] = k
                raise PasswordError(
                    'composite value found, need key. Choose from:',
                    *sorted(choices.keys()),
                    sep = '\n',
                    culprit = name,
                    is_collection = True,
                    collection = choices
                )
        else:
            try:
                if is_collection(value):
                    value = value[key]
                else:
                    warn('not a composite value, key ignored.', culprit=name)
                    key = None
            except (IndexError, KeyError, TypeError):
                raise PasswordError(
                    'key not found.', culprit=cls.combine_field(name, key)
                )

        # initialize the value if needed
        try:
            value.initialize(cls, name, key)
                # if Secret or Script, initialize otherwise raise exception
        except AttributeError:
            pass
        return value

    # is_secret() {{{2
    @classmethod
    def is_secret(cls, name, key=None):
        value = cls.__dict__.get(name)
        if key is None:
            return isinstance(value, (GeneratedSecret, ObscuredSecret))
        else:
            try:
                return isinstance(value, (GeneratedSecret, ObscuredSecret))
            except (IndexError, KeyError, TypeError):
                raise PasswordError(
                    'not found.', culprit=cls.combine_field(name, key)
                )

    # split_field() {{{2
    @classmethod
    def split_field(cls, field):
        # Account fields can either be scalars or composites (vectors or
        # dictionaries). This function takes a string or tuple (field) that the
        # user provides to specify which account value they wish and splits it
        # into a name and a key.  If the field is a scalar, the key will be
        # None.  Users request a value using one of the following forms:
        #     True: use default name
        #     field: scalar value (key=None)
        #     index: questions (field->'questions', key=index)
        #     field[index] or field.index: for vector value
        #     field[key] or field.key: for dictionary value

        # handle empty field
        if field is True or field is False or field == '':
            field = None
        if field is None:
            field = cls.get_scalar('default', default=None)

        # convert field into integer if possible
        try:
            field = int(field)
        except (ValueError, TypeError):
            pass

        # separate field into name and key
        if type(field) is tuple:
            # split field if given as a tuple
            if len(field) == 1:
                name, key = field[0], None
            elif len(field) == 2:
                name, key = field[0], field[1]
            else:
                raise PasswordError('too many values.', culprit=field)
        elif is_str(field):
            # split field if given in the form: name[key]
            match = VECTOR_PATTERN.match(field)
            if match:
                name, key = match.groups()
            else:
                # split field if given in the form: name.key
                try:
                    name, key = field.split('.')
                except ValueError:
                    # must be simple name
                    name, key = field, None
        elif field is None:
            # handle defaulting
            defaults = get_setting('default_field').split()
            for default in defaults:
                if hasattr(cls, default):
                    name, key = default, None
                    break
            else:
                raise PasswordError(
                    'no default available, you must request a specific value.',
                    culprit=cls.get_name()
                )
        elif type(field) is int:
            name, key = get_setting('default_vector_field'), int(field)
        else:
            raise PasswordError('invalid field.', culprit=field)

        # look up name and key
        return cls.find_field(name, key)

    # find_field() {{{2
    @classmethod
    def find_field(cls, name, key=None):
        # look up field name while ignoring case and treating - and _ as same
        names = {
            n.replace('-', '_').lower(): n
            for n in cls.__dict__.keys()
            if not n.startswith('_')
        }
        try:
            name = names[name.replace('-', '_').lower()]
        except KeyError:
            raise PasswordError('field not found.', culprit=name)

        # name is now the true field name, now resolve key
        if key is None:
            return name, None
        try:
            return name, int(key)
        except ValueError:
            pass
        try:
            value = getattr(cls, name)
            keys = {
                n.replace('-', '_').lower(): n
                for n in value.keys()
            }
            try:
                key = keys[key.replace('-', '_').lower()]
            except KeyError:
                raise PasswordError('key not found.', culprit=key)
        except AttributeError:
            key = None
        return name, key

    # combine_field() {{{2
    @classmethod
    def combine_field(cls, name, key=None):
        # Inverse of split_field().

        if key is None:
            return name
        else:
            return '%s.%s' % (name, key)

    # get_value() {{{2
    @classmethod
    def get_value(cls, field=None):
        """Get account value.

        Return value from the account given a user friendly identifier or
        script. User friendly identifiers include:

         |  *None*: value of default field
         |  *name*: scalar value
         |  *name.key* or *name[key]*:
         |      member of a dictionary or array
         |      key is string for dictionary, integer for array

        Scripts are simply strings with embedded attributes.
        Ex: *'username: {username}, password: {passcode}'*

        Args:
            field (str):
                Field identifier or script.

        Returns:
            :class:`avendesora.AccountValue`: the desired value.
        """
        # get default if field was not given
        if field is None:
            field = cls.get_scalar('default', default=None)

        # determine whether field is actually a script
        is_script = is_str(field) and '{' in field and '}' in field

        if is_script:
            # run the script
            script = Script(field)
            script.initialize(cls)
            value = str(script)
            is_secret = script.is_secret
            name = key = desc = None
        else:
            name, key = cls.split_field(field)

            value = cls.get_scalar(name, key)
            is_secret = cls.is_secret(name, key)
            try:
                desc = value.get_description()
            except AttributeError:
                desc = None
        return AccountValue(value, is_secret, name, key, desc)

    # get_values() {{{2
    @classmethod
    def get_values(cls, name):
        """Iterate through the values for a field.

        Args:
            name (str):
                The name of the field.

        Returns:
            Returns a pair (2-tuple) that contains the key and the value given
            as an :class:`avendesora.AccountValue` for each of the values.  If
            the value is a scalar, the key is None.
        """
        name, key = cls.find_field(name)
        value = getattr(cls, name, None)
        if value is None:
            if name == 'NAME':
                value = cls.get_name()
            else:
                return

        values = Collection(value, splitter=False)
        for key, val in values.items():
            value = cls.get_scalar(name, key)
            is_secret = cls.is_secret(name, key)
            try:
                desc = value.get_description()
            except AttributeError:
                desc = None
            yield key, AccountValue(value, is_secret, name, key, desc)

    # get_composite() {{{2
    @classmethod
    def get_composite(cls, name):
        """Get field value given a field name.

        A lower level interface than *get_value()* that given a name returns the
        value of the associated field, which may be a scalar (string or integer)
        or a composite (array of dictionary).  Unlike *get_value()*, the actual
        value is returned, not a object that contains multiple facets of the
        value.

        Args:
            name (str):
                The name of the field.

        Returns:
            The requested value.
        """
        value = getattr(cls, name, None)
        if value is None:
            if name == 'NAME':
                return cls.get_name()
            return None

        if is_collection(value):
            if type(value) is dict:
                result = {}
                for key in value.keys():
                    v = cls.get_scalar(name, key)
                    if isinstance(v, GeneratedSecret) or isinstance(v, ObscuredSecret):
                        v = str(v)
                    result[key] = v
            elif type(value) is list:
                result = []
                for index in range(len(value)):
                    v = cls.get_scalar(name, index)
                    if isinstance(v, GeneratedSecret) or isinstance(v, ObscuredSecret):
                        v = str(v)
                    result.append(v)
            else:
                raise NotImplementedError
        else:
            result = cls.get_scalar(name)
            if isinstance(result, GeneratedSecret) or isinstance(result, ObscuredSecret):
                result = str(result)
        return result

    # write_summary() {{{2
    @classmethod
    def write_summary(cls):
        # present all account values that are not explicitly secret to the user

        def fmt_field(key, value='', level=0):
            if '\n' in value:
                value = indent(dedent(value), get_setting('indent')).strip('\n')
                sep = '\n'
            elif value:
                sep = ' '
            else:
                sep = ''
            key = str(key).replace('_', ' ')
            leader = level*get_setting('indent')
            return indent(LabelColor(key + ':') + sep + value, leader)

        def reveal(name, key=None):
            return "<reveal with 'avendesora value %s %s'>" % (
                cls.get_name(), cls.combine_field(name, key)
            )

        def extract_collection(name, collection):
            lines = [fmt_field(key)]
            for k, v in Collection(collection).items():
                if isinstance(v, (GeneratedSecret, ObscuredSecret)):
                    # is a secret, get description if available
                    v = ' '.join(cull([v.get_description(), reveal(name, k)]))
                lines.append(fmt_field(k, v, level=1))
            return lines

        # preload list with the names associated with this account
        names = [cls.get_name()] + getattr(cls, 'aliases', [])
        lines = [fmt_field('names', ', '.join(names))]

        for key, value in cls.items():
            if is_collection(value):
                lines += extract_collection(key, value)
            elif hasattr(value, 'script'):
                lines.append(fmt_field(key, '<%s>' % value.script))
            elif cls.is_secret(key):
                lines.append(fmt_field(key, reveal(key)))
            else:
                lines.append(fmt_field(key, value))
        output(*lines, sep='\n')

    # archive() {{{2
    @classmethod
    def archive(cls):
        # return all account fields along with their values as a dictionary

        def extract(value, name, key=None):
            if not is_collection(value):
                if hasattr(value, 'initialize'):
                    value.initialize(cls, name, key)
                return value
            try:
                return {k: extract(v, name, k) for k, v in value.items()}
            except AttributeError:
                return [extract(v, name, i) for i, v in enumerate(value)]

        return {k: extract(v, k) for k, v in cls.items(True) if k != 'master'}

    # open_browser() {{{2
    @classmethod
    def open_browser(cls, key=None, browser_name=None, list_urls=False):
        if not browser_name:
            browser_name = cls.get_scalar('browser', default=None)
        browser = StandardBrowser(browser_name)

        # get the urls from the urls attribute
        # this must be second so it overrides those from recognizers.
        primary_urls = getattr(cls, 'urls', [])
        if type(primary_urls) != dict:
            if is_str(primary_urls):
                primary_urls = primary_urls.split()
            primary_urls = {None: primary_urls} if primary_urls else {}

        # get the urls from the url recognizers
        discovery = getattr(cls, 'discovery', ())
        urls = {}
        for each in Collection(discovery):
            urls.update(each.all_urls())

        # combine, primary_urls must be added to urls, so they dominate
        urls.update(primary_urls)

        # select the urls
        if not key:
            key = getattr(cls, 'default_url', None)
        try:
            urls = urls[key]
        except KeyError:
            keys = cull(urls.keys())
            if keys:
                if key:
                    msg = 'unknown key, choose from {}.'
                else:
                    msg = 'key required, choose from {}.'
                raise PasswordError(msg.format(conjoin(keys)), culprit=key)
            else:
                raise PasswordError(
                    'keys are not supported with urls on this account.',
                    culprit=key
                )

        # open the url
        if list_urls:
            for url in urls:
                output(url)
        else:
            url = list(Collection(urls))[0]  # use the first url specified
            browser.run(url)

    # has_field() {{{2
    @classmethod
    def has_field(cls, name):
        return name in dir(cls)

    # get_username() {{{2
    @classmethod
    def get_username(cls):
        """Get the username.

        Like *get_value()*, but tries the *credential_ids* in order and returns
        the first found. *credential_ids* is an Avendesora configuration setting
        that by default is *username* and *email*.

        Returns:
            The username or email address.
        """
        identities = Collection(get_setting('credential_ids'))
        for identity in identities:
            try:
                return cls.get_value(identity)
            except PasswordError:
                pass

    # get_passcode() {{{2
    @classmethod
    def get_passcode(cls):
        """Get the passcode.

        Like *get_value()*, but tries the *credential_secrets* in order and returns
        the first found. *credential_secrets* is an Avendesora configuration setting
        that by default is *password*, *passphrase*, and *passcode*.

        Returns:
            The passcode.
        """
        secrets = Collection(get_setting('credential_secrets'))
        for passcode in secrets:
            try:
                return cls.get_value(passcode)
            except PasswordError:
                pass


# StealthAccount class {{{1
class StealthAccount(Account):
    """Empty account that defines how to generate a secret.

    With stealth accounts the actual account name is requested directly from the
    user. Only one attribute is generally given for stealth accounts, which is
    suitable as a default such as password, passphrase or passcode, and that
    contains the method for generating the desired secret based on the account
    name and the master seed in the stealth_accounts file.
    """

    __NO_MASTER = True
        # prevents master password from being added to this base class

    # initialize() {{{2
    @classmethod
    def initialize(cls, interactive_seed=False, stealth_name=None):
        cls._interactive_seed = interactive_seed
        cls.stealth_name = stealth_name
        log('initializing stealth account:', cls.get_name())
        for key, value in cls.items():
            # reset the secrets so they honor stealth_name
            try:
                value.reset()
            except AttributeError:
                pass

    @classmethod
    def get_seed(cls):
        if cls.stealth_name:
            # In this case we are running using API rather than running from
            # command line and the account names was specified to get_account().
            return cls.stealth_name
        # need to handle case where stdin/stdout is not available.
        # perhaps write generic password getter that supports both gui and tui.
        # Then have global option that indicates which should be used.
        # Separate name from seed. Only request seed when generating a password.
        import getpass
        try:
            name = getpass.getpass('account name: ')
        except EOFError:
            output()
            name = ''
        if not name:
            warn('null account name.')
        return name

    @classmethod
    def archive(cls):
        # do not archive stealth accounts
        pass
