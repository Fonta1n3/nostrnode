#!/usr/bin/env python3
# Copyright (c) 2015-2021 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from base64 import urlsafe_b64encode
from os import urandom

import hmac


def generate_salt(size):
    """Create size byte hex salt"""
    return urandom(size).hex()


def generate_password():
    """Create 32 byte b64 password"""
    return urlsafe_b64encode(urandom(32)).decode('utf-8')


def password_to_hmac(salt, password):
    m = hmac.new(bytearray(salt, 'utf-8'), bytearray(password, 'utf-8'), 'SHA256')
    return m.hexdigest()


def main():
    # Create 16 byte hex salt
    password = generate_password()
    salt = generate_salt(16)
    password_hmac = password_to_hmac(salt, password)

    return (password, 'rpcauth={0}:{1}${2}'.format('nostrnode', salt, password_hmac))


if __name__ == '__main__':
    main()