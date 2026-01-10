import psutil
import asyncio

def get_cpu_usage(interval=1):
    return psutil.cpu_percent(interval=interval)

def get_ram_usage():
    return psutil.virtual_memory().percent

def get_cpu_temp():
    return psutil.sensors_temperatures()['k10temp'][0].current

def get_stats(interval):
    cpu_usage = get_cpu_usage(interval)
    cpu_temp = get_cpu_temp()
    ram_usage = get_ram_usage()

    return {
        'cpu_usage': cpu_usage,
        'cpu_temp': cpu_temp,
        'ram_usage': ram_usage,
    }

async def get_stats_async(interval):
    return await asyncio.to_thread(get_stats, interval)