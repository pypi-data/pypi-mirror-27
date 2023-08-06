import cProfile
import contextlib
import functools
import io
import logging
import pstats
import time


__all__ = ['timing', 'profile', 'profiler']


def timing(f):
    log = logging.getLogger('instrument.%s' % f.__qualname__)
    count = 0
    t = 0.0
    s = 0.0
    guard = False
    @functools.wraps(f)
    def wrapper(*args, **kw):
        nonlocal t, s, count, guard
        t0, s0 = time.perf_counter(), time.process_time()
        recurring = guard
        guard = True
        try:
            return f(*args, **kw)
        finally:
            guard = False
            if not recurring:
                t_, s_, = time.perf_counter() - t0, time.process_time() - s0
                t += t_
                s += s_
                count += 1
                log.error(
                    '%f wall %f %2.2f%% cpu count=%d (tot %f wall %f %2.2f%% cpu avg %f wall %f cpu)',
                    t_, s_, 100.0 * s_ / t_, count,
                    t, s, 100.0 * s / t,
                t / count, s / count)
    return wrapper

def profile(f):
    log = logging.getLogger('profile.%s' % f.__qualname__)
    count = 0
    t = 0.0
    s = 0.0
    guard = False
    pr = cProfile.Profile()
    @functools.wraps(f)
    def wrapper(*args, **kw):
        nonlocal t, s, count, guard, pr
        t0, s0 = time.perf_counter(), time.process_time()
        recurring = guard
        guard = True
        pr.enable()
        try:
            return f(*args, **kw)
        finally:
            guard = False
            if not recurring:
                pr.disable()
                t_, s_, = time.perf_counter() - t0, time.process_time() - s0
                t += t_
                s += s_
                count += 1
                log.error(
                    '%f wall %f %2.2f%% cpu count=%d (tot %f wall %f %2.2f%% cpu avg %f wall %f cpu)',
                    t_, s_, 100.0 * s_ / t_, count,
                    t, s, 100.0 * s / t,
                t / count, s / count)
                out = io.StringIO()
                ps = pstats.Stats(pr, stream=out).sort_stats('cumulative')
                ps.print_stats(20)
                ps.print_callers(20)
                log.error('profiler:\n' + out.getvalue())
    return wrapper


_profilers = {}

@contextlib.contextmanager
def profiler(name=None):
    if name not in _profilers:
        _profilers[name] = [cProfile.Profile()]
    log = logging.getLogger(
        'profile' + ('.' + name if name is not None else ''))
    (pr,) = _profilers[name]
    pr.enable()
    try:
        yield
    finally:
        out = io.StringIO()
        ps = pstats.Stats(pr, stream=out).sort_stats('cumulative')
        ps.print_stats(20)
        ps.print_callers(20)
        log.error('profiler:\n' + out.getvalue())


