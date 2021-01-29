from pyrambium.app.shared import return_success, raised_exception, get_mothership
from fastapi import APIRouter, status

router = APIRouter(
    prefix="/mothership",
    tags = ['Mothership']
)

@router.get('/', status_code=status.HTTP_200_OK)
def get_mothership_dict():
    try:
        return return_success(get_mothership().dict())
    except Exception as e:
        raise raised_exception("failed to retrieve the Mothership", e)

@router.get('/clear', status_code=status.HTTP_200_OK)
def clear_mothership():
    try:
        get_mothership().clear_all()
        return return_success("cleared")
    except Exception as e:
        raise raised_exception("failed to clear the Mothership", e)

@router.get('/save/{file}', status_code=status.HTTP_200_OK)
def save_mothership(file:str):
    try:
        get_mothership().save(file)
        return return_success("saved")
    except Exception as e:
        raise raised_exception("failed to save the Mothership", e)

@router.get('/retrieve/{file}', status_code=status.HTTP_200_OK)
def retrieve_mothership(file:str):
    try:
        return return_success(get_mothership().load(file))
    except Exception as e:
        raise raised_exception("failed to retrieve the Mothership", e)