from bs4 import BeautifulSoup
from cast_scraper import scrape_movie_cast
import requests
import pprint
import json
import os
import random
import time

url = "https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in"
page = requests.get(url)
soup = BeautifulSoup(page.text,'html.parser')

#Task1
# Here we scrape the list of 250 movies data.
def scrape_top_list():
	main_div = soup.find('div', class_='lister')
	tbody = main_div.find('tbody', class_='lister-list')
	trs = tbody.find_all('tr')

	movie_ranks =[]
	movie_name = []
	year_of_realease = []
	movie_urls = []
	movie_ratings = []

	for tr in trs:
		# Here we scrape ranks of movies. 
		position = tr.find('td', class_ ="titleColumn").get_text().strip()
		rank = ''
		for i in position:
			if '.' not in i:
				rank = rank + i	
			else:
				break
		movie_ranks.append(rank)
		
		# Here we scrape movie name or movie title	
		title = tr.find('td', class_ ="titleColumn").a.get_text()
		movie_name.append(title)

		# Here we scrape year of movie released.
		year = tr.find('td',class_ = "titleColumn").span.get_text()
		year_of_realease.append(year)

		# Here we scrape imdb ratings of movies.
		imdb_rating = tr.find('td',class_="ratingColumn imdbRating").strong.get_text()
		movie_ratings.append(imdb_rating)

		# Here we scrape movies urls or links.
		link = tr.find('td', class_="titleColumn").a['href']
		movie_link = "https://www.imdb.com" + link
		movie_urls.append(movie_link)

	Top_Movies = []
	movie_details ={'position':'','name':'','year':'','rating':'','url':''}
	for i in range(0,len(movie_ranks)):
		movie_details['position'] = int(movie_ranks[i])
		movie_details['name'] = str(movie_name[i])
		year_of_realease[i] = year_of_realease[i][1:5]
		movie_details['year'] = int(year_of_realease[i])
		movie_details['rating'] = float(movie_ratings[i])
		movie_details['url'] = movie_urls[i]
		Top_Movies.append(movie_details)
		movie_details ={'position':'','name':'','year':'','rating':'','url':''}
	return (Top_Movies)
top_movies = scrape_top_list()
#pprint.pprint(top_movies)
#print(top_movies)

#Task2
# Here the parameter movies is the dic type which is output of scrapee_top_list() function 
# Here we passed the scrape as argument in this function.
def group_by_year(movies):
	years = []
	movie_dict = {}
	for i in movies:
		year = i['year']
		if year not in years:
			years.append(year)
	for i in years:
		movie_dict[i] = []
	return movie_dict
# pprint.pprint(group_by_year(top_movies))
# print(group_by_year(top_movies))

#Task3
# Here the parameter movies is the dic type which is output of scrapee_top_list() function 
# Here we passed the scrape as argument in this function.
def group_by_decade(movies):
	movies_by_year = group_by_year(movies)
	movie_decade = {}
	decade_list = []

	# Here we get the keys of group_by_year() function which is years of movies
	for keys in movies_by_year:
		reminder = keys % 10
		subtract = keys - reminder
		if subtract not in decade_list:
			decade_list.append((subtract))
	decade_list.sort()

	# Here we created movie_decade dic and assigning the empty list to it.
	for decades in decade_list:
		movie_decade[decades] = []

	# Here we assiging the value to movie_decade dic
	for i in movie_decade:
		for j in movies_by_year:
			if j in range(i,i+10):
				movie_decade[i] += movies_by_year[j]
	return movie_decade
	#pprint.pprint(movie_decade)
# print(group_by_decade(top_movies))

