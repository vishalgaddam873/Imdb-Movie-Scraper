from scraper import scrape_top_list
import requests
from bs4 import BeautifulSoup

def get_rating_url(movies_list):
    url_list = []
    for i in movies_list:
        url = i['url']
        rating_url = url[:37] + "ratings?ref_=tt_ov_rt"
        url_list.append(rating_url)

    return url_list

top_movies = scrape_top_list()
rating_url_list = get_rating_url(top_movies)
# print(rating_url_list)

def scrape_rating_page(url_list):
    ratings_list = []
    for url in url_list:

        imdb_id = url[27:36]
        page = requests.get(url)
        soup = BeautifulSoup(page.text,'html.parser')
        name = soup.title.get_text().split()
        ratings_by_demographic = soup.find('div',class_="title-ratings-sub-page")
        rating_tables = ratings_by_demographic.find_all('table')
        trs = rating_tables[1].find_all('tr')


        ratings_by_gender = {'movie_name':name[0],'imdb_id': imdb_id,'gender':{'male':{'count':'','rating':''},'female':{'count':'','rating':''}}}

        for i in range(len(trs)):
            count = ''
            if i == 2:
                males_ratings = trs[i].find('td',class_='ratingTable').get_text().split()
                for i in males_ratings[1]:
                    for j in i:
                        if ',' in j:
                            pass
                        else:
                            count += j

                ratings_by_gender['gender']['male']['count'] = int(count)
                ratings_by_gender['gender']['male']['rating'] = float(males_ratings[0])

            elif i == 3:
                females_ratings = trs[i].find('td',class_='ratingTable').get_text().split()
                for i in females_ratings[1]:
                    for j in i:
                        if ',' in j:
                            pass
                        else:
                            count += j

                ratings_by_gender['gender']['female']['count'] = int(count)
                ratings_by_gender['gender']['female']['rating'] = float(females_ratings[0])

        ratings_list.append(ratings_by_gender)


    print(ratings_list)

rating_page = scrape_rating_page(rating_url_list)
print(rating_page)
