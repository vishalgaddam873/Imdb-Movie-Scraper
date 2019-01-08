from bs4 import BeautifulSoup
import requests

url = "https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in"
page = requests.get(url)
soup = BeautifulSoup(page.text,'html.parser')

def scrap_top_list():
	main_div = soup.find('div', class_='lister')
	tbody = main_div.find('tbody', class_='lister-list')
	trs = tbody.find_all('tr')

	movie_ranks =[]
	movie_name = []
	year_of_realease = []
	movie_urls = []
	movie_ratings = []

	for tr in trs:
		# Here we scrap ranks of movies. 
		position = tr.find('td', class_ ="titleColumn").get_text().strip()
		rank = ''
		for i in position:
			if '.' not in i:
				rank = rank + i	
			else:
				break
		movie_ranks.append(rank)
		
		# Here we scrap movie name or movie title	
		title = tr.find('td', class_ ="titleColumn").a.get_text()
		movie_name.append(title)

		# Here we scrap year of movie released.
		year = tr.find('td',class_ = "titleColumn").span.get_text()
		year_of_realease.append(year)

		# Here we scrap imdb ratings of movies.
		imdb_rating = tr.find('td',class_="ratingColumn imdbRating").strong.get_text()
		movie_ratings.append(imdb_rating)

		# Here we scrap movies urls or links.
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
		Top_Movies.append(details.copy())
	return (Top_Movies)
scrap = scrap_top_list()
#pprint.pprint(scrap)
#print(scrap)

def group_by_year(movies):
	years = []
	movie_dict = {}
	for i in movies:
		year = i['year']
		if year not in years:
			years.append(year)
	for i in years:
		movie_dict[i] = []

	for j in movies:
		year = j['year']
		for k in movie_dict:
			if str(k) == str(year):
				movie_dict[k].append(j)
	file2 = open('data/movies_by_year.txt','w+')

	for i in movie_dict:
		data = movie_dict[i]
		file2.write(str(i) + "\n")
		number2 = 1
		for j in data:
			file2.write(str(number2)+ ". " + j['name'] +" \n")
			number2 +=1
		file2.write("\n\n")
	file2.close()
	return movie_dict
# pprint.pprint(group_by_year(scrap))
#print(group_by_year(scrap))

def group_by_decade(movies):
	movies_by_year = group_by_year(movies)
	movie_decade = {}
	decade_list = []
	for value in movies_by_year:
		reminder = value % 10
		subtract = value - reminder
		if subtract not in decade_list:
			decade_list.append((subtract))
	decade_list.sort()
	for decades in decade_list:
		movie_decade[decades] = []

	for i in movie_decade:
		for j in movies_by_year:
			if j in range(i,i+10):
				movie_decade[i] += movies_by_year[j]
	file3 = open('data/Movie_by_decade.txt','w+')
	for i in movie_decade:
		year = i
		data = movie_decade[i]
		file3.write(str(year) +'s \n')
		number3 = 1
		for j in data:
			file3.write(str(number3)+". "+j['name']+ " \n")
			number3+=1
		file3.write('\n\n')
	file3.close()
	return movie_decade
	#pprint.pprint(movie_decade)
# print(group_by_decade(scrap))

#Task 4
def get_movie_details():
	movies_urls = soup.find('div',class_="lister")
	url_t_body = movies_urls.find('tbody', class_="lister-list")
	url_trs = url_t_body.find_all('tr')

	url_list = []
	for links in url_trs:
		url_t_data = links.find_all('td', class_="titleColumn")
		for url_link in url_t_data:
			b = url_link.a['href']
			movie_url = "https://www.imdb.com" + b 
			url_list.append(movie_url)
	return url_list			
movie_detail_url = get_movie_details()

def extract_movie_detail(movie_url):
	html_doc = urlopen(movie_url)
	soup = BeautifulSoup(html_doc,'lxml')

	title_tag = soup.title.get_text()

	# Here I scrap director and movie_bio data
	main_div = soup.find('div', class_="plot_summary")
	director_of_movie = main_div.find('div', class_="credit_summary_item")
	director = [director.get_text() for director in director_of_movie.find_all('a')]	
	movie_bio = main_div.find('div',class_="summary_text")

	# Here I scrap Movie name
	name = soup.find('div', class_='title_wrapper').h1.get_text()

	# Here I scrap the runtime of the movie
	title_div = soup.find('div', class_="title_bar_wrapper")
	title_subtext = title_div.find('div', class_="subtext")
	movie_runtime = title_subtext.find('time').get_text().strip()
	runtime_hours = int(movie_runtime[0]) * 60
	if 'min' in title_subtext:
		runtime_minutes = int(movie_runtime[3:].strip('min'))
		total_runtime = runtime_hours + runtime_minutes
	else:
		total_runtime = runtime_hours 

	

	# Here I scrap Gener of the movies
	genre = title_subtext.find_all('a')
	genre.pop()
	Genre = [i.get_text() for i in genre]
	
	# Here I scrap the movie poster link
	movie_poster = soup.find('div', class_="poster").a['href']
	movie_poster_link = "https://www.imdb.com" + movie_poster

	# Here I scrap the moive_language and movie_country
	movie_details = soup.find('div', attrs={"class":"article","id":"titleDetails"})
	list_of_divs = movie_details.find_all('div')
	for div in list_of_divs:
		tag_h4 =  div.find_all('h4')
		for text in tag_h4:
			if 'Language:' in text:
				tag_anchor = div.find_all('a')
				movie_language = [language.get_text() for language in tag_anchor]
			elif 'Country:' in text:
				tag_anchor = div.find_all('a')
				movie_country = [country.get_text() for country in tag_anchor]

	movie_detail_dic = {'name':'','director':'','movie_bio':'','runtime':'','gener':'','language':'','country':'','poster_img_url':''}
	
	movie_detail_dic['name'] = name[:-8]
	movie_detail_dic['director'] = director
	movie_detail_dic['movie_bio'] = movie_bio.get_text().strip()
	movie_detail_dic['runtime'] = total_runtime
	movie_detail_dic['gener'] = Genre
	movie_detail_dic['language'] = movie_language
	movie_detail_dic['country'] = movie_country
	movie_detail_dic['poster_img_url'] = movie_poster_link

	return movie_detail_dic

# for links in movie_detail_url:
# 	print(extract_movie_detail(links))

# Task 5
def get_movie_list_details(movies):
	movie_list = []
	first_20 = movies[:20]
	for i in first_20:
		urls = i['url']
		a = extract_movie_detail(urls)
		movie_list.append(a)
	return movie_list
movie_list_detail = get_movie_list_details(scrap)
# print(movie_list_detail)

# Task 6
def analyse_movies_language(movies):
	language_list = []
	for i in movies:
		a = i['language']
		for j in a:
			if j not in language_list:
				language_list.append(j)
	analyse__language ={lang:0 for lang in language_list} 
	for lang in language_list:
		for movie in movies:
			if lang in movie['language']:
				analyse__language[lang] +=1
	return analyse__language

language_analyse = analyse_movies_language(movie_list_detail)

# Task 7
def analyse_movies_directors(movies):
	director_list = []
	for i in movies:
		a = i['director']
		for j in a:
			if j not in director_list:
				director_list.append(j)
	analyse__director ={director:0 for director in director_list} 
	for director in director_list:
		for movie in movies:
			if director in movie['director']:
				analyse__director[director] +=1
	return analyse__director
director_analyse = analyse_movies_directors(movie_list_detail)
# print(director_analyse)

# Task 8
def get_see_full_cast_url(movie_url):
# From this function I scrap the see_full_cast link urls from movie details page.
	html_doc = urlopen(movie_url)
	soup = BeautifulSoup(html_doc,'lxml')

	# Here I call extract_movie_detail and get poster_img_url
	movies_urls = extract_movie_detail(movie_url)
	imgae_url = movies_urls['poster_img_url']

	# Here I scrap cast url.
	movie_details = soup.find('div', attrs={"class":"article","id":"titleCast"})
	cast_main_div = movie_details.find('div', class_="see-more").a['href']
	cast_url = imgae_url[:37] + cast_main_div

	cast_html = urlopen(cast_url)
	cast_soup = BeautifulSoup(cast_html,'lxml')

	detail_list = []

	cast_detail = {'cast_list':[]}
	# Here I scrap movie name and Cast details.
	main_div = cast_soup.find('div', class_='article listo')
	movie_name = main_div.find('div',class_='parent').h3.a.get_text()
	cast_table = main_div.find('table', class_='cast_list')
	cast_table_trs = cast_table.find_all('tr')
	for tr in cast_table_trs:
		cast_tds = tr.find_all('td')
		for td in cast_tds:
			td_image = td.find_all('img')
			for image in td_image:
				cast_detail['cast_list'].append(image['title'])
	detail_list.append(cast_detail)
	cast_dic = {movie_name:detail_list}
	return cast_dic

for links in movie_detail_url:
	print(get_see_full_cast_url(links))

