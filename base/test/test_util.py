def test_now_1():
    from datetime import datetime, timedelta
    from pyrambium.base.service.util import Now
    now1 = datetime.now()
    now2 = Now.dt()
    elapsed = now2 - now1
    assert elapsed < timedelta(microseconds=100.0)

def test_now_2():
    from datetime import datetime, timedelta
    from pyrambium.base.service.util import Now
    now = datetime.now()
    now2 = Now.t()
    date2 = datetime(year=now.year, month=now.month, day=now.day, hour=now2.hour, minute=now2.minute, second=now2.second, microsecond=now2.microsecond)
    elapsed = date2 - now
    assert elapsed < timedelta(microseconds=100.0)

def test_now_3():
    from datetime import datetime, timedelta
    from pyrambium.base.service.util import Now
    now1 = datetime.now().time()
    now1_str = now1.strftime('%H:%M:%S')
    now2 = Now.s()
    assert now1_str in now2

def test_all_visible_subclasses():
    from pyrambium.base.service.util import all_visible_subclasses
    class A:
        pass
    class B(A):
        pass
    class C(A):
        pass
    class D(B):
        pass
    x = all_visible_subclasses(A)
    y = {B,C,D}
    assert x == y

def test_key_strings_from_class():
    from pyrambium.base.service.util import key_strings_from_class
    from pydantic import BaseModel
    class A(BaseModel):
        a:str
        b:str
    x = {'a', 'b'}
    y = key_strings_from_class(A)
    assert x == y

def test_key_strings_from_dict():
    from pyrambium.base.service.util import key_strings_from_dict
    x = {'a', 'b'}
    y = key_strings_from_dict({'a':1, 'b':2})
    assert x == y

def test_filepathe():
    from pyrambium.base.service.util import FilePathe
    path = FilePathe(path = 'a/b/c')
    new_path = FilePathe(**(path.dict()))
    assert path.path == new_path.path, 'path reconstruction failed'