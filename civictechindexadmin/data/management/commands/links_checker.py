import requests
import urllib3

from django.core.management.base import BaseCommand

from ...models import Link

from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Command(BaseCommand):
    help = ("Test the response to all URLs in the Link table")
    
    def handle(self, **options):    
        broken_links = 0
        bad_links = 0
        links = 0
        
        timezone = datetime.now().astimezone().tzinfo
        #print(timezone)        
        now = datetime.now()
        print(now.strftime("%m/%d/%Y, %H:%M") + " - " + str(timezone))
        
        fd = open("links_checker.log", mode='w')
        
        fd.write('Link Checker run of ' + now.strftime("%m/%d/%Y, %H:%M") + " - " + str(timezone) + '\n')
        
        for url in Link.objects.all():
            #print('Link ', url.url)
            #print()
            
            links += 1
            
            try:
                response = requests.get(url.url, {'User-Agent': 'Mozilla/5.0'}, allow_redirects=False, verify=False)
                #print(response, url)
            except Exception as e:
                broken_links += 1
                #logger.error('broken_links.requests_exception', url=url, error=e)
                if url.http_status != "broken":
                    url.http_status = "broken"
                    url.http_status_date = now.today()
                    url.save()
                msg = 'broken link ' + str(url)
                print(msg)
                fd.write(msg+'\n')
                continue
            
            if response.status_code >= 300:
                bad_links += 1
                if url.http_status != str(response.status_code):
                    url.http_status = str(response.status_code)
                    url.http_status_date = now.today()
                    url.save()
                msg = 'status ' + str(response.status_code) + ' for ' + str(url)
                print(msg)
                fd.write(msg+'\n')
                
            #if(links >= 10):
                #break # to stop on testing/debugging
                
        print('========================================')
        print('Checked Links ', links)
        print('Bad (code >= 300) Links ', bad_links)
        print('Broken Links ', broken_links)

        fd.write('=======================================\n')
        fd.write('Checked Links ' + str(links) + '\n')
        fd.write('Bad (code >= 300) Links ' + str(bad_links) + '\n')
        fd.write('Broken Links ' + str(broken_links) + '\n')
    
        fd.close()
