#testutil.py

import unittest
import logging
import stackless
import time
import contextlib

from stacklesslib import main, app, util
from stacklesslib.errors import TimeoutError, CancelledError


class TestTaskletCallNew(unittest.TestCase):
    def dispatcher(self):
        return util.tasklet_new

    def testResult(self):
        def func(result):
            return result, result
        v = 1, 2, 3
        self.assertEqual(util.tasklet_call(lambda:func(v), dispatcher=self.dispatcher()), (v, v))

    def testException(self):
        def func(e):
            raise e
        e = ZeroDivisionError
        self.assertRaises(e, util.tasklet_call, lambda:func(e), dispatcher=self.dispatcher())

    def testTasklets(self):
        def func():
            return stackless.getcurrent()

        other = util.tasklet_call(func, dispatcher=self.dispatcher())
        self.assertNotEqual(other, stackless.getcurrent())

    def testTimeout(self):
        def func():
            return main.sleep(0.1)
        self.assertRaises(TimeoutError, util.tasklet_call, func, dispatcher=self.dispatcher(), timeout=0.01)

    def testCancel(self):
        def func():
            me = stackless.getcurrent()
            def killer():
                me.kill()
            stackless.tasklet(killer)()
            return main.sleep(0.1)
        self.assertRaises(CancelledError, util.tasklet_call, func, dispatcher=self.dispatcher(), timeout=0.01)

class TestTaskletCallRun(TestTaskletCallNew):
    def dispatcher(self):
        return util.tasklet_run


class TestCancellable(unittest.TestCase):

    def testCancel(self):
        handle = util.cancellable()
        c = stackless.channel()

        def foo():
            with handle:
                c.receive()

        def cancellor(handle):
            handle.cancel("foo", "bar")
        t = stackless.tasklet(cancellor)(handle)
        self.assertRaises(CancelledError, foo)


    def testCancelled(self):
        handle = util.cancellable()
        c = stackless.channel()

        def foo():
            with handle:
                c.receive()

        def cancellor(handle):
            self.assertFalse(handle.cancelled())
            handle.cancel("foo", "bar")
            self.assertTrue(handle.cancelled())

        self.assertFalse(handle.cancelled())
        t = stackless.tasklet(cancellor)(handle)
        self.assertRaises(CancelledError, foo)
        self.assertTrue(handle.cancelled())


    def testCancelSelf(self):
        handle = util.cancellable()
        c = stackless.channel()

        def foo():
            with handle:
                handle.cancel()
        self.assertRaises(CancelledError, foo)


    def testCancelArgs(self):
        handle = util.cancellable()
        c = stackless.channel()
        def foo():
            with handle:
                c.receive()
        def cancellor(handle):
            handle.cancel("foo", "bar")
        t = stackless.tasklet(cancellor)(handle)
        try:
            foo()
        except CancelledError as e:
            self.assertEqual(e.args, ("foo", "bar"))

    def testCancelMatch(self):
        handle = util.cancellable()
        c = stackless.channel()
        def foo():
            with handle:
                c.receive()
        def cancellor(handle):
            handle.cancel("foo", "bar")
        t = stackless.tasklet(cancellor)(handle)
        try:
            foo()
        except CancelledError as e:
            self.assertTrue(handle.match(e))

    def testCancelMatchFail(self):
        handle1 = util.cancellable()
        handle2 = util.cancellable()
        c = stackless.channel()
        def foo():
            with handle1:
                with handle2:
                    c.receive()
        def cancellor(handle):
            handle.cancel("foo", "bar")
        t = stackless.tasklet(cancellor)(handle2)
        try:
            foo()
        except CancelledError as e:
            self.assertFalse(handle1.match(e))
            self.assertTrue(handle2.match(e))

    def testCancelMatchFail2(self):
        handle1 = util.cancellable()
        handle2 = util.cancellable()
        c = stackless.channel()
        def foo():
            #with handle1:
                with handle2:
                    c.receive()
        def cancellor(handle):
            handle.cancel("foo", "bar")
        t = stackless.tasklet(cancellor)(handle2)
        try:
            foo()
        except CancelledError as e:
            self.assertFalse(handle1.match(e))
            self.assertTrue(handle2.match(e))

    def testCancelMatchFail3(self):
        handle1 = util.cancellable()
        handle2 = util.cancellable()
        c = stackless.channel()
        def foo():
            with handle1:
                with handle2:
                    c.receive()
        def cancellor(handle):
            handle.cancel("foo", "bar")
        t = stackless.tasklet(cancellor)(handle1)
        try:
            foo()
        except CancelledError as e:
            self.assertFalse(handle2.match(e))
            self.assertTrue(handle1.match(e))

    def testCancelFail(self):
        handle = util.cancellable()
        handle.cancel()
        self.assertFalse(handle.cancelled())

    def testCancelFail2(self):
        handle = util.cancellable()
        def foo():
            with handle:
                return
        foo()
        handle.cancel()
        self.assertFalse(handle.cancelled())

    def testCancelMatchFail4(self):
        handle = util.cancellable()
        self.assertFalse(handle.match(CancelledError()))
        self.assertFalse(handle.match(CancelledError))
        self.assertFalse(handle.match(1))
        self.assertFalse(handle.match("fpp"))
        self.assertFalse(handle.match(None))

    def testSelf(self):
        handle = util.cancellable()
        with handle as h:
            self.assertTrue(handle is h)

