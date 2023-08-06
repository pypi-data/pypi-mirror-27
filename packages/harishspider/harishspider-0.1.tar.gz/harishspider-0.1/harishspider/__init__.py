from bs4 import BeautifulSoup
import re
import requests
import random
import urllib.request


def emails(urlstr):
	url=urlstr
	if(url.startswith("http://") or url.startswith("https://")):
		proc=[]
		mail=[]
		proxies = {"https":"https://r170146:sailakshmi@10.20.3.3:3128","http":"http://r170146:sailakshmi@10.20.3.3:3128"}

		try:
			response=requests.get(url,proxies=proxies)
			soup=BeautifulSoup(response.text,'html.parser')
			links = [a.attrs.get('href') for a in soup.select('a[href]') ]
			for i in links:
				if(("contact" in i or "Contact")or("Career" in i or "career" in i))or('about' in i or "About" in i)or('Services' in i or 'services' in i):
					proc.append(i)
			proc=set(proc)
			for j in proc:
				if(j.startswith("http") or j.startswith("www")):
					r=requests.get(j)
					data=r.text
					soup=BeautifulSoup(data,'html.parser')
					for name in soup.find_all('a'):
						k=name.text
						a=bool(re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',k))
						if('dot' in k and 'at' in k)or ('@' in k and a==True):
							k=k.replace(" ",'').replace('\r','')
							k=k.replace('\n','').replace('\t','')
							if(len(mail)==0)or(k not in mail):
								print(k)
							mail.append(k)
				else:
					newurl=url+j
					r=requests.get(newurl,proxies=proxies)
					data=r.text
					soup=BeautifulSoup(data,'html.parser')
					for name in soup.find_all('a'):
						k=name.text
						a=bool(re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',k))
						if('dot' in k and 'at' in k)or ('@' in k and a==True):
							k=k.replace(" ",'').replace('\r','')
							k=k.replace('\n','').replace('\t','')
							if(len(mail)==0)or(k not in mail):
								print(k)
							mail.append(k)
			mail=set(mail)
			if(len(mail)==0):
				print("NO MAILS FOUND")
		except Exception as e:
			return(e)
	else:
		return("Incorrect URL !! ")