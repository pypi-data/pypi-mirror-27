import aiohttp

from .base import BASE_URL


URL = 'iss/history/engines/stock/markets/shares/boards/'


class HistoryShares:
    
    def __init__(self, ticker=None, board='tqbr'):
        self.ticker = ticker
        self.url = '{}{}{}{}/securities'.format(BASE_URL, 
            URL, board, ticker)

    async def call_chunks(self):
        pass

    async def call(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                print(resp.status())
                print(resp.text())
