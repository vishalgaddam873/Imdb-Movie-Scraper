from bs4 import BeautifulSoup
import requests,json,os

# Task 12

def get_cast_url(movie_url):
	# From this function I scrap the see_full_cast link urls from movie details page.
	html_doc = requests.get(movie_url)
	soup = BeautifulSoup(html_doc.text,'html.parser')

	# Here I call extract_movie_detail and get poster_img_url
	movie = scrap_movie_details(movie_url)
	json_2_dic = json.loads(movie)
	imgae_url = json_2_dic['poster_img_url']
	movie_name = json_2_dic['name']

	# Here I scrap cast url.
	movie_details = soup.find('div', attrs={"class":"article","id":"titleCast"})
	cast_main_div = movie_details.find('div', class_="see-more").a['href']
	cast_url = imgae_url[:37] + cast_main_div
	return cast_url

# url2 = scrap[0]['url']
# movie_cast_url = get_cast_url(url2)

def scrape_movie_cast(movie_cast_url):
	cast_id = ''
	for _id in movie_cast_url[27:]:
		if '/' not in _id:
			cast_id += _id
		else:
			break
	file_name1 = cast_id + '_cast.json'

	text = None
	if os.path.exists('data/cast/' + file_name1):
		f = open('data/cast/' + file_name1)
		text = f.read()
		json_2_list = json.loads(text)
		return json_2_list

	if text is None:
		cast_html = requests.get(movie_cast_url)
		cast_soup = BeautifulSoup(cast_html.text,'html.parser')

		cast_name_list = []
		cast_id_imdb = []
		cast_detail_list = []
		# Here I scrap movie name and Cast details.
		main_div = cast_soup.find('div', class_='article listo')
		movie_name = main_div.find('div',class_='parent').h3.a.get_text()
		cast_table = main_div.find('table', class_='cast_list')
		cast_table_trs = cast_table.find_all('tr')
		# cast_table_trs.pop(0)
		for tr in cast_table_trs:
			cast_tds = tr.find_all('td')
			if len(cast_tds) > 1:
				cast_imdb_id = cast_tds[0].a['href'][6:]
				_id = ''
				for _cast_id in cast_imdb_id:
					if '/' in _cast_id:
						break
					else:
						_id += _cast_id 
				cast_id_imdb.append(_id)

				cast_name = cast_tds[1].a.get_text().strip('\n')
				cast_name_list.append(cast_name.strip())

		cast_dic = {'imdb_id':'','name':''}
		for i in range(len(cast_name_list)):
			cast_dic['imdb_id']  = cast_id_imdb[i]
			cast_dic['name'] = cast_name_list[i] 
			cast_detail_list.append(cast_dic)
			cast_dic = {'imdb_id':'','name':''}
	
		file1 = open('data/cast/'+ file_name1,'w')
		raw   = json.dumps(cast_detail_list)
		file1.write(raw)
		file1.close()
		return cast_detail_list
# cast_detail = scrape_movie_cast(movie_cast_url)
# print(cast_detail)

