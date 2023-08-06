import linecache
import random

name_file = 'resource/name.txt'
email_file = 'resource/email.txt'
IDcard_file = 'resource/IDcard.txt'
phone_file = 'resource/phone.txt'
username_file = 'resource/username.txt'
address_file = 'resource/address.txt'


def _make_gen(reader):
    b = reader(1024 * 1024)
    while b:
        yield b
        b = reader(1024*1024)


def rawpycount(filename):
    f = open(filename, 'rb')
    f_gen = _make_gen(f.raw.read)
    return sum( buf.count(b'\n') for buf in f_gen )


def getfile(filename, length=1):
    linenum = rawpycount(filename)
    result = set()
    while len(result)<length:
        tmp = linecache.getline(filename, random.randrange(1, linenum, 1)).strip()
        result.add(tmp)
    return result


def name(length=1):
    return getfile(name_file, length=length)


def email(length=1):
    return getfile(email_file, length=length)


def ID(length=1):
    return getfile(IDcard_file, length=length)


def phone(length=1):
    return getfile(phone_file, length=length)


def username(length=1):
    return getfile(username_file, length=length)


def address(length=1):
    return getfile(address_file, length=length)