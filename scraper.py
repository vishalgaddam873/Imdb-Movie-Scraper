from urllib.request import urlopen
from bs4 import BeautifulSoup

def scrap_top_list(position_l,name_l,year_l,rating_l):
	Top_Movies = []
	details ={'position':'','name':'','year':'','rating':''} 
	for i in range(0,250):
		details['position'] = position_l[i]
		details['name'] = name_l[i]
		details['year'] = year_l[i]
		details['rating'] = rating_l[i]
		Top_Movies.append(details.copy())
	return (Top_Movies)



url = "https://www.imdb.com/india/top-rated-indian-movies/?ref_=nv_mv_250_in"
html = urlopen(url)
soup = BeautifulSoup(html, 'lxml')

title = soup.title
main_div = soup.find('div',class_="lister")
t_body = main_div.find('tbody', class_="lister-list")
trs = t_body.find_all('tr')
titleColumn = ''
ratingColumn = ''
yearcolumn = ''

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

position= [str(i) for i in range(1,len(trs)+1)]

x = scrap_top_list(position,title,year,ratings)
print(x)
file1 = open('movie.txt','w+')
for i in x:
	data = ''
	for j in i:
		data =  data + str(i[j]) + "   "
	file1.write(data)
	file1.write('\n\n')
file1.close()
