#testtimeout.py
"""Test various timeout aspects of stacklesslib"""
import unittest
import logging
import stackless
import time
import contextlib

from stacklesslib import main, app, util
from stacklesslib.errors import TimeoutError

#compute fluff
fluffs = []
for i in range(100):
    t0 = time.time()
    t1 = time.time()
    while(t1 == t0):
        t1 = time.time()
    fluffs.append(t1-t0)
fluff = max(fluffs) * 2
# print "fluff", fluff
# typcially 2ms

class TimeoutMixin(object):
    def _notimeout(self, call, timeout=0.01):
        with self.Timer(timeout):
            with util.timeout(timeout):
                return call()

    def _timeout(self, call, timeout=0.01):
        self.assertRaises(TimeoutError, self._notimeout, call, timeout)

    @contextlib.contextmanager
    def Timer(self, delay):
        t0 = time.time()
        try:
            yield
        except TimeoutError:
            dt = time.time() - t0
            self.assertLessEqual(delay - fluff, dt, "timedout %s early, fluff=%s"%(delay-dt, fluff))
            self.assertLessEqual(dt, delay + fluff, "timedout %s late, fluff=%s"%(dt-delay, fluff))
            raise


class TestTimeout(TimeoutMixin, unittest.TestCase):

    def test_send(self):
        c = stackless.channel()
        self._timeout(lambda:c.send(None))

    def test_receive(self):
        c = stackless.channel()
        self._timeout(c.receive)

    def test_success(self):
        def func():
            return "hullo"
        result = self._notimeout(func)
        self.assertEqual(result, "hullo")

    def test_long_success(self):
        import time
        sleep = getattr(time, "real_sleep", time.sleep)
        def func():
            sleep(0.01)
            return "hullo"
        # should not timeou because there is no point for the tasklet
        # to do so
        result = self._notimeout(func, 0.001)
        self.assertEqual(result, "hullo")

    def test_sleep(self):
        result = self._timeout(lambda:app.sleep(1.0))

    def test_event(self):
        e = app.Event()
        result = self._timeout(lambda:e.wait())

    def test_Lock(self):
        e = app.Lock()
        with e:
            result = self._timeout(lambda:e.acquire())


class TestTimeoutDeco(TestTimeout):
    """Using the function decorator"""
    def _notimeout(self, call, timeout=0.01):
        call2 = util.timeout_function(timeout)(call)
        with self.Timer(timeout):
            return call2()

class TestTimeoutFunc(TestTimeout):
    """Using the function call proxy"""
    def _notimeout(self, call, timeout=0.01):
        def call2():
            ok, val = util.timeout_call(call, timeout)
            if ok:
                return val
            else:
                raise TimeoutError("dude")
        with self.Timer(timeout):
            return call2()

class TestRecursion(TimeoutMixin, unittest.TestCase):
    def test_no_inner_catch(self):

        def inner():
            with util.timeout(1.0): #long timeout
                try:
                    app.sleep(2.0)
                except TimeoutError:
                    self.assertFalse("this should not have timed out")
        self._timeout(inner, 0.01)

    def test_inner_catch_reraise(self):
        def inner():
            with util.timeout(0.01): #long timeout
                app.sleep(2.0)
        # expect the inner timeout to percolate outwards
        def outer():
            with util.timeout(1.0):
                self.assertRaises(TimeoutError, inner)
                raise TimeoutError
        self.assertRaises(TimeoutError, outer)

    def test_inner_catch(self):
        def inner():
            with util.timeout(0.01): #long timeout
                app.sleep(2.0)

        # expect the inner timeout to percolate outwards
        def outer():
            with util.timeout(1.0):
                self.assertRaises(TimeoutError, inner)
                return "foo"
        self.assertEqual(outer(), "foo")

    def test_inner_same(self):
        def inner():
            with util.timeout(0.01): #long timeout
                app.sleep(2.0)

        def outer():
            with util.timeout(0.01):
                self.assertRaises(TimeoutError, inner)
                raise TimeoutError
                return "foo"
        self.assertRaises(TimeoutError, outer)
        #self.assertEqual(outer(), "foo")

    def test_three_timeouts(self):
        def one():
            with util.timeout(0.06):
                app.sleep(1.0)
        def two():
            with util.timeout(0.08):
                self.assertRaises(TimeoutError, one)
                app.sleep(1.0)

        def three():
            with util.timeout(0.01):
                self.assertRaises(TimeoutError, two)
                app.sleep(1.0)
        self.assertRaises(TimeoutError, three)

    def test_three_successes(self):
        def one():
            with util.timeout(0.06):
                return "foo"
        def two():
            with util.timeout(0.08):
                return one()
        def three():
            with util.timeout(0.01):
                return two()
        self.assertEqual("foo", three())

    def test_inst(self):
        def one():
            try:
                exc = TimeoutError()
                with util.timeout(0.01, exc=exc):
                    app.sleep(1.0)
            except Exception as e:
                self.assertTrue(e is exc)
                raise
        def two():
            try:
                exc = TimeoutError()
                with util.timeout(0.02, exc=exc):
                    one()
            except Exception as e:
                self.assertFalse(e is exc)
                raise
        self.assertRaises(TimeoutError, two)


    def test_exc_inst(self):
        def one():
            try:
                exc=ZeroDivisionError("hello")
                with util.timeout(0.01, exc=exc):
                    app.sleep(1.0)
            except Exception as e:
                self.assertTrue(e is exc)
                self.assertEqual(e.args[0], "hello")
                self.assertEqual(type(e), ZeroDivisionError)
                raise
        self.assertRaises(ZeroDivisionError, one)

    def test_exc_class(self):
        def one():
            try:
                exc=ZeroDivisionError
                with util.timeout(0.01, exc=exc):
                    app.sleep(1.0)
            except Exception as e:
                self.assertTrue(type(e) is exc)
                self.assertEqual(e.args, ())
                raise
        self.assertRaises(ZeroDivisionError, one)


class TestTimeouts(unittest.TestCase):
    def test_timeouts(self):
        t = util.Timeouts(0.01)
        def s():
            with t.timeout():
                app.sleep(0.005)

        s() #first one should be ok
        self.assertRaises(TimeoutError, s)
        self.assertRaises(TimeoutError, s)


from .support import load_tests

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    unittest.main()
