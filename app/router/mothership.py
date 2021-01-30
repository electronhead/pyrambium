from pyrambium.app.shared import return_success, raised_exception, get_mothership
from fastapi import APIRouter, status

router = APIRouter(
    prefix="/mothership",
    tags = ['Mothership']
)

@router.get('/clear', status_code=status.HTTP_200_OK)
def clear_mothership():
    try:
        get_mothership(router).clear_all()
        return return_success("mothership cleared")
    except Exception as e:
        raise raised_exception("failed to clear the Mothership", e)

@router.get('/load', status_code=status.HTTP_200_OK)
def load():
    try:
        return return_success(get_mothership(router).load_current())
    except Exception as e:
        raise raised_exception("failed to retrieve the Mothership", e)

@router.get('/save', status_code=status.HTTP_200_OK)
def save():
    try:
        get_mothership(router).save_current()
        return return_success(f"mothership saved to current")
    except Exception as e:
        raise raised_exception("failed to save the Mothership", e)

@router.get('/load_from_name/{name}', status_code=status.HTTP_200_OK)
def load_from_name(name:str):
    try:
        return return_success(get_mothership(router).load_from_name(name))
    except Exception as e:
        raise raised_exception("failed to retrieve the Mothership", e)

@router.get('/save_to_name/{name}', status_code=status.HTTP_200_OK)
def save_to_name(name:str):
    try:
        get_mothership(router).save_to_name(name)
        return return_success(f"mothership saved to ({name})")
    except Exception as e:
        raise raised_exception("failed to save the Mothership", e)

@router.get('/saved_dir', status_code=status.HTTP_200_OK)
def retrieve_mothership(saved_dir:str):
    try:
        return return_success(get_mothership(router).get_saved_dir())
    except Exception as e:
        raise raised_exception("failed to retrieve the Mothership", e)

@router.put('/saved_dir/{saved_dir}', status_code=status.HTTP_200_OK)
def retrieve_mothership(saved_dir:str):
    try:
        return return_success(f"saved_dir set to ({saved_dir})")
    except Exception as e:
        raise raised_exception("failed to retrieve the Mothership", e)