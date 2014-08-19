#!/usr/bin/env python2

import glutabbix
from glutabbix import Glutabbix
import doctest

if __name__ == '__main__':
    nfail, ntests = doctest.testmod(glutabbix)

