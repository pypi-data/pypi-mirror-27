from .account import Account, StealthAccount, Script, AccountValue
from .charsets import (
    exclude, LOWERCASE, UPPERCASE, LETTERS, DIGITS, ALPHANUMERIC,
    HEXDIGITS, PUNCTUATION, SYMBOLS, WHITESPACE, PRINTABLE, DISTINGUISHABLE
)
from .error import PasswordError
from .generator import PasswordGenerator
from .obscure import Hide, Hidden, GPG
try:
    from .obscure import Scrypt
except ImportError:  # no cover
    pass
from .recognize import (
    RecognizeAll, RecognizeAny, RecognizeTitle, RecognizeURL, RecognizeCWD,
    RecognizeHost, RecognizeUser, RecognizeEnvVar, RecognizeNetwork,
    RecognizeFile
)
from .secrets import (
    Password, Passphrase, PIN, Question, MixedPassword, PasswordRecipe,
    BirthDate, SecretExhausted
)

# the following are used when generating the documentation and are not needed
# otherwise
from . import command

__version__ = '1.8.0'
__released__ = '2017-11-23'
