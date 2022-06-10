import urllib
import requests
from bs4 import BeautifulSoup

def find_jobs(job_title,location):
    job_soup = load_indeed_jobs_div(job_title,location)
    jobs_list, num_listings = extract_job_information_indeed(job_soup)

    return jobs_list, num_listings

def load_indeed_jobs_div(job_title,location):
    getvars = {'q':job_title,'l':location, 'fromage':'last','sort':'date'}
    url = ('https://www.indeed.com/jobs?' + urllib.parse.urlencode(getvars))
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    job_soup = soup.find(id='mosaic-provider-jobcards')
    return job_soup

def extract_job_information_indeed(job_soup):
    job_elems = job_soup.find_all('div',class_='cardOutline')
    jobs_list = {'titles' : [], 'companies' : [], 'links' : [], 'dates' : []}

    for job_elem in job_elems:
        jobs_list['titles'].append(extract_job_title_indeed(job_elem))
        jobs_list['companies'].append(extract_company_indeed(job_elem))
        jobs_list['links'].append(extract_link_indeed(job_elem))
        jobs_list['dates'].append(extract_date_indeed(job_elem))

    num_listings = len(jobs_list['titles'])

    return jobs_list, num_listings

def extract_job_title_indeed(job_elem):
    title_elem = job_elem.find('h2',class_='jobTitle')
    title = title_elem.text.strip()
    if title[:3] == 'new' and title[:3].islower():
        title = title[3:]
    return title

def extract_company_indeed(job_elem):
    company_elem = job_elem.find('span',class_='companyName')
    company = company_elem.text.strip()
    return company

def extract_link_indeed(job_elem):
    link = job_elem.find('a',class_='jcs-JobTitle')['href']
    link = 'https://www.indeed.com' + link
    return link

def extract_date_indeed(job_elem):
    date_elem = job_elem.find('span',class_='date')
    date = date_elem.text.strip()
    return date

jobs, num_listings = find_jobs('python','San Francisco')
print(jobs['titles'])
print(num_listings)