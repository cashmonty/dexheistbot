import aiohttp
import datetime
import asyncio

async def get_ohlc_data(token_address, interval='1h'):
    url = 'https://api.syve.ai/v1/price/historical/ohlc'

    # Setting default values for other parameters
    pool_address = 'all'  # default to consider all pools
    price_type = 'price_token_usd_robust_tick_1'  # default price type
    from_timestamp = 0  # default
    until_timestamp = int(datetime.datetime.now().timestamp())  # current timestamp
    max_size = 500  # default
    fill = 'true'
    order = 'desc'
    volume = 'true'


    params = {
        'token_address': token_address,
        'pool_address': pool_address,
        'price_type': price_type,
        'interval': interval,
        'from_timestamp': from_timestamp,
        'until_timestamp': until_timestamp,
        'max_size': max_size,
        'order': order,
        'fill': fill,
        'with_volume': volume
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    print(f"Error fetching data with status code: {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"HTTP request error: {e}")
        return None
    except asyncio.TimeoutError as e:
        print(f"Request timed out: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None