from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
import httpx

fast = FastAPI()
fast.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@fast.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Pokemon search route garxa 
@fast.post("/search", response_class=HTMLResponse)
async def search_pokemon(request: Request, pokemon_name: str = Form(...)):
    pokemon_name = pokemon_name.lower().replace(" ", "-")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}")
            response.raise_for_status()
            pokemon_data = response.json()
            return templates.TemplateResponse("result.html", {"request": request, "pokemon": pokemon_data})
    except httpx.HTTPStatusError as exc:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(exc)})