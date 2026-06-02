'''from fastapi import FastAPI, HTTPException
from urllib.parse import quote_plus
import httpx
from bs4 import BeautifulSoup

app = FastAPI()


@app.get("/character/{name}")
async def get_character(name: str):
    url = f"https://www.tibia.com/community/?subtopic=characters&name={quote_plus(name)}"

    async with httpx.AsyncClient(
        headers={"User-Agent": "Mozilla/5.0"}
    ) as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Erro ao acessar tibia.com")

    soup = BeautifulSoup(response.text, "lxml")

    character = {}

    rows = soup.select("table.TableContent tr")

    for row in rows:
        cols = row.find_all("td")

        if len(cols) == 2:
            key = cols[0].get_text(strip=True).replace(":", "")
            value = cols[1].get_text(" ", strip=True)

            character[key] = value

    if not character:
        raise HTTPException(status_code=404, detail="Personagem não encontrado")

    return {
        "source": "tibia.com",
        "url": url,
        "character": character
    }'''