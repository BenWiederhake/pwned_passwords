# pwned_passwords

> Tells you which passwords have been pwned

This little tools reads passwords (or any arbitrary strings) from stdin, and checks them against [haveibeenpwned.com](https://haveibeenpwned.com/), or more precisely it's API at https://api.pwnedpasswords.com.

Includes rate-limiting, randomized order, response padding, and a free unicorn.

<!-- Here is the unicorn: 🦄 -->

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [TODOs](#todos)
- [NOTDOs](#notdos)
- [Contribute](#contribute)

## Install

If you don't already have it installed, run `pip install -U requests`. Or if you prefer, run
`pip3 install -r requirements.txt`. Or something along those lines. You probably already have it
installed anyway.

## Usage

You can run it in the terminal and enter passwords by hand:

```
$ ./pwned_passwords.py 
# Paste your passwords here, or pipe them in.
# Remember to terminate input, e.g. by Ctrl-D.
MyPassword
so95gz8elaiuewrhaosirh
^D
# Processing 2 passwords now.
# Due to rate-limiting, this may take a while.
# Done!
# Password pwned: MyPassword
# 2 passwords checked, 1 of which are pwned.
```

(The `^D` only indicate the time at which I pressed control-d. These characters will probably not appear on your screen.)

Or you can feed something else to it:

```
$ ./pwned_passwords.py < ~/Dropbox/throwaway_passwords.txt 
# Paste your passwords here, or pipe them in.
# Remember to terminate input, e.g. by Ctrl-D.
# Processing 2 passwords now.
# Due to rate-limiting, this may take a while.
# Done!
# Password pwned: MyPassword
# 2 passwords checked, 1 of which are pwned.
```

Obviously, you should clear the terminal after typing it by hand.

## TODOs

I'm mostly happy with the tool.

I want to:
* Keep it up to date
* Maybe add something so that my personal `throwaway_passwords.txt` is checked regularly?
* Make it even easier to audit?

## NOTDOs

Here are some things this project will definitely not support:
* Dummy requests (What for? just inject it into your source then!)
* Avoiding the rate-limiting (Be a nice netizen!)
* Be more performant (Because performance doesn't matter here)
* Exception handling (The user is probably a Big Boy/Girl/Programmer/Dinosaur and should try to understand the error themselves)

## Contribute

Feel free to dive in! [Open an issue](https://github.com/BenWiederhake/pwned_passwords/issues/new) or submit PRs.
