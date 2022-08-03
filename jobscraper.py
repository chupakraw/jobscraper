import gspread
import urllib
import requests
from datetime import date
from bs4 import BeautifulSoup

sa = gspread.service_account()
sh = sa.open('jobscraper')
wks = sh.worksheet('Sheet1')

jobs_list = []

def find_jobs(job_title,location):
    getvars = {'q':job_title,'l':location, 'sort':'date'}
    url = ('https://www.indeed.com/jobs?' + urllib.parse.urlencode(getvars))
    load_indeed_job_elems(url)

def load_indeed_job_elems(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    job_soup = soup.find('ul', class_='jobsearch-ResultsList')
    job_elems = job_soup.find_all('div',class_='cardOutline')
    extract_indeed_job_info(job_elems)
    check_pagination(soup)

def check_pagination(soup):
    next_url = soup.find('a',{'aria-label':'Next'})
    if next_url:
        url = 'https://www.indeed.com' + next_url['href']
        load_indeed_job_elems(url)

def extract_indeed_job_info(job_elems):
    for job_elem in job_elems:
        row = [date.today().strftime('%m/%d/%y'),
            extract_info(job_elem,'titles','h2','jobTitle'),
            extract_info(job_elem,'companies','span','companyName'),
            extract_info(job_elem,'links','a','jcs-JobTitle')]
        jobs_list.append(row)
    
def extract_info(job_elem,info_type,elem,class_name):
    if info_type != 'links':
        info_elem = job_elem.find(elem,class_=class_name)
        info = info_elem.text.strip()
        if info_type == 'titles' and info[:3] == 'new' and info[:3].islower():
            info = info[3:]
    else:
        info_elem = job_elem.find(elem,class_=class_name)['href']
        info = 'https://www.indeed.com' + info_elem
    return info

find_jobs('python','San Francisco')
num_listings = len(jobs_list)
print(num_listings)
wks.append_rows(jobs_list)