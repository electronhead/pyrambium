def test_during_period():
    """
    def during_period(self, callable, tag:str):
        if (self.start is not None) and (self.stop is not None):
            is_in_period_wrapper = lambda start, stop: (lambda now: start < now and now < stop if (start < stop) else start < now or now < stop)
            is_in_period = is_in_period_wrapper(self.start, self.stop)
            do_nothing = lambda tag, scheduler_info: None
            return lambda: (callable if is_in_period(Now.t()) else do_nothing)(tag=tag, scheduler_info=self.info())
        else:
            return lambda: callable(tag=tag, scheduler_info=self.info())
    """
    from mothership.base.service.scheduler import Scheduler
    from mothership.base.service.util import Now
    from datetime import time

    daytime = (time(6,0,0), time(18,0,0))
    nighttime = (time(18,0,0), time(6,0,0))

    s_daytime = Scheduler(start = daytime[0], stop = daytime[1])
    s_nighttime = Scheduler(start = nighttime[0], stop = nighttime[1])

    callable = lambda tag, scheduler_info: True
    daytime_callable = s_daytime.during_period(callable, tag='abc')
    nighttime_callable = s_nighttime.during_period(callable, tag='abc')

    now = Now.t()

    is_daytime = daytime[0] < now and now < daytime[1]
    if is_daytime:
        assert daytime_callable() and not nighttime_callable()
    else:
        assert not daytime_callable() and nighttime_callable()