# Task 4 and 8,9,13
def scrape_movie_details(movie_url):

	# Task 9
	sleep_time = random.randint(1,3)
	
	# task 8
	movie_id = ''
	for _id in movie_url[27:]:
		if '/' not in _id:
			movie_id += _id
		else:
			break
	file_name = movie_id + '.json'

	text = None
	if os.path.exists('data/movie_details/' + file_name):
		f = open('data/movie_details/' + file_name)
		text = f.read()
		jload = json.loads(text)
		return jload
	if text is None:
		# Task 9
		time.sleep(sleep_time)
		
		# Task 4
		page = requests.get(movie_url)
		soup = BeautifulSoup(page.text,'html.parser')

		# Here I scrape movie name
		title_div = soup.find('div',class_="title_wrapper").h1.get_text()
		movie_name = ''
		for i in title_div:
			if '(' not in i:
				movie_name = (movie_name + i).strip()
			else:
				break

		# In this div where I get all the other things like runtime,gener and more
		sub_div  = soup.find('div',class_="subtext")
		
		# Here I scrape movie runtime.
		runtime = sub_div.find('time').get_text().strip()
		runtime_hours = int(runtime[0])*60
		if 'min' in sub_div:
			runtime_minutes = int(movie_runtime[3:].strip('min'))
			movie_runtime = runtime_hours + runtime_minutes
		else:
			movie_runtime = runtime_hours 

		# Here I scrape movie gener.
		gener = sub_div.find_all('a')
		gener.pop()
		movie_gener = [i.get_text() for i in gener]

		# In This div i get movie bio and movie director
		summary = soup.find('div', class_="plot_summary")

		# Here I scrape movie bio
		movie_bio = summary.find('div', class_="summary_text").get_text().strip()

		# Here I scrape director of the movie.
		director = summary.find('div', class_="credit_summary_item")
		director_list = director.find_all('a')
		movie_directors=[]
		for i in director_list:
			if '1 more credit' not in i.get_text():
				movie_directors.append(i.get_text().strip())

		# In this div i get country and language details.
		extra_details = soup.find('div', attrs={"class":"article","id":"titleDetails"})
		list_of_divs = extra_details.find_all('div')
		for div in list_of_divs:
			tag_h4 =  div.find_all('h4')
			for text in tag_h4:
				if 'Language:' in text:
					tag_anchor = div.find_all('a')
					movie_language = [language.get_text() for language in tag_anchor]
				elif 'Country:' in text:
					tag_anchor = div.find_all('a')
					movie_country = ''.join([country.get_text() for country in tag_anchor])

		# Here I scrape Poster Image_Url.
		movie_poster_link = soup.find('div', class_="poster").a['href']
		movie_poster= "https://www.imdb.com" + movie_poster_link

		# Bouns Task 1
		# Here I scrap More like this:
		im_id =[]
		mm_name = []  # Most view movie : mm
		more_like = soup.find('div',class_='rec_slide')
		related_movie = more_like.find('div',class_='rec_page')
		all_movie = related_movie.find_all('div')
		for i in all_movie:
			if i.a:
				_id = i.a['href'][7:16]
				im_id.append(_id)
				mm = i.a.img['title']
				mm_name.append(mm)
	
		# Task 13
		# Here I scrape cast url.
		movie_details = soup.find('div', attrs={"class":"article","id":"titleCast"})
		cast_main_div = movie_details.find('div', class_="see-more").a['href']
		cast_url = movie_poster[:37] + cast_main_div
		cast_detail = scrape_movie_cast(cast_url)

		# Task 4
		# Here I create Dic for movie-details
		movie_detail_dic = {'name':'','director':'','bio':'','runtime':'','gener':'','language':'','country':'','poster_img_url':'','cast':'','similar_movie':[]}

		movie_detail_dic['name'] = movie_name
		movie_detail_dic['director'] = movie_directors
		movie_detail_dic['bio'] = movie_bio
		movie_detail_dic['runtime'] = movie_runtime
		movie_detail_dic['gener'] = movie_gener
		movie_detail_dic['language'] = movie_language
		movie_detail_dic['country'] = movie_country
		movie_detail_dic['poster_img_url'] = movie_poster
		# Task 13
		movie_detail_dic['cast'] = cast_detail

		# Bonus Task 1
		similar_movie_dict = {'imdb_id':'','name':''}
		for m in range(len(mm_name)):
			similar_movie_dict['imdb_id'] = im_id[m]
			similar_movie_dict['name'] = mm_name[m]
			movie_detail_dic['similar_movie'].append(similar_movie_dict)
			similar_movie_dict = {'imdb_id':'','name':''}

		# Task 8
		file1 = open('data/movie_details/'+ file_name,'w')
		raw = json.dumps(movie_detail_dic)
		file1.write(raw)
		file1.close()
		
		return movie_detail_dic

# url1 = top_movies[0]['url']
# movie_detail = scrape_movie_details(url1)
# print(movie_detail)

