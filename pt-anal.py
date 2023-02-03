import config # config.py for credentials
import requests
import time
import datetime
import chardet
import proxmoxer

print(datetime.datetime.now())

def send_to_telegram(message):
    apiURL = f'https://api.telegram.org/bot{config.apiToken}/sendMessage'
    print(message)
    try:
        response = requests.post(apiURL, json={'chat_id': config.chatID, 'text': message}) # Comment this for disable Telegram
        print(response.text)
    except Exception as e:
        print(e)

for web in config.web:
    while config.attempts:
        try:
            startTime = time.time()
            content = requests.get(web[1]).content
            endTime = time.time()
            speed = endTime - startTime
            detchar = chardet.detect(content)
            content = content.decode(detchar['encoding'])
            if content.find(web[2]) == -1:
                raise Exception(f'Keywords "{web[2]}" were not found on the page.') 
            #print(web[0], str(speed))
            ohshit = 'test'
            break
        except Exception as e:
            config.attempts -=1
            ohshit = f'The Website "{web[0]}" is Down.\n {web[1]}\n {e}'
            #print('try again')
    else:
        if ohshit:
            send_to_telegram(ohshit)
            ohshit = None



#proxmox = proxmoxer.ProxmoxAPI('', user='', password='', verify_ssl=False)
#print(proxmox.nodes.kickback.status.get())
#for node in proxmox.nodes.get():
#    status = proxmox.nodes(node['node']).status.get()
#    print(status['loadavg'])

