import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


base_url = 'https://hprera.nic.in/PublicDashboard'


response = requests.get(base_url, verify=False)
soup = BeautifulSoup(response.text, 'html.parser')


project_links = soup.select('a[href^="/Public/ReraProjectDetails"]')[:6]

project_details = []

for link in project_links:
    project_url = 'https://hprera.nic.in' + link['href']
    project_response = requests.get(project_url, verify=False)
    project_soup = BeautifulSoup(project_response.text, 'html.parser')
    
    try:
        gstin = project_soup.find('span', text='GSTIN No').find_next('span').text.strip()
        pan = project_soup.find('span', text='PAN No').find_next('span').text.strip()
        name = project_soup.find('span', text='Name').find_next('span').text.strip()
        address = project_soup.find('span', text='Permanent Address').find_next('span').text.strip()
        
        project_details.append({
            'GSTIN No': gstin,
            'PAN No': pan,
            'Name': name,
            'Permanent Address': address
        })
    except AttributeError:
        print(f"Some details are missing for project at {project_url}")


df = pd.DataFrame(project_details)


df.to_csv('registered_projects.csv', index=False)

print("Scraping completed! Data saved to 'registered_projects.csv'")