# Task 5
def get_movie_list_details(movie_list):
	movies_detail_list = []
	for i in movie_list:
		detail = scrape_movie_details(i['url'])
		movies_detail_list.append(detail)
	return movies_detail_list
movies_detail = get_movie_list_details(top_movies)       
# print(movies_detail)

# Task 6
def analyse_movies_language(movies_list):
	language_list = []
	for movie in movies_list:
		for j in movie['language']:
			if j not in language_list:
				language_list.append(j)
	analyse__language ={lang:0 for lang in language_list} 
	for lang in language_list:
		for movie in movies_list:
			if lang in movie['language']:
				analyse__language[lang] +=1
	return analyse__language
# movies_detail_list = get_movie_list_details(top_movies[:10])
# language_analysis = analyse_movies_language(movies_detail_list)
# print(language_analysis)

# Task7
def analyse_movies_directors(movies_list):
	director_list = []
	for movie in movies_list:
		for j in movie['director']:
			if j not in director_list:
				director_list.append(j)
	analyse__director ={director:0 for director in director_list} 
	for director in director_list:
		for movie in movies_list:
			if director in movie['director']:
				analyse__director[director] +=1
	return analyse__director

# movies_detail_list = get_movie_list_details(top_movies[:10])
# director_analysis = analyse_movies_directors(movies_detail_list)
# print(director_analysis)

# # Task 8,9 are include in Task4

# Task 10
def  analyse_language_and_directors(movies_list):
	directors_dic = {}
	for movie in movies_list:
		for director in movie['director']:
			directors_dic[director] = {}
	for i in range(len(movies_list)):
		for director in directors_dic:
			if director in movies_list[i]['director']:
				for language in movies_list[i]['language']:
					directors_dic[director][language] = 0
	for i in range(len(movies_list)):
		for director in directors_dic:
			if director in movies_list[i]['director']:
				for language in movies_list[i]['language']:
					directors_dic[director][language] +=1
	return directors_dic
	# pprint.pprint(directors_dic) 
# director_by_language = analyse_language_and_directors(movies_detail)
# print(director_by_language)


# Task 11
def analyse_movie_gener(movies_list):
	gener_list = []
	for movie in movies_list:
		gener = movie['gener']
		for i in gener:
			if i not in gener_list:
				gener_list.append(i)

	analyse_gener = {gener_type:0 for gener_type in gener_list}
	for gener_type in gener_list:
		for movie in movies_list:
			if gener_type in movie['gener']:
				analyse_gener[gener_type] +=1
	return analyse_gener
# gener_analysis = analyse_movie_gener(movies_detail)
# print(gener_analysis)

# Task 12 : Checked the cast_scrapeer.py file 
# Task 13 included in Task 4

# Task 14
def analyse_co_actors(movies_list):
	actors_id = {}
	cast = ''
	for movie in movies_list:
		_id =movie['cast'][0]
		actors_id[_id['imdb_id']] = {'name':_id['name'],'frequent_co_actors':[]}
		for movie1 in movies_list:
			flag = 0
			cast = movie1['cast'][0]
			if _id['imdb_id'] == cast['imdb_id']:
				a = actors_id[cast['imdb_id']]['frequent_co_actors']
				for cast1 in movie1['cast'][1:5]:
					if not any(d['imdb_id'] == cast1['imdb_id'] for d in a):
						a.append({'imdb_id':cast1['imdb_id'],'name':cast1['name'],'num_movies':flag+1})
					else:
						for i in a:
							if i['imdb_id'] == cast1['imdb_id']:
								i['num_movies'] +=1
	return actors_id
	# pprint.pprint(actors_id)
	
co_actors_analysis = analyse_co_actors(movies_detail)
print(co_actors_analysis)

# Task 15
def analyse_actors(movies_list):
	actors_dict = {}
	for movie in movies_list:
		flag = 0
		for cast in movie['cast']:
			id_ = cast['imdb_id']
			for cast1 in movie['cast']:
				id_2 = cast1['imdb_id']
				if id_2 == id_:
					flag +=1
				if flag >1:
					actors_dict[id_] = {'name':cast['name'],'num_movies':flag}
					
	return actors_dict

# actors_analysis = analyse_actors(movies_detail)
# print(actors_analysis)
