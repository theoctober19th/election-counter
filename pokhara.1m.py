#!/opt/homebrew/bin/python3

from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup


ELECTION_URL = f"https://election.ekantipur.com/"
KATHMANDU_URL = urljoin(ELECTION_URL, "pradesh-4/district-kaski/pokhara-lekhnath")

response = requests.get(KATHMANDU_URL, params={"lng": "eng"})
soup = BeautifulSoup(response.content, "lxml")

cards = soup.select("div.col-xl-6")
mayor_card = cards[0]
deputy_mayor_card = cards[1]

mayor_candidate_wrapper = mayor_card.select("div.candidate-meta-wrapper")
deputy_mayor_candidate_wrapper = deputy_mayor_card.select("div.candidate-meta-wrapper")
mayor_vote_counts = {}
deputy_mayor_vote_counts = {}

for wrapper in mayor_candidate_wrapper:
    candidate_name = wrapper.select_one("div.candidate-name").text.strip()
    candidate_name = candidate_name.split()[-1]
    votes = wrapper.select_one("div.vote-numbers").text
    try:
        votes = votes.strip()
        votes = int(votes)
    except:
        votes = 0
    if votes:
        mayor_vote_counts[candidate_name] = votes

mayor_vote_counts = sorted(mayor_vote_counts.items(), key=lambda item: item[1], reverse=True)

for wrapper in deputy_mayor_candidate_wrapper:
    candidate_name = wrapper.select_one("div.candidate-name").text.strip()
    candidate_name = candidate_name.split()[-1]
    votes = wrapper.select_one("div.vote-numbers").text
    try:
        votes = votes.strip()
        votes = int(votes)
    except:
        votes = 0
    if votes > 0:
        deputy_mayor_vote_counts[candidate_name] = votes

deputy_mayor_vote_counts = sorted(deputy_mayor_vote_counts.items(), key=lambda item: item[1], reverse=True)

can1, vote1 = mayor_vote_counts.pop(0)
can2, vote2 = mayor_vote_counts.pop(0)

difference = vote1 - vote2
print(f"{can1} {vote1} / {vote2} {can2} ({difference:+g})")
