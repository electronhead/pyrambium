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

    (tmp_path / 'saved').mkdir(parents=True, exist_ok=True)
    (tmp_path / 'output').mkdir(parents=True, exist_ok=True)

    saved_dir = str(tmp_path / 'saved') + '/'

    output_file_path = tmp_path / 'output' / 'heartbeat.txt'
    output_file = str(output_file_path)

    continuous = Continuous()

    mothership = Mothership(saved_dir=saved_dir)
    action = FileHeartbeat(file=output_file)
    scheduler = TimelyScheduler(interval=1)

    mothership.add_action('foo', action)
    mothership.add_scheduler('bar', scheduler)
    mothership.schedule_action('bar', 'foo', continuous)

    assert continuous.job_count() == 1
    assert mothership.get_scheduled_action_count() == continuous.job_count()

    continuous.run_continuously()
    time.sleep(4)
    continuous.stop_running_continuously()

    line = None
    with output_file_path.open(mode='r') as fid:
        line = fid.readline()

    assert line is not None