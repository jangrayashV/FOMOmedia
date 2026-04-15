from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from db import get_db
from schemas import POVCreate, POVRead, POVUpdate
from models import POV, User
from dependencies import get_current_user

router = APIRouter(prefix="/v1/pov", tags=["pov"])

@router.post("/new", response_model=POVRead)
async def create_pov(cred: POVCreate, db: AsyncSession = Depends(get_db), current_user:User = Depends(get_current_user)):
    new_pov = POV(
        user_id = current_user.user_id,
        parent_pov_id = cred.parent_pov_id,
        content = cred.content
    )
    db.add(new_pov)
    await db.commit()
    await db.refresh(new_pov)
    return new_pov


#to do later: add authentication to this endpoint, so that no one can see povs without ever logging in. For now, this is just for testing purposes.
@router.get("/all", response_model=list[POVRead])
async def get_all_povs(db: AsyncSession = Depends(get_db)):
    response = await db.execute(select(POV))
    all_povs = response.scalars().all()
    return all_povs

@router.get("/my", response_model=list[POVRead])
async def get_my_povs(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = await db.execute(select(POV).where(current_user.user_id == POV.user_id))
    my_povs = response.scalars().all()
    return my_povs

@router.get("/{pov_id}", response_model=POVRead)
async def get_my_pov(pov_id: int, db:AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = await db.execute(select(POV).where(POV.pov_id == pov_id, current_user.user_id == POV.user_id))
    my_pov = response.scalar_one_or_none()

    if not my_pov:
        raise HTTPException(status_code=404, detail="POV not found")

    return my_pov

@router.patch("/{pov_id}", response_model=POVRead)
async def update_pov(pov_id: int, pov_update: POVUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = await db.execute(select(POV).where(POV.pov_id == pov_id, current_user.user_id == POV.user_id))
    my_pov = response.scalar_one_or_none()

    if not my_pov:
        raise HTTPException(status_code=404, detail="POV not found")

    my_pov.content = pov_update.content
    await db.commit()
    await db.refresh(my_pov)
    return my_pov

@router.delete("/{pov_id}")
async def delete_pov(pov_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    response = await db.execute(select(POV).where(POV.pov_id == pov_id, POV.user_id == current_user.user_id))
    my_pov = response.scalar_one_or_none()

    if not my_pov:
        raise HTTPException(status_code=404, detail="POV not found")
    
    await db.delete(my_pov)
    await db.commit()
    return {"detail": "POV deleted successfully"}