class test_QueueChannel(unittest.TestCase):
    def setUp(self):
        self.c = util.QueueChannel()

    def test_create(self):
        pass

    def test_send(self):
        #sending on a QueueChannel isn't blocking
        self.c.send(1)
        self.c.send(2)
        self.assertEqual(self.c.receive(), 1)
        self.assertEqual(self.c.receive(), 2)

    def test_receive(self):
        #receiving on a QueueChannel blocks
        r = []
        def f():
            for i in range(10):
                r.append(self.c.receive())

        self.c.send(0)
        self.c.send(1)
        t = stackless.tasklet(f)()
        t.run()
        self.assertEqual(r, range(2))
        self.c.send(2)
        self.assertEqual(r, range(3))
        for i in range(3, 10):
            self.c.send(i)
        self.assertEqual(r, range(10))


class test_bounded_QueueChannel(test_QueueChannel):
    def setUp(self):
        self.c = util.QueueChannel(3)


    def test_block(self):
        where = [None]
        def f():
            for i in range(10):
                where[0] = i
                self.c.send(i)
        t = stackless.tasklet(f)()
        t.run()
        self.assertTrue(t.blocked)
        self.assertEqual(where[0], 3)
        r = []
        for i in range(3):
            r.append(self.c.receive())
        self.assertEqual(r, range(3))
        t.run()
        self.assertEqual(where[0], 6)

        for i in range(7):
            r.append(self.c.receive())
        self.assertEqual(r, range(10))
        t.run()
        self.assertEqual(where[0], 9)


class test_zero_bounded_QueueChannel(test_QueueChannel):
    def setUp(self):
        self.c = util.QueueChannel(0)

    def test_send(self):
        # sending on a a zero bounded channel is equivalent to a normal one.
        where = [None]
        def f():
            for i in range(10):
                where[0] = i
                self.c.send(i)
        t = stackless.tasklet(f)()
        t.run()
        self.assertTrue(t.blocked)
        self.assertEqual(where[0], 0)

        r = []
        for i in range(5):
            r.append(self.c.receive())
        t.run()
        self.assertEqual(r, range(5))
        self.assertEqual(where[0], 5)

        for i in range(5):
            r.append(self.c.receive())
        t.run()
        self.assertEqual(r, range(10))
        self.assertEqual(where[0], 9)

    def test_receive(self):
        #receiving on a QueueChannel blocks
        r = []
        def f():
            for i in range(10):
                r.append(self.c.receive())

        t = stackless.tasklet(f)()
        self.c.send(0)
        self.c.send(1)
        self.assertEqual(r, range(2))
        self.c.send(2)
        self.assertEqual(r, range(3))
        for i in range(3, 10):
            self.c.send(i)
        self.assertEqual(r, range(10))


from .support import load_tests

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    unittest.main()

