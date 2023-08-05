from __future__ import print_function

import logging
import sys

log = logging.getLogger('dmoj.cptbox')


def print_protection_fault(fault, stream=sys.stderr):
    syscall, callname, args = fault
    log.warning('Protection fault on: %d (%s)', syscall, callname)
    print('Protection fault on: %d (%s)' % (syscall, callname), file=stream)
    for i, arg in enumerate(args):
        log.info('Arg%d: 0x%016x', i, arg)
        print('Arg%d: 0x%016x' % (i, arg), file=stream)
