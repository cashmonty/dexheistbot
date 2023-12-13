
import discord
from apirequest import get_ohlc_data
from utils import process_ohlc_data_and_generate_chart
from discord.ext import commands

@commands.command(name='chart', help='Generate a chart for given token and interval')
async def chart(ctx, token_address: str, interval: str = '1h'):
    ohlc_data = await get_ohlc_data(token_address, interval)
    if ohlc_data is not None:
        chart_file = await process_ohlc_data_and_generate_chart(ohlc_data)
        await ctx.send(file=discord.File(chart_file))
    else:
        await ctx.send("Failed to fetch OHLC data.")
