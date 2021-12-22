

import random

super_proxy = "super_proxy"
country_url_list = [

	"http://%s-country-tm-session-%s:%s@"+super_proxy+":%d",
	"http://%s-country-de-session-%s:%s@"+super_proxy+":%d",
	"http://%s-country-ar-session-%s:%s@"+super_proxy+":%d",
	"http://%s-country-my-session-%s:%s@"+super_proxy+":%d",
	"http://%s-country-gb-session-%s:%s@"+super_proxy+":%d",
	"http://%s-country-ge-session-%s:%s@"+super_proxy+":%d",
	"http://%s-country-vn-session-%s:%s@"+super_proxy+":%d",
	"http://%s-country-in-session-%s:%s@"+super_proxy+":%d",
	"http://%s-country-ie-session-%s:%s@"+super_proxy+":%d",
	"http://%s-country-ae-session-%s:%s@"+super_proxy+":%d",
	"http://%s-country-ag-session-%s:%s@"+super_proxy+":%d",



]

country_url_choice = country_url_list[random.randint(0, len(country_url_list) -1)]
print(country_url_choice)