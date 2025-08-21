from fastapi import APIRouter
router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.get("/current")
def get_current_profile():
    return {"name": "Azim"}
