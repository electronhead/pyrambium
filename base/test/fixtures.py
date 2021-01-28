import pytest

@pytest.fixture
def friends(tmp_path):
    def stuff():
        # want a fresh tuple from the fixture
        from mothership.base.service.mothership import Mothership
        from mothership.base.service.action import FileHeartbeat
        from mothership.base.service.scheduler import TimelyScheduler
        from mothership.base.service.continuous import Continuous

        saved_dir = str(tmp_path)
        output_file = str(tmp_path / 'output.txt')
        continuous = Continuous()
        mothership = Mothership(saved_dir=saved_dir)
        action = FileHeartbeat(file=output_file)
        scheduler = TimelyScheduler(interval=1)

        return mothership, scheduler, action, continuous
    return stuff