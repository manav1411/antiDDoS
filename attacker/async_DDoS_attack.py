import asyncio
import aiohttp

async def make_request(session, url):
    try:
        async with session.get(url) as response:
            # You could process the response here
            await response.text()
    except Exception as e:
        print(f"An error occurred: {e}")

async def simulate_ddos(target_url, number_of_requests):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(number_of_requests):
            task = asyncio.ensure_future(make_request(session, target_url))
            tasks.append(task)
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Replace with your web server's URL
    url = 'http://localhost:8080'
    # Number of requests you want to simulate
    number_of_requests = 1000

    asyncio.run(simulate_ddos(url, number_of_requests))
