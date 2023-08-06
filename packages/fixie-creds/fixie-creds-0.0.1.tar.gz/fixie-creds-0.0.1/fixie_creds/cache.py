"""Represents a credentials cache that is backed by the file system. This cache
is the underlying registration and verification engine for credentials.

Importantly, while the credtials may generate a token for a user, that token is
NEVER stored. Instead, the hash of the token is stored.  Verification compares
the hash of token provided by the user to the stored hashed token.
"""
import os
import json
import random
import hashlib
from collections import namedtuple

from fixie.environ import expand_and_make_dir

from fixie.environ import ENV


User = namedtuple('User', ['user', 'email', 'hashed_token'])


class Cache:
    """A cache for fixie credentials."""

    __inst = None

    def __new__(cls):
        # make the cache a singleton
        if Cache.__inst is None:
            Cache.__inst = object.__new__(cls)
        return Cache.__inst

    def __init__(self, credsdir=None, seed=None, nbytes=20):
        """
        Parameters
        ----------
        credsdir : str or None, optional
            Path to credentials directory, if None, defaults to $FIXIE_CREDS_DIR.
        seed : int, bytes, or None, optional
            Value to seed to Pythons RNG. This is provided for testing purpose,
            For production, this should be set to None so that reseeding is
            done based on system time and other parameters.
        nbytes : int, optional
            Number of bits to use when generating for tokens.
        """
        random.seed(seed)
        self.nbytes = nbytes
        self.nbits = nbytes * 8
        self._credsdir = None
        self._dirty = True
        self._users = {}  # maps usernames to named tuples of
        self.credsdir = credsdir

    @property
    def credsdir(self):
        value = self._credsdir
        if value is None:
            value = ENV['FIXIE_CREDS_DIR']
        return value

    @credsdir.setter
    def credsdir(self, value):
        self._dirty = True
        self._users.clear()
        if value is None:
            self._credsdir = value
        else:
            self._credsdir = expand_and_make_dir(value)

    def user_cred_file(self, user):
        """Returns the credential filename for a user."""
        return os.path.join(self.credsdir, user + '.json')

    def user_exists(self, user):
        """Returns whether or not a user exists (ie has been registered)."""
        if user in self._users:
            return True
        return os.path.isfile(self.user_cred_file(user))

    def hash_token(self, token):
        """Hashes a token."""
        i = int(token, 16)
        b = i.to_bytes(self.nbytes, 'little')
        h = hashlib.sha256(b)
        return h.hexdigest()

    def write_user(self, user, email, hashed_token):
        """Writes a user's credential file."""
        data = {'user': user, 'email': email, 'hashed_token': hashed_token}
        fname = self.user_cred_file(user)
        with open(fname, 'w') as f:
            json.dump(data, f, sort_keys=True, separators=(',', ':'))
        os.chmod(fname, 0o600)
        self._users[user] = User(**data)

    def load_user(self, user):
        """Loads a user into the cache from the filesystem."""
        fname = self.user_cred_file(user)
        with open(fname, 'r') as f:
            data = json.load(f)
        u = self._users[data['user']] = User(**data)
        return u

    def get_user(self, user):
        """Returns the user, loading it from the file system if needed."""
        u = self._users.get(user, None)
        if u is None:
            u = self.load_user(user)
        return u

    def remove_user(self, user):
        """Remove the user from the cache and the file system."""
        self._users.pop(user)
        fname = self.user_cred_file(user)
        if os.path.isfile(fname):
            os.remove(fname)

    def register(self, user, email):
        """Registers a new user and provides their token.

        Parameters
        ----------
        user : str
            Name of the user to register.
        email : str
            Email address for the user.

        Returns
        -------
        token or message : str
            The token if the registration was successful, and an error message
            if it wasn't.
        flag : bool
            Whether or not the registration was successful.
        """
        if self.user_exists(user):
            return 'User {0!r} already registered'.format(user), False
        token = hex(random.getrandbits(self.nbits))[2:]
        hashed_token = self.hash_token(token)
        self.write_user(user, email, hashed_token)
        return token, True

    def verify(self, user, token):
        """Verifies whether or not the user-token pair match.

        Parameters
        ----------
        user : str
            Name of the user.
        token : str
            The token to verify for the user.

        Returns
        -------
        verified : bool
            Whether or not the user-token pair is valid.
        message : str
            A message string, if needed.
        flag : bool
            Whether or not the verification itself could be completed successfully.
        """
        if not self.user_exists(user):
            return False, 'User {0!r} not registered'.format(user), False
        u = self.get_user(user)
        hashed_token = self.hash_token(token)
        valid = (hashed_token == u.hashed_token)
        msg = 'User verified' if valid else 'Invalid token for user ' + user
        return valid, msg, True

    def deregister(self, user, token):
        """Deregisters a user.

        Parameters
        ----------
        user : str
            Name of the user to deregister.
        token : str
            The user's token

        Returns
        -------
        message : str
            Message for status of deregistration
        flag : bool
            Whether or not the deregistration was successful.
        """
        valid, msg, flag = self.verify(user, token)
        if not valid or not flag:
            return msg, False
        self.remove_user(user)
        return user + ' deregistered', True

    def reset(self, user, email):
        """Resets a user's token on the system. The email address here must match
        the one originally provided.

        Parameters
        ----------
        user : str
            Name of the user to register.
        email : str
            Email address for the user.

        Returns
        -------
        token or message : str
            The token if the registration was successful, and an error message
            if it wasn't.
        flag : bool
            Whether or not the registration was successful.
        """
        if not self.user_exists(user):
            return 'User {0!r} not registered'.format(user), False
        u = self.get_user(user)
        if email != u.email:
            return 'User email does not match registered email address', False
        self.remove_user(user)
        token, flag = self.register(user, email)
        return token, flag


CACHE = Cache()
