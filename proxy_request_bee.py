

import requests

def proxy_request(target_url):
    response = requests.get(
        url='https://app.scrapingbee.com/api/v1/',
        params={
            'api_key': '5J7SL860TS4SODR1GB6WCVHHOWVMELQCIERZI1YJ8JQ776CD01SVFFXJ597W2FXV8DABZ0JKD2FXA2M3',
            'url': target_url, 
            'render_js': 'false', 
        },
        
    )
    print('Response HTTP Status Code: ', response.status_code)
    print('Response HTTP Response Body: ', response.content)
    return(response.text)