from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from app.models.db import get_session
from app.models.model_profile import Profile

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.get("")
def list_profiles(session=Depends(get_session)):
    return session.exec(select(Profile)).all()

@router.get("/current")
def get_current_profile(session=Depends(get_session)):
    prof = session.exec(select(Profile).where(Profile.is_current == True)).first()
    if not prof:
        raise HTTPException(status_code=404, detail="No current profile")
    return {"id": prof.id, "name": prof.name}

@router.post("")
def create_profile(name: str, session=Depends(get_session)):
    p = Profile(name=name, is_current=False)
    session.add(p); session.commit(); session.refresh(p)
    return p

@router.post("/switch/{profile_id}")
def switch_current_profile(profile_id: int, session=Depends(get_session)):
    # set all to false, then set chosen to true
    for p in session.exec(select(Profile)).all():
        p.is_current = (p.id == profile_id)
        session.add(p)
    session.commit()
    return {"ok": True, "current_profile_id": profile_id}
