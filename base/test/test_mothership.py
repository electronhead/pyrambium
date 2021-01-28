def test_schedule_action(tmp_path):
    """
    Tests Mothership and Continuous objects running a scheduled action.
    """
    from mothership.base.service.mothership import Mothership
    from mothership.base.service.action import FileHeartbeat
    from mothership.base.service.scheduler import TimelyScheduler
    from mothership.base.service.continuous import Continuous
    import time
    import json

    saved_dir = str(tmp_path)
    output_file = str(tmp_path / 'output.txt')

    continuous = Continuous()

    mothership = Mothership(saved_dir=saved_dir)
    action = FileHeartbeat(file=output_file)
    scheduler = TimelyScheduler(interval=1)

    mothership.add_action('foo', action)
    mothership.add_scheduler('bar', scheduler)
    mothership.schedule_action('bar', 'foo', continuous)

    continuous.run_continuously()
    time.sleep(4)
    continuous.stop_running_continuously()
    continuous.clear()

    line = None
    with open(output_file, 'r') as fid:
        line = fid.readline()

    assert line is not None and type(line) is str and len(line) > 0

def test_unschedule_action(tmp_path):
    """
    Tests unscheduling an action.
    """
    from mothership.base.service.mothership import Mothership
    from mothership.base.service.action import FileHeartbeat
    from mothership.base.service.scheduler import TimelyScheduler
    from mothership.base.service.continuous import Continuous
    import time

    saved_dir = str(tmp_path)
    output_file = str(tmp_path / 'output.txt')

    continuous = Continuous()

    mothership = Mothership(saved_dir=saved_dir)
    action = FileHeartbeat(file=output_file)
    scheduler = TimelyScheduler(interval=1)

    mothership.add_action('foo', action)
    mothership.add_scheduler('bar', scheduler)
    mothership.schedule_action('bar', 'foo', continuous)
    mothership.unschedule_action('foo', continuous)

    assert continuous.job_count() == 0
    assert mothership.get_scheduled_action_count() == continuous.job_count()

def test_reschedule_action(tmp_path):
    """
    Tests unscheduling and then rescheduling an action.
    """
    from mothership.base.service.mothership import Mothership
    from mothership.base.service.action import FileHeartbeat
    from mothership.base.service.scheduler import TimelyScheduler
    from mothership.base.service.continuous import Continuous
    import time

    saved_dir = str(tmp_path)
    output_file = str(tmp_path / 'output.txt')

    continuous = Continuous()

    mothership = Mothership(saved_dir=saved_dir)
    action = FileHeartbeat(file=output_file)
    scheduler = TimelyScheduler(interval=1)

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
    with open(output_file, 'r') as fid:
        line = fid.readline()

    assert line is not None and type(line) is str and len(line) > 0