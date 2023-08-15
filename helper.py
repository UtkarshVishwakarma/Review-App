import requests
from bs4 import BeautifulSoup

def fetch_reviews(movie):
    url = f"https://www.omdbapi.com/?apikey=f4e281ed&t&t={movie}"
    response = requests.get(url)
    data = response.json()
    if data.get("Response") == "True":
        id = data.get("imdbID")
    else:
        raise Exception("Not Found")

    url = f'https://www.imdb.com/title/{id}/reviews/?ref_=tt_ql_2'
    r= requests.get(url)   
    soup = BeautifulSoup(r.content, 'html.parser')

    reviews = []
    titles = []
    for i in soup.find_all('div', class_='text'):
      reviews.append(i.get_text())

    for i in soup.find_all('a', class_='title'):
      titles.append(i.get_text())

    return titles, reviews