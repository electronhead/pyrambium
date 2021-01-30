import pytest

@pytest.fixture
def friends(tmp_path):
    def stuff():
        # want a fresh tuple from the fixture
        from pyrambium.base.service.mothership import Mothership
        from pyrambium.base.service.action import FileHeartbeat
        from pyrambium.base.service.scheduler import TimelyScheduler
        from pyrambium.base.service.continuous import Continuous

        saved_dir = str(tmp_path)
        output_file = str(tmp_path / 'output.txt')
        mothership = Mothership(saved_dir=saved_dir)
        mothership.set_continuous(Continuous())
        action = FileHeartbeat(file=output_file)
        scheduler = TimelyScheduler(interval=1)

        return mothership, scheduler, action
    return stuff