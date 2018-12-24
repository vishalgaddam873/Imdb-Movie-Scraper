#Format
# [
# {
# 'name': 'Anand', 
# 'year_of_release': 1971, 
# 'position': 1, 
# 'rating': 8.7} ,
#  {}, {}, {}, {}
# ]
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

