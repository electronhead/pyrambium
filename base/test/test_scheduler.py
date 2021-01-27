def test_during_period():
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

def test_file_action(tmp_path):
    """
    This test exercises the schedule_timely_callable method.
    """
    from pydantic import BaseModel
    from mothership.base.service.action import Action, ActionPayload
    from mothership.base.service.continuous import Continuous
    from mothership.base.service.util import PP
    import time

    class FileAction:
        def execute(self, tag=None, scheduler_info:dict=None):
            path = tmp_path / 'test.txt'
            with path.open(mode='a') as fid:
                fid.write('blee\n')
            return {'outcome':'file appended'}

    class Suite():
        def __init__(self, action):
            self.action = action
        def gather(self):
            path = tmp_path / 'test.txt'
            with path.open(mode='r') as fid:
                return sum(1 for line in fid)
        def run(self):
            continuous = Continuous()
            continuous.schedule_timely_callable('tag', self.action.execute)
            continuous.run_continuously()
            time.sleep(4)
            continuous.stop_running_continuously()
            continuous.clear()
    suite = Suite(FileAction())
    suite.run()
    line_count = suite.gather()
    assert line_count and line_count >= 1, "no lines written to file"