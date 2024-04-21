import platform

import aiohttp
import asyncio
from datetime import datetime, timedelta
import sys


async def main():
    arg = sys.argv[1]

    try:
        days = int(arg)
    except ValueError:
        print("Argument must be an integer")
        return

    formatted_result = []
    if days <= 10:
        for i in range(days):
            datetime_today = datetime.now()-timedelta(days=i)
            today = datetime_today.strftime("%d.%m.%Y")
            params = {
                "date": today
            }
            async with aiohttp.ClientSession() as session:
                async with aiohttp.ClientSession(
                        connector=aiohttp.TCPConnector(ssl=False)) as session:
                    async with session.get(
                         'https://api.privatbank.ua/p24api/exchange_rates',
                         params=params) as response:

                        result = await response.json()

                        date = result['date']
                        date_exchange_rates = {}
                        currencies = ["USD", "EUR"]

                        for data in result['exchangeRate']:

                            currency = data['currency']
                            if currency in currencies:
                                sale_rate = data.get(
                                    'saleRate', data['saleRateNB']
                                    )
                                purchase_rate = data.get(
                                    'purchaseRate', data['purchaseRateNB']
                                )

                                date_exchange_rates[currency] = {
                                    'sale': sale_rate,
                                    'purchase': purchase_rate
                                    }

                        formatted_result.append({
                                date: date_exchange_rates
                                })

        return formatted_result
    else:
        return "Date range should be no more than 10 days"


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)
