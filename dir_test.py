import os 


path = "C:\\Users\\Sam\\Documents\\crosby_qcc_scrape"
company_jsons_subfolder_name = "company_jsons"
company_jsons_directory = (os.path.join(path, company_jsons_subfolder_name))
potential_files = os.listdir(company_jsons_directory)
finished_company_list = ['combined_company_json.txt', 'combined_company_json_2021_11_24_23_34_17.txt']
unadded_files = []
for company_file in potential_files:
	if company_file not in finished_company_list:
		unadded_files.append(company_file)
if len(unadded_files) > 0:
	target_json = unadded_files[0]
	print("Working on {}, there are {} unprocessed files remaining.".format(target_json, len(unadded_files)))
else:
	print("No remaining unprocessed files in directory. ")