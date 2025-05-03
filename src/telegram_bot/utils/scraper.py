import logging
from playwright.async_api import async_playwright
from typing import List, Dict, Optional, Union

logger = logging.getLogger(__name__)

DRAFT5_URL = "https://draft5.gg/equipe/330-FURIA/campeonatos"

def class_contains(substrings: Union[str, List[str]]):
    if isinstance(substrings, str):
        substrings = [substrings]
    return lambda classes: classes and any(sub in cls for sub in substrings for cls in classes)

async def fetch_draft5() -> List[Dict[str, str]]:
    """
    Busca próximos campeonatos da FURIA no draft5.gg usando Playwright.
    Retorna uma lista de dicionários com informações dos campeonatos.
    """
    tournaments = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(DRAFT5_URL)
        await page.wait_for_selector("a.TournamentCard__TournamentCardContainer-sc-1vb6wff-0")

        # Campeonatos
        cards = await page.query_selector_all("a.TournamentCard__TournamentCardContainer-sc-1vb6wff-0")
        for card in cards:
            nome = await card.query_selector("h4")
            data = await card.query_selector("small")
            link = await card.get_attribute("href")
            tournament = {
                "name": await nome.inner_text() if nome else "Nome não disponível",
                "dates": await data.inner_text() if data else "Datas não disponíveis",
                "url": f"https://draft5.gg{link}" if link else "",
            }
            tournaments.append(tournament)

        await browser.close()
    return tournaments

