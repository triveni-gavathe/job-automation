import requests
from bs4 import Beutifulsoup
from django.conf import settings

HEADERS={
    'user-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/120.0.0.0 Safari/537.36'
}

#fallback jobs
def get_fallback_jobs(role,location):
    return[
        {
            'title':f'junior {role}',
            'company':'TechCrop INdia',
            'location':location,
            'link':'https://internshala.com/jobs',
            'source':'Fallback'
        },
        {
            'title':f'{role} intern',
            'company':'Digigtal solution',
            'location':location,
            'link':'https://internshala.com/jobs',
            'source':'Fallback'
        },
        {
            'title':f'{role} Fresher',
            'company':'starup HUb',
            'location':location,
            'link':'https://internshala.com/jobs',
            'source':'Fallback'
        }       
    ]
# jserch api  its uesd for the fetch form thejob linkdin and 500 request per month and its free plan i used 
def fetch_jsearch(role,location):
    jobs=[]
    try:
        api_key=getattr(settings,'RAPID_API_KEY',None)
        if not api_key:
            print('jsearch :no api key found')
            return[]
        url="https://jsearch.p.rapidapi.com/search" 
        heaers={
            "X-RapidAPI-Key":api_key,
            "X-RapidAPI-Host":"Jsearch.p.rapidapi.com"
        }
        params={
            "query":f"{role} in {location} india ",
            "page":"1",
            "num_pages":"1"
            
        }
        response=requests.get(
            url,headers=heaers,
            params=params,timeout=10
        )
        if response.status_code!=200:
            print(f"jsearch api error :{response.status_code}")
            return[]
        data=response.json()
        print(data)
        for job in data.get('data',[])[:10]:
            jobs.append({
                'title':job.get('job_title','N/A'),
              'company':job.get('employer_name','N/A'),
              'location':job.get('job_city',location),
              'link':job.get('job_apply_link','#'),
              'source':'Linkedin/Indeed',
                             
            
            })
            
            print(f"jsearch:found{len(jobs)} jobs")
    except Exception as e:
        print(f"JSEARCH FAILED:{e}")
    return jobs



#----------intershala Scraper-----------
def fetch_intershala(role,location):
    jobs=[]
    try:
        role_slug=role.strip().lower().replace(' ','-')
        location_slug=location.strip().lower().replace(' ','-')
        url=(
            f"https://internshala.com/jobs/"
            f"{role_slug}--jobs-in{location_slug}"
            
        )
        response=requests.get(url,headers=HEADERS,timeout=10)
        if requests.status_codes !=200:
            return[]             
        soup=Beutifulsoup(response.text,'html.parser')
        listings=soup.find_all(
            'div',class_='individual_intership',limit=10
        )
        for job in listings:
            try:
                title=job.find('h3').text.strip()
                company=job.find('h4').text.strip()
                loc=job.find(
                    'p',class_= 'location'
                ).text_strip()
                link_tag=job.find('a',class_='view_Detail_button')
                link=(
                    'https://internshala.com'+link_tag['href']
                    if link_tag else '#'
                     
                )
                #which information we faced save int he jobs list
                jobs.append({
                    'title':title,
                    'company':company,
                    'location':loc,
                    'link':link,
                    'source':'intershala'
                    
                })
            except:
                continue
        print(f"intrnshala:found{len(jobs)}jobs")    
    except Exception as e:
        print(f"internshala failed:{e}")            
        
    return jobs      

#-----naukri--------------
def fetch_naukri(role,location):
    jobs=[]
    try:
        role_slug=role.strip().lower().replace(' ','-')
        location_slug=location.strip().lower().replace(' ','-')
        url=(
            f"https://www.naukri.com/"
            f"{role_slug}-jobs-in-{location_slug}"
            
        )
        response=requests.get(url,headers=HEADERS,timeout=10)
        soup=Beutifulsoup(response.text,'html.parser')
        listings=soup.find_all(
            'article',class_='jobTuple',limit=10
            
        )
        for job in listings:
            try:
                title=job.find('a',class_='title').text.strip()
                company=job.find(
                    'a',class_='subTitle'
                    
                ).text.strip()
                loc=job.find(
                    'li',class_='location'
                    
                ).text.strip()
                link=job.find('a',class_='title')['href']
                jobs.append({
                    'title':title,
                    'company':company,
                    'location':location,
                    'link':link,
                    'source':'naukri'
                })
            except:
                continue
            print(f"naukri found{len(jobs)} jobs")  #retnr the result how many the job found
    except Exception as e:
        print(f"naukri faield:{e}")
    return jobs

#----------main search woth fallback------------
def search_jobs(role,location):
    all_jobs=[]
    print("tryin the jearch api.......")
    all_jobs+=fetch_jsearch(role,location)
    print("tryin the intershala api.......")
    all_jobs+=fetch_intershala(role,location)    
    print("tryin the Naukri api.......")
    all_jobs+=fetch_naukri(role,location)   
    if not all_jobs:
        print("ALL source failed-using fallback") 
        all_jobs=get_fallback_jobs(role,location)
    print(f"Total:{len(all_jobs)}jobs")   
    return all_jobs
 
            