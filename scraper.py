from bs4 import BeautifulSoup as BS
import requests, pprint, json, os, random, time

#Task1
# Here we scrape the list of 250 movies data.
def scrape_top_list():
	url = "https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in"
	page = requests.get(url)
	soup = BS(page.text,'html.parser')
	TopMoviesList = []
	tbody = soup.find('tbody', class_='lister-list')
	trs = tbody.find_all('tr')
	for tr in trs:
		# Here we scrape rank,name,released year of movies.
		movie_data = tr.find('td', class_ ="titleColumn").get_text().strip().split()
		# Here we create dictionary for movie details
		movies_detail ={'position':'','name':'','year':'','rating':'','url':''}
		movies_detail['position'] = int(movie_data[0].strip('.'))
		movies_detail['year'] =  int(movie_data[-1].strip("()"))
		movie_data.pop(0)
		movie_data.pop(-1)
		movies_detail['name'] = " ".join(movie_data)
		movies_detail['rating'] = float(tr.find('strong').get_text())
		movies_detail['url'] = "https://www.imdb.com" + tr.find('a').get('href')[0:17]
		# Here we appending the movie details dictonary in TopMoviesList
		TopMoviesList.append(movies_detail)

	return (TopMoviesList)
top_movies = scrape_top_list()
# pprint.pprint(top_movies)

#Task2
# Here we group the movies by year
def group_by_year(movie_list):
	movies_by_year = {}
	for movie in movie_list:
		movies_by_year[movie['year']] = []
	for year in movies_by_year:
		for Movie_  in movie_list:
			if year == Movie_['year']:
				movies_by_year[year].append(Movie_)
	return movies_by_year
# movie_analysis_by_year = group_by_year(top_movies)
# pprint.pprint(movie_analysis_by_year)

#Task3
# Here we group the movie by decade
def group_by_decade(movie_list):
	movies_by_decade = {}
	for movie in movie_list:
		division = movie['year'] // 10
		decade_year = division * 10
		movies_by_decade[decade_year] = []
	for decade in movies_by_decade:
		for Movie_ in movie_list:
			division_ = Movie_['year'] // 10
			decade_year_ = division_ * 10
			if decade == decade_year_:
				movies_by_decade[decade].append(Movie_)

	return movies_by_decade
# movie_analysis_by_decade = group_by_decade(top_movies)
# pprint.pprint(movie_analysis_by_decade)

# Task 12
def scrape_movie_cast(movie_cast_url):
	file_name = movie_cast_url[27:36] + '_cast.json'
	if os.path.exists('Database/movies_cast_cache/' + file_name):
		with open('Database/movies_cast_cache/' + file_name) as content:
			text = content.read()
			caste_details = json.loads(text)
			return caste_details
	else:
		cast_html = requests.get(movie_cast_url)
		cast_soup = BS(cast_html.text,'html.parser')
		cast_detail_list = []
		# Here we scrape Cast details.
		main_div = cast_soup.find('div', class_='article listo')
		cast_table = main_div.find('table', class_='cast_list')
		cast_table_trs = cast_table.find_all('tr')
		cast_table_trs.pop(0)
		for tr in cast_table_trs:
			cast_tds = tr.find_all('td')
			if len(cast_tds) > 1:
				movie_cast = {'imdb_id':'','name':''}
				movie_cast['imdb_id']  = cast_tds[1].a['href'][7:15]
				movie_cast['name'] = cast_tds[1].get_text().strip()
				cast_detail_list.append(movie_cast)
		with open('Database/movies_cast_cache/'+ file_name,'w') as file:
			raw  = json.dumps(cast_detail_list,indent=4, sort_keys=True)
			file.write(raw)
			file.close()
		return cast_detail_list
# Here the url is Anand movie
# cast_url = 'https://www.imdb.com/title/tt0066763/fullcredits?ref_=tt_cl_sm#cast'
# movie_caste = scrape_movie_cast(cast_url)
# pprint.pprint(movie_caste)

# Task 4 and 8,9,13
def scrape_movie_details(movie_url):
	file_name = movie_url[27:].strip('/') + '.json' # Task 8
	if os.path.exists('Database/movies_cache/' + file_name):
		with open('Database/movies_cache/' + file_name) as content:
			text = content.read()
			movie_details = json.loads(text)
		return movie_details
	else:
		time.sleep(random.randint(1,3)) # Task 9
		page = requests.get(movie_url) # Task 4
		soup = BS(page.text,'html.parser')
		# Here we scrape movie name
		movie_name = soup.find('div',class_="title_wrapper").h1.get_text().split()
		movie_name.pop()
		# Here we scrape all the other things like runtime,gener and more
		movie_detail = soup.find('div',class_='plot_summary')
		movie_bio = movie_detail.find('div',class_='summary_text').get_text().strip()
		movie_directors = movie_detail.find('div', class_='credit_summary_item')
		directors = movie_directors.find_all('a')
		directors_list = [director.get_text() for director in directors]
		# Here we get poster image url
		poster_image_url = soup.find('div', class_='poster').a.img['src']
		movie_data = soup.find('div',class_="title_wrapper")
		time_gener_div = movie_data.find('div',class_='subtext')
		geners = time_gener_div.find_all('a')
		geners.pop()
		gener_list = [gener.get_text() for gener in geners]
		# Here we get movie runtime
		movie_runtime = time_gener_div.find('time').get_text().strip().split()
		minutes = 0
		for Time in movie_runtime:
		    if 'h' in Time:
		        hours_to_min = int(Time.strip('h')) * 60
		    elif 'min' in Time:
		        minutes = int(Time.strip('min'))
		runtime = hours_to_min + minutes

		country_lang_div = soup.find('div',attrs = {'class':'article','id':'titleDetails'})
		list_of_divs = country_lang_div.find_all('div',class_='txt-block')
		for check_div in list_of_divs:
		    detail_list = check_div.get_text().split()
		    if detail_list[0] == 'Country:':
		        country = check_div.find('a').get_text()
		    elif detail_list[0] == 'Language:':
		        a_tag_list = check_div.find_all('a')
		        language_list = [language.get_text() for language in a_tag_list]
		# Task 13: Here I scrape cast url.
		details = soup.find('div', attrs={"class":"article","id":"titleCast"})
		cast_main_div = details.find('div', class_="see-more").a['href']
		cast_url = movie_url[:37] + cast_main_div
		cast_detail = scrape_movie_cast(cast_url)
		print(" ".join(movie_name))
		movie_details = {'movieName':" ".join(movie_name),
			'director':directors_list,
			'bio':movie_bio,
			'runtime':runtime,
			'gener':gener_list,
			'language':language_list,
			'country':country,
			'poster_img_url':poster_image_url,
			'cast':cast_detail,# Task 13
			'similar_movie':[]}
		# Bonus Task 1: Here I scrap More like this:

		more_like = soup.find('div',class_='rec_slide')
		if more_like != None:
			related_movie = more_like.find('div',class_='rec_page')
			all_movie = related_movie.find_all('div')
			for movie in all_movie:
				if movie.a:
					similar_movies = {'imdb_id':movie.a['href'][7:16],
					'name':movie.a.img['title']}
					movie_details['similar_movie'].append(similar_movies)
			with open('Database/movies_cache/'+ file_name,'w') as file: # Task 8
				raw = json.dumps(movie_details,indent=4, sort_keys = True)
				file.write(raw)
				file.close()
			return movie_details
# url1 = top_movies[0]['url']
# movie_detail = scrape_movie_details(url1)
# pprint.pprint(movie_detail)

# Task 5
def get_movie_list_details(movie_list):
	movies_details_list = []
	for i in movie_list:
		details = scrape_movie_details(i['url'])
		movies_details_list.append(details)
	return movies_details_list
movies_details = get_movie_list_details(top_movies)
pprint.pprint(movies_details)

# Task 6
# Here we group the movies by languages
def analyse_movies_language(movies_list):
	movies_by_language = {}
	for movie in movies_list:
		for language in movie['language']:
			movies_by_language[language] = 0
	for lang in movies_by_language:
		for movie_ in movies_list:
			if lang in movie_['language']:
				movies_by_language[lang] +=1
	return movies_by_language
