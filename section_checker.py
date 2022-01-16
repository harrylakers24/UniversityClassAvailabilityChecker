import urllib.request as urllib2
import requests
from bs4 import BeautifulSoup
import re

opener = urllib2.build_opener()
opener.addheaders = [('user-agent', 'Mozilla/5.0')]


def find_avail(url):
	url = "https://courses.students.ubc.ca" + url

	#opens and reads url
	singleResult = opener.open(url).read()

	singleSoup = BeautifulSoup(singleResult, 'lxml')

	#looks for text indicating indicating different designations making a section unavailable
	sectionFull = singleSoup.find(text="Note: this section is full")
	sectionBlocked = singleSoup.find(text="Note: this section is blocked from registration. Check the comments for details or contact the department for further details.")
	sectionRestricted = singleSoup.find(text="Note: this section is restricted")
	sectionSTT = singleSoup.find(text="Note: The remaining seats in this section are only available through a Standard Timetable (STT)")

	#if all designations are None, then the section is available
	return (sectionFull == None and sectionBlocked == None and sectionRestricted == None and sectionSTT == None)

def get_url_urls(url):
	#gets contents from url
	result = requests.get(url)
	src = result.content

	soup = BeautifulSoup(src, 'lxml')

	urls = []
	#skips first and last elements as they are default None 
	for tr_tag in soup.find_all("tr")[1:-2]:
		#finds a tags with link
		a_tag = tr_tag.find('a', href=True)
		#adds url to list
		urls.append(a_tag['href'])

	return urls

def check_all_sections(urls):
	for url in urls:
		if find_avail(url):
			return True

	return False

def get_course_section_name(url):
	url = "https://courses.students.ubc.ca" + url
	#gets contents from url
	result = requests.get(url)
	src = result.content

	soup = BeautifulSoup(src, 'lxml')

	#section name is always in h4 tag
	text = soup.find("h4").text.strip()

	return text

def find_course_sections(urls):
	sections = []
	for url in urls:
		sections.append(get_course_section_name(url))

	return sections

def get_course_sections(dept: str, course: str):
	url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept=" + dept + "&course=" + course
	return find_course_sections(get_url_urls(url))

def get_course_avail(dept: str, course: str):
	url = "https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept=" + dept + "&course=" + course
	return check_all_sections(get_url_urls(url))

print(get_course_sections("MATH", "316"))

print(get_course_avail("MATH", "316"))
