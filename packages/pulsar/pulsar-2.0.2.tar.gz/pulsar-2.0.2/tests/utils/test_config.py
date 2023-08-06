'''Config and Setting classes'''
import os
import sys
import pickle
import tempfile
import traceback
import unittest

from pulsar.api import get_actor
from pulsar.utils import system
from pulsar.utils.config import (
    validate_callable, pass_through, validate_list, validate_bool,
    validate_pos_int, validate_pos_float, validate_dict, validate_string
)

from tests.utils import config, post_fork


class TestConfig(unittest.TestCase):

    def testFunction(self):
        cfg = config()
        worker = get_actor()
        self.assertTrue(cfg.post_fork)
        self.assertEqual(cfg.post_fork(worker), None)
        cfg.set('post_fork', post_fork)
        self.assertEqual(cfg.post_fork(worker), worker)
        cfg1 = pickle.loads(pickle.dumps(cfg))
        self.assertEqual(cfg1.post_fork(worker), worker)

    def testFunctionFromConfigFile(self):
        worker = get_actor()
        cfg = config()
        self.assertEqual(cfg.connection_made(worker), None)
        module_name = 'tests.utils'
        self.assertEqual(cfg.import_from_module(module_name)[0],
                         ('foo', 5))
        self.assertEqual(cfg.connection_made(worker), worker)
        cfg1 = pickle.loads(pickle.dumps(cfg))
        self.assertEqual(cfg1.connection_made(worker), worker)

    def testBadConfig(self):
        cfg = config()
        self.assertEqual(cfg.config, 'config.py')
        self.assertEqual(cfg.import_from_module('foo/bla/cnkjnckjcn.py'), [])
        cfg.set('config', None)
        self.assertEqual(cfg.config, None)

    def test_exclude(self):
        cfg = config(exclude=['config'])
        self.assertEqual(cfg.config, 'config.py')
        self.assertEqual(cfg.params['config'], 'config.py')
        self.assertFalse('config' in cfg.settings)

    def testDefaults(self):
        self.assertFalse(pass_through(None))
        cfg = config()
        self.assertEqual(list(sorted(cfg)), list(sorted(cfg.settings)))

        def _():
            cfg.debug = 3
        self.assertRaises(AttributeError, _)
        #
        name = tempfile.mktemp()
        with open(name, 'w') as f:
            f.write('a')
        self.assertRaises(RuntimeError, cfg.import_from_module, name)
        os.remove(name)
        #
        name = '%s.py' % name
        with open(name, 'w') as f:
            f.write('a')
        self.assertRaises(RuntimeError, cfg.import_from_module, name)
        os.remove(name)

    def testSystem(self):
        cfg = config()
        self.assertEqual(cfg.uid, system.get_uid())
        self.assertEqual(cfg.gid, system.get_gid())
        self.assertEqual(cfg.proc_name, 'pulsar')
        cfg.set('process_name', 'bla')
        self.assertEqual(cfg.proc_name, 'bla')

    def testValidation(self):
        self.assertEqual(validate_list((1, 2)), [1, 2])
        self.assertRaises(TypeError, validate_list, 'bla')
        self.assertEqual(validate_string(' bla  '), 'bla')
        self.assertEqual(validate_string(None), None)
        self.assertRaises(TypeError, validate_string, [])
        self.assertEqual(validate_bool(True), True)
        self.assertEqual(validate_bool('true '), True)
        self.assertEqual(validate_bool(' false'), False)
        self.assertRaises(TypeError, validate_bool, [])
        self.assertRaises(ValueError, validate_bool, 'foo')
        self.assertRaises(ValueError, validate_pos_int, 'foo')
        self.assertRaises(ValueError, validate_pos_int, -1)
        self.assertRaises(ValueError, validate_pos_float, 'foo')
        self.assertRaises(ValueError, validate_pos_float, -0.001)
        self.assertEqual(validate_pos_float('0.101'), 0.101)
        self.assertRaises(TypeError, validate_dict, 4)

    def test_validate_callable(self):
        self.assertRaises(TypeError, validate_callable(1), None)
        self.assertRaises(TypeError, validate_callable(1), 4)
        self.assertRaises(TypeError, validate_callable(1), object())

        class test1:
            def __call__(self, arg):
                pass

        class test2:
            def __call__(self, arg1, arg2=None):
                pass

        test = test1()
        self.assertEqual(validate_callable(1)(test), test)
        self.assertRaises(TypeError, validate_callable(2), test)
        test = test2()
        self.assertEqual(validate_callable(1)(test), test)
        self.assertEqual(validate_callable(2)(test), test)
        self.assertRaises(TypeError, validate_callable(3), test)

    def test_methods(self):
        cfg = config()
        self.assertEqual(cfg.get('sdjcbsjkbcd', 'ciao'), 'ciao')
        d = dict(cfg.items())
        self.assertEqual(len(d), len(cfg))
        sett = cfg.get('debug')
        self.assertTrue(str(sett))
        self.assertEqual(cfg.settings['debug'].default, False)
        cfg.set('debug', True, default=True)
        self.assertEqual(cfg.debug, True)
        self.assertEqual(cfg.settings['debug'].default, True)

    def test_attribute_error(self):
        cfg = config()
        self.assertRaises(AttributeError, lambda: cfg.wwwwww)
        # Check KeyError not in stacktrace
        try:
            cfg.aaa
        except AttributeError:
            stack = '\n'.join(traceback.format_tb(sys.exc_info()[2]))
        self.assertFalse('KeyError' in stack)
