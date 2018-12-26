from urllib.request import urlopen
from bs4 import BeautifulSoup
import pprint
def scrap_top_list(position_l,name_l,year_l,rating_l):
	Top_Movies = []
	details ={'position':'','name':'','year':'','rating':''}
	for i in range(0,len(position_l)):
		details['position'] = int(position_l[i])
		details['name'] = str(name_l[i])
		year_l[i] = year_l[i][1:5]
		details['year'] = int(year_l[i])
		details['rating'] = float(rating_l[i])
		Top_Movies.append(details.copy())
	return (Top_Movies)
def top_movie_list():
	url = "https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in"
	html = urlopen(url)
	soup = BeautifulSoup(html, 'lxml')

	title = soup.title
	main_div = soup.find('div',class_="lister")
	t_body = main_div.find('tbody', class_="lister-list")
	trs = t_body.find_all('tr')

	title = []
	ratings = []
	year = []
	position=[]
	for tr in trs:
		titleColumn = tr.find('td',class_="titleColumn").a.get_text()
		title.append(titleColumn)

		yearcolumn = tr.find('td',class_="titleColumn").span.get_text()
		year.append(yearcolumn)

		ratingColumn = tr.find('td',class_="ratingColumn imdbRating").strong.get_text()
		ratings.append(ratingColumn)

	position = [str(i) for i in range(1,len(trs)+1)]

	x = scrap_top_list(position,title,year,ratings)


	file1 = open('top_movies.txt','w+')
	for i in x:
		data = ''
		for j in i:
			data =  data + str(i[j]) + "   "
		file1.write(data)
		file1.write('\n\n')
	file1.close()
	return x

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
	file2 = open('movies_by_year.txt','w+')
	
	for i in movie_dict:
		data = movie_dict[i]
		file2.write("The list of movies in "+ str(i) + ":-\n")
		number2 = 1
		for j in data:
			file2.write(str(number2)+ ". " + j['name'] +" \n")
			number2 +=1
		file2.write("\n\n")
	file2.close()
	return movie_dict
	#pprint.pprint(movie_dict)
# print(group_by_year(top_movie_list()))
def group_by_decade(movies):
	years = []
	movie_decade = {}
	for i in movies.keys():
		years.append(i)
	years.sort()
	decade_list = []
	for value in years:
		reminder = value % 10
		subtract = value - reminder
		if subtract not in decade_list:
			decade_list.append((subtract))
	for decades in decade_list:
		movie_decade[decades] = []
	for k,v in movies.items():
		years = k
		values = v
		for i in movie_decade:
			if years in range(i,i+10):
				for x in values:
					movie_decade[i].append(x)
	file3 = open('Movie_by_decade.txt','w+')
	data1 = ''
	for i in movie_decade:
		year = i
		data = movie_decade[i]
		file3.write("The list of movies in " + str(year) +'s Decade:-\n')
		number3 = 1
		for j in data:
			file3.write(str(number3)+". "+j['name']+ " \n")
			number3+=1
		file3.write('\n\n')
	file3.close()
	# return movie_decade
	pprint.pprint(movie_decade)
print(group_by_decade(group_by_year(top_movie_list())))
