import pytest
from mothership.base.test.fixtures import friends

def test_schedule_action(friends):
    """
    Tests Mothership and Continuous objects running a scheduled action.
    """
    import time

    mothership, scheduler, action, continuous = friends()

    mothership.add_action('foo', action)
    mothership.add_scheduler('bar', scheduler)
    mothership.schedule_action('bar', 'foo', continuous)

    continuous.run_continuously()
    time.sleep(4)
    continuous.stop_running_continuously()
    continuous.clear()

    line = None
    with open(action.file, 'r') as fid:
        line = fid.readline()

    assert line is not None and type(line) is str and len(line) > 0

def test_unschedule_action(friends):
    """
    Tests unscheduling an action.
    """
    mothership, scheduler, action, continuous = friends()

    mothership.add_action('foo', action)
    mothership.add_scheduler('bar', scheduler)
    mothership.schedule_action('bar', 'foo', continuous)
    mothership.unschedule_action('foo', continuous)

    assert continuous.job_count() == 0
    assert mothership.get_scheduled_action_count() == continuous.job_count()

def test_reschedule_action(friends):
    """
    Tests unscheduling and then rescheduling an action.
    """
    import time

    mothership, scheduler, action, continuous = friends()

    mothership.add_action('foo', action)
    mothership.add_scheduler('bar', scheduler)
    mothership.schedule_action('bar', 'foo', continuous)
    mothership.unschedule_action('foo', continuous)
    mothership.schedule_action('bar', 'foo', continuous)

    continuous.run_continuously()
    time.sleep(4)
    continuous.stop_running_continuously()
    continuous.clear()

    line = None
    with open(action.file, 'r') as fid:
        line = fid.readline()

    assert line is not None and type(line) is str and len(line) > 0
