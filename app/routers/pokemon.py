from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..database import get_db
from ..models import Pokemon

router = APIRouter()

@router.get("/pokemons")
async def get_pokemons(name: str = None, type: str = None, db: AsyncSession = Depends(get_db)):
    query = select(Pokemon)
    
    if name:
        query = query.where(Pokemon.name.ilike(f"%{name}%"))
    if type:
        query = query.where(Pokemon.type.ilike(f"%{type}%"))
    
    result = await db.execute(query)
    pokemons = result.scalars().all()
    
    return pokemons
