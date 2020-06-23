#!/usr/bin/env python3
# coding=utf-8
#
# Check to see if a password shows up on Troy Hunt's
# V2 update to Pwned Passwords, and if so, how many
# times.
#
# Todo: add exception handling
#
# Strongly influenced by https://github.com/zenone/pwned_passwords/


########################################
# Imports
import collections
import hashlib
import random
import requests
import sys
import time


########################################
# Functions

def hash_password(password):
    '''
    Create a sha1 hash of the password.
    :param password: String passed in by the user to be hashed and sliced.
    :return tuple: Return the slices of the password hash.
    '''
    sha1 = hashlib.sha1()
    sha1.update(password.encode('utf-8'))
    sha1_hexdigest = sha1.hexdigest().upper()
    sha1_prefix = sha1_hexdigest[0:5]
    sha1_suffix = sha1_hexdigest[5:]
    return (sha1_prefix, sha1_suffix, password)


def fetch_suffixes(sha1_prefixes):
    '''
    Check hash against pwnedpasswords.com
    '''
    sha1_prefixes = list(set(sha1_prefixes))  # Avoid duplicate requests
    random.shuffle(sha1_prefixes)  # Don't leak any order
    base_url = 'https://api.pwnedpasswords.com/range/{0}'
    pwned_suffixes = dict()
    for prefix in sha1_prefixes:
        time.sleep(1)  # Make sure we do not flood their service.
        # Prevent catastrophically wrong usage:
        assert len(prefix) == 5 and prefix.isalnum()
        query_url = base_url.format(prefix)
        # In case you want extra transparency:
        #print(query_url)
        resp = requests.get(query_url, headers={'Add-Padding': 'true'})
        if resp.status_code != 200:
            print('[!] Error checking hash. Code: {0}.  Abort!'.format(resp.status_code))
            exit(1)
        suffixes = set()
        for line in resp.text.split('\n'):
            if line == '':
                continue
            suffix = line[:35]
            assert len(suffix) == 35 and suffix.isalnum(), suffix
            suffixes.add(suffix)
        pwned_suffixes[prefix] = suffixes
    return pwned_suffixes


def check_bulk(passwords):
    hashes = [hash_password(pw) for pw in passwords]
    pwned_suffixes = fetch_suffixes(h[0] for h in hashes)
    return [h[2] for h in hashes if h[1] in pwned_suffixes[h[0]]]


def main():
    '''
    Main function that reads passwords one-by-one from stdin, and reports errors.
    '''
    # Fetch input
    passwords = []
    print('# Paste your passwords here, or pipe them in.')
    print('# Remember to terminate input, e.g. by Ctrl-D.')
    for line in sys.stdin:
        # Strip any trailing newline characters.
        passwords.append(line.rstrip('\r\n'))

    # Do the checks
    print('# Processing {} passwords now.'.format(len(passwords)))
    print('# Due to rate-limiting, this may take a while.')
    bad_pws = check_bulk(passwords)

    # Final result
    print('# Done!')
    for bad_pw in bad_pws:
        print('# Password pwned: {}'.format(bad_pw))
    print('# {} passwords checked, {} of which are pwned.'.format(len(passwords), len(bad_pws)))


if __name__ == '__main__':
    main()
