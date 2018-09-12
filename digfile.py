# library imports
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent
ua = UserAgent()

# List to store Links from google search page
sites = []
movies = [] #List to store link of movies
googleallpages = [] # List to store next 9 pages of google search

headers = {'User-Agent': ua.random}

#Initializing variables with blank
soup = ' '
ext = ' '

#File valid extensions (file links should end with these extensions)
ext1 = ('mkv','mov','avi','mp4','mpg','wmv')
ext2 = ('mp3','wav','ac3','ogg','flac','wma','m4a')
ext3 = ('MOBI','PDF','RTF','DOC','DOCX')
ext4 = ('exe','iso','tar','rar','zip','apk')
ext5 = ('jpg','png','bmp','gif','tif','tiff','psd')
ext6 = ' '

#Function to make URL from search term and file extensions.
def makeURL(name,filetype):
	# URL Prefix
	urlPref = "https://www.google.com/search?q="
	# URL mid part
	urlMid = "%20%2B("
	#File extentions to be searched (concatenating file type presets to url form)
	FileExt = '%7C'.join(filetype)
	#URL Suffix
	urlSuff = ")%20-inurl%3A(jsp%7Cpl%7Cphp%7Chtml%7Caspx%7Chtm%7Ccf%7Cshtml)%20intitle%3Aindex.of%20-inurl%3A(listen77%7Cmp3raid%7Cmp3toss%7Cmp3drug%7Cindex_of%7Cwallywashis)"
	# complete URL of first search page
	url1 = urlPref + name + urlMid + FileExt + urlSuff
	return url1


#Function to find and append the websites on a google search page into sites[] list
def getResLinks(url):
	# Get URL page data
	page = requests.get(url, headers=headers)
	# Get page data parsed as HTML
	global soup
	soup = BeautifulSoup(page.text, "html.parser")
	#Scraping google searchpage links
	links = soup.findAll("cite")
	print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~ WEB FOLDER LINKS ~~~~~~~~~~~~~~~~~~~~~~~~")
	for getL in links:
		hrefs = getL.get_text()
		sites.append(hrefs)
		print(hrefs)

#function to find next 9 search pages of google and store them in googleallpages[] list
def googlekpages():
	flclasslinks = []
	nextpage = soup.find_all("a",class_="fl")
	for pages in nextpage:
		pg = (pages['href'])
		pg = 'http://google.com' + pg
		if "&start=" not in pg :
			continue
		else :
			flclasslinks.append(pg)
	global googleallpages
	googleallpages = flclasslinks

#Function to check whether the Search term is present in final file link. It'll return 1 if matches else skip the link.
def match(filekalink, searchterm):
	delimiters = {'%20','%5','_','.','-','/',':','%','(',')','{','}','[',']'}
	filekalink = filekalink.lower()
	searchterm = searchterm.lower()
	for delimiter in delimiters:
		filekalink = filekalink.replace(delimiter,' ')
	filekalink = filekalink.split(' ')
	if set(searchterm.split(' ')).issubset(filekalink) :
		return 1

#Function to get the link of file from websites in sites[] list. 
def getMovielink(websites):
	print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~ FILE LINKS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	for site in websites:
		if ((site.startswith("https://")) or (site.startswith("http://"))):
			fullsitelink = site
		else :
			fullsitelink = "http://" + site
		try :
			innersite = requests.get(fullsitelink, headers=headers)
			innersoup = BeautifulSoup(innersite.text, "html.parser")
			alllinks = innersoup.findAll("a")
			for movielink in alllinks:
				movie = (movielink['href'])
				milgaya = fullsitelink + movie
				if milgaya.endswith(ext) :
					if match(milgaya, name) == 1:
						print(milgaya)
		except :
			continue


#Name of file to be searched - Search Term
name = input("Enter file name : ")
contenttype = input("\nEnter its type -\nPress : \n |- 1. Video, Movies, Clips, TV Shows, Documentaries \n |- 2. Music, Songs, Audio \n |- 3. E-books, PDFs, Document, Spreadsheets, Presentations \n |- 4. Softwares, Applications, Zip Folders, ISOs \n |- 5. Images, Photos, Albums, Graphics, GIFs, PSDs \n |- 6. Custom file type \n")
if contenttype == '1':
	ext = ext1
elif contenttype == '2':
	ext = ext2
elif contenttype == '3':
	ext = ext3
elif contenttype == '4':
	ext = ext4
elif contenttype == '5':
	ext = ext5
elif contenttype == '6':
	ext6 = input("\nEnter file extensions seperated by comma(,) -                 			For ex: txt,jpg,mp3\n\t")
	ext6 = ext6.replace(',',' ')
	ext6 = ext6.split(' ')
	ext6 = tuple(ext6)
	ext = ext6

url = makeURL(name,ext)
getResLinks(url)
getMovielink(sites)

ask = input("Want more links? (Y/N)\n").upper()
if ask == 'Y':
	googlekpages()
	print(googleallpages)
	for page in googleallpages:
		getResLinks(page)
	for onesite in sites:
		getMovielink(sites)



