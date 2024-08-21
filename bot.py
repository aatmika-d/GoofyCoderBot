import discord
import requests
import random

# Initialize the Discord client with intents
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Function to get a random problem from Codeforces or CodeChef
def get_random_problem(site, min_rating=None, max_rating=None):
    if site == "codeforces":
        url = f"https://codeforces.com/api/problemset.problems"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200:
            return f"Error: Unable to fetch problems from {site}."

        problems = data['result']['problems']
        if min_rating and max_rating:
            problems = [problem for problem in problems if 'rating' in problem and min_rating <= problem['rating'] <= max_rating]

        if not problems:
            return f"No problems found in the specified range."

        problem = random.choice(problems)
        return f"Problem: {problem['name']}\nLink: https://codeforces.com/problemset/problem/{problem['contestId']}/{problem['index']}"

    elif site == "codechef":
        # CodeChef API placeholder
        # Since CodeChef doesn't provide an open API like Codeforces,
        # you would need to either scrape the website or use a different approach.
        # Here's a placeholder response for now.
        return "CodeChef API is not available, but here's a random link: https://www.codechef.com/problems/school"

    else:
        return f"Site '{site}' is not supported."

# Event when the bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Event to handle messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # Command to get a random problem
    if message.content.startswith("!problem"):
        parts = message.content.split()
        site = parts[1] if len(parts) > 1 else None
        min_rating = int(parts[2]) if len(parts) > 2 else None
        max_rating = int(parts[3]) if len(parts) > 3 else None
        
        if not site:
            await message.channel.send("Please specify a site. Example: `!problem codeforces`")
            return

        problem = get_random_problem(site, min_rating, max_rating)
        await message.channel.send(problem)

    # Response when the user says "bye"
    if message.content.lower() == "bye":
        await message.channel.send("Goodbye! Have a great day coding!")

    # Add more commands or responses as needed

# Run the bot with your token
client.run('write token here')