# movies_details_list = get_movie_list_details(top_movies[:10])
# language_analysis = analyse_movies_language(movies_details_list)
# pprint.pprint(language_analysis)

# Task7
def analyse_movies_directors(movies_list):
	movies_by_directors = {}
	for movie in movies_list:
		for director in movie['director']:
			movies_by_directors[director] = 0
	for direct in movies_by_directors:
		for movie_ in movies_list:
			if direct in movie_['director']:
				movies_by_directors[direct] +=1
	return movies_by_directors
# movies_details_list = get_movie_list_details(top_movies[:10])
# director_analysis = analyse_movies_directors(movies_details_list)
# pprint.pprint(director_analysis)

# Task 8,9 are include in Task4

# Task 10
def  analyse_language_and_directors(movies_list):
	directors_by_language = {}
	for movie in movies_list:
		for director in movie['director']:
			directors_by_language[director] = {}

	for director_key in directors_by_language:
		for movie_ in movies_list:
			if director_key in movie_['director']:
				for language in movie_['language']:
					directors_by_language[director_key][language] = 0

	for director_ in directors_by_language:
		for Movie_ in movies_list:
			if director_ in Movie_['director']:
				for lang in Movie_['language']:
					directors_by_language[director_][lang] +=1
	return directors_by_language
# directors_by_language_analysis = analyse_language_and_directors(movies_details)
# pprint.pprint(directors_by_language_analysis)

# Task 11
def analyse_movie_gener(movies_list):
	movies_by_gener = {}
	for movie in movies_list:
		for gener in movie['gener']:
			movies_by_gener[gener] = 0

	for gener_key in movies_by_gener:
		for Movie_ in movies_list:
			if gener_key in Movie_['gener']:
				movies_by_gener[gener_key] +=1
	return movies_by_gener
# movies_by_gener_analysis = analyse_movie_gener(movies_details)
# pprint.pprint(movies_by_gener_analysis)

# Task 12 : Before Task 4
# Task 13 included in Task 4

# Task 14
def analyse_co_actors(movies_list):
	actors_dict = {}
	for movie in movies_list:
		actors_dict[movie['cast'][0]['imdb_id']] = {
						'name':movie['cast'][0]['name'],'frequent_co_actors':[]}
	co_actors_dict = {'imdb_id':'','name':'','num_movies':0}
	for actor in actors_dict:
		co_actors_list = actors_dict[actor]['frequent_co_actors']
		flag = 0
		for cast in movies_list:
			lead_cast_id = cast['cast'][0]['imdb_id']
			for co_actors in cast['cast'][:5]:
				if actor == co_actors['imdb_id']:
					for co_actors_1 in cast['cast'][:5]:
						if co_actors_1['imdb_id'] != actor:
							co_actors_dict['imdb_id'] = co_actors_1['imdb_id']
							co_actors_dict['name'] = co_actors_1['name']
							if not any(d['imdb_id'] == co_actors_dict['imdb_id'] for d in co_actors_list):
								co_actors_dict['num_movies'] = 1
								actors_dict[actor]['frequent_co_actors'].append(co_actors_dict)
								co_actors_dict = {'imdb_id':'','name':'','num_movies':0}
							else:
								for d in co_actors_list:
									if co_actors_dict['imdb_id'] == d['imdb_id']:
										d['num_movies'] +=1
	return actors_dict
# analysis_co_actors = analyse_co_actors(movies_details)
# pprint.pprint(analysis_co_actors)

# Task 15
def analyse_actors(movies_list):
	actors_dict = {}
	for movie in movies_list:
		for actor in movie['cast']:
			flag = 0
			for Movie_ in movies_list:
				for Actor_ in Movie_['cast']:
					if actor['imdb_id'] == Actor_['imdb_id']:
						flag +=1
			if flag > 1:
				actors_dict[actor['imdb_id']] = {'name':actor['name'],'num_movies':flag}
	return actors_dict
# actors_analysis = analyse_actors(movies_details)
# pprint.pprint(actors_analysis)
