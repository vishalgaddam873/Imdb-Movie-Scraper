from urllib.request import urlopen
from bs4 import BeautifulSoup
import pprint

url = "https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in"
html = urlopen(url)
soup = BeautifulSoup(html,'lxml')


def top_movie_list(position_l,name_l,year_l,rating_l,url_l):
	Top_Movies = []
	details ={'position':'','name':'','year':'','rating':'','url':''}
	for i in range(0,len(position_l)):
		details['position'] = int(position_l[i])
		details['name'] = str(name_l[i])
		year_l[i] = year_l[i][1:5]
		details['year'] = int(year_l[i])
		details['rating'] = float(rating_l[i])
		details['url'] = url_l[i]
		Top_Movies.append(details.copy())
	return (Top_Movies)

def scrap_top_list():
	title = soup.title
	main_div = soup.find('div',class_="lister")
	t_body = main_div.find('tbody', class_="lister-list")
	trs = t_body.find_all('tr')

	title = []
	ratings = []
	year = []
	position=[]
	movie_urls = []
	for tr in trs:
		titleColumn = tr.find('td',class_="titleColumn").a.get_text()
		title.append(titleColumn)

		yearcolumn = tr.find('td',class_="titleColumn").span.get_text()
		year.append(yearcolumn)

		ratingColumn = tr.find('td',class_="ratingColumn imdbRating").strong.get_text()
		ratings.append(ratingColumn)

		url_t_data = tr.find('td', class_="titleColumn").a['href']
		movie_url = "https://www.imdb.com" + url_t_data
		movie_urls.append(movie_url)
	position = [str(i) for i in range(1,len(trs)+1)]
	x = top_movie_list(position,title,year,ratings,movie_urls)

	file1 = open('data/top_movies.txt','w+')
	for i in x:
		data = ''
		for j in i:
			data =  data + str(i[j]) + "   "
		file1.write(data)
		file1.write('\n\n')
	file1.close()
	return x
scrap = scrap_top_list()
# print(scrap)

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
	# pprint.pprint(movie_dict)
# print(group_by_year(scrap))

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
print(director_analyse)