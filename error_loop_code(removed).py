		if error_loop_count < 10:
			try:
				#----function meat 
				res = proxy_request(company_page_link)
				soup = bs4.BeautifulSoup(res, 'html.parser')
				basic_info 	= soup.find('div', class_='contact-info')
				basic_info_lines = basic_info.find_all('div', class_="rline")
				company_name_div 	= soup.find('div', class_="title")
				company_name_div 	= company_name_div.find('h1')
				error_loop = False
			except:
				error_loop_count += 1
				print("Connection blocked on page%s. Sleeping for 30 then resetting connection. Loop %i" % (id_string, error_loop_count))
				time.sleep(30)
			print(error_loop_count)