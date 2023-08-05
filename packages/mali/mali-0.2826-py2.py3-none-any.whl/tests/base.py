# -*- coding: utf8 -*-
import random
import string
import unittest

import httpretty
import logging


class Expando(object):
    def __init__(self, *args, **kw):
        self.__dict__.update(kw)


def global_some_random_shit(chars=string.ascii_lowercase + string.digits, size=8):
    return ''.join(random.choice(chars) for _ in range(size))


class BaseTest(unittest.TestCase):
    # class variable used by jmock style calls
    sharedController = None
    # so that nosetests run
    context = None

    def __init__(self, methodName=''):
        self.route_logging_stdout()

        super(BaseTest, self).__init__(methodName)
        self.datastore_probability = 1

    def setUp(self):
        super(BaseTest, self).setUp()

        httpretty.HTTPretty.allow_net_connect = False

        logging.debug('test setup')

    def tearDown(self):
        logging.debug('test tearDown')

        httpretty.HTTPretty.allow_net_connect = True

        super(BaseTest, self).tearDown()

    @classmethod
    def some_random_shit_number_int63(cls):
        return random.getrandbits(63)

    @classmethod
    def some_random_shit(cls, chars=string.ascii_lowercase + string.digits, size=8):
        return global_some_random_shit(chars, size)

    @classmethod
    def some_random_shit_alpha(cls, chars=string.ascii_lowercase, size=8):
        return global_some_random_shit(chars, size)

    @classmethod
    def some_random_float(cls, inclusive_lower=0.0, exclusive_upper=1.0, decimal_digits=10):
        scale = 10 ** decimal_digits
        inclusive_lower = inclusive_lower * scale
        exclusive_upper = exclusive_upper * scale
        return random.randint(inclusive_lower, exclusive_upper - 1) * 1.0 / scale

    @classmethod
    def some_random_sha_hash(cls):
        return cls.some_random_shit(chars=string.hexdigits, size=40)

    @classmethod
    def route_logging_stdout(cls):
        logging.basicConfig(level=logging.WARNING)
        # logging.getLogger().setLevel(logging.DEBUG)
        # import sys
        # logging.basicConfig(stream=sys.stdout)
        # logging.getLogger().setLevel(logging.DEBUG)


class BaseCliTest(BaseTest):
    def setUp(self):
        from mali import add_commands

        super(BaseCliTest, self).setUp()

        add_commands()
