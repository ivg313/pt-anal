import config # config.py for credentials
import requests
import time
import datetime
import chardet

print(datetime.datetime.now())

def send_to_telegram(message):
    apiURL = f'https://api.telegram.org/bot{config.apiToken}/sendMessage'
    print(message)
    try:
        response = requests.post(apiURL, json={'chat_id': config.chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

for web in config.web:
    try:
        startTime = time.time()
        content = requests.get(web[1]).content
        endTime = time.time()
        speed = endTime - startTime
        detchar = chardet.detect(content)
        content = content.decode(detchar['encoding'])
        if content.find(web[2]) == -1:
            raise Exception(f'Keywords "{web[2]}" were not found on the page.') 
       # print(web[0], str(speed))
    except Exception as e:
        ohshit = f'The Website "{web[0]}" is Down.\n {web[1]}\n {e}'
        send_to_telegram(ohshit)
        print(ohshit)

