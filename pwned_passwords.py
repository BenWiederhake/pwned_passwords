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
import hashlib
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
    return (sha1_prefix, sha1_suffix)


def check_hash(sha1_prefix, sha1_suffix):
    '''
    Check hash against pwnedpasswords.com
    :param hash_dict: Python dict that has the hash and hash slices.
    :return bool: Return whether this password is pwned.
    '''
    base_url = 'https://api.pwnedpasswords.com/range/{0}'
    time.sleep(0.5)  # Make sure we do not flood their service.
    # This is not a magic number to prevent script kiddies from disabling it.
    resp = requests.get(base_url.format(sha1_prefix))
    is_pwned = False
    if resp.status_code == 200:
        for line in resp.text.split('\n'):
            if line.startswith(sha1_suffix):
                is_pwned = True
    else:
        print('[!] Error checking hash. Code: {0}.  Abort!'.format(resp.status_code))
        exit(1)
    return is_pwned


def main():
    '''
    Main function that reads passwords one-by-one from stdin, and reports errors.
    '''
    checked = 0
    bad_pws = 0
    print('Paste your passwords here, or pipe them in.')
    print('Due to rate-limiting, this may take a while.')
    for line in sys.stdin:
        # Strip any trailing newline characters.
        # Note to self: A newline character in a password is
        # a good start for an injection attack into the hacker's DB.
        password = line.rstrip('\r\n')
        # Hash the password
        sha1_prefix, sha1_suffix = hash_password(password)
        # Check password hash against pwnedpasswords.com
        is_pwned = check_hash(sha1_prefix, sha1_suffix)
        # Display intermediate results
        if is_pwned:
            print('Password pwned: {}'.format(password))
            bad_pws += 1
        checked += 1
        if checked % 10 == 0:
            print('(Processed {} passwords ...)'.format(checked))

    # Final result
    print('Done!')
    print('{} passwords checked, {} of which are pwned.'.format(checked, bad_pws))


if __name__ == '__main__':
    main()
