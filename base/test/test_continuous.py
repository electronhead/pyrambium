from mothership.base.service.continuous import Continuous
from mothership.base.service.util import TimeUnit
import time

def test_timely_callable(tmp_path):
    """
    This test exercises the schedule_timely_callable method.
    """
    class Suite:
        def __init__(self):
            self.content = 'foobarbaz'
            self.file = 'text.txt'
            self.path = tmp_path / self.file
        def callable(self):
            with self.path.open(mode='a') as fid:
                fid.write(self.content)
                fid.write('\n')
        def gather(self):
            result = []
            with self.path.open(mode='r') as fid:
                result.append(fid.readlines())
            return result
        def run(self):
            continuous = Continuous()
            continuous.schedule_timely_callable('tag', self.callable)
            continuous.run_continuously()
            time.sleep(4)
            continuous.stop_running_continuously()
            continuous.clear()
    suite = Suite()
    suite.run()
    accumulated_content = suite.gather()
    assert accumulated_content and len(accumulated_content) > 0

def test_random_callable(tmp_path):
    """
    This test exercises the schedule_timely_callable method.
    """
    class Suite:
        def __init__(self):
            self.content = 'foobarbaz'
            self.file = 'text.txt'
            self.path = tmp_path / self.file
        def callable(self):
            with self.path.open(mode='a') as fid:
                fid.write(self.content)
                fid.write('\n')
        def gather(self):
            result = []
            with self.path.open(mode='r') as fid:
                result.append(fid.readlines())
            return result
        def run(self):
            continuous = Continuous()
            continuous.schedule_random_callable('tag', self.callable, time_unit=TimeUnit.second, low=1, high=3)
            continuous.run_continuously()
            time.sleep(4)
            continuous.stop_running_continuously()
            continuous.clear()
    suite = Suite()
    suite.run()
    accumulated_content = suite.gather()
    assert accumulated_content and len(accumulated_content) > 0
    

    
