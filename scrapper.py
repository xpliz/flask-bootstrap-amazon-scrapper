from bs4 import BeautifulSoup
from faker import Faker
from sqlite3 import Error

import requests
import random
import sqlite3

# Database functions
def db_connect():
	try:
		conn = sqlite3.connect('scrapper.db')
		create_table = """CREATE TABLE IF NOT EXISTS scrapper (
											ID INTEGER PRIMARY KEY AUTOINCREMENT,
											date DEFAULT CURRENT_TIMESTAMP,
											title TEXT,
											price TEXT,
											rating TEXT,
											reviews TEXT,
											availability TEXT,
											url TEXT NOT NULL
											);"""
		conn.execute(create_table)
		return conn
	except Error as e:
			print(e)
	return None

def insert_row(conn, title, price, rating, reviews, availability, url):
    conn.execute(
        "INSERT INTO scrapper (title, price, rating, reviews, availability, url) VALUES (?, ?, ?, ?, ?, ?);", (title, price, rating, reviews, availability, url))
    conn.commit()

def get_rows(conn):
    query = conn.execute("SELECT STRFTIME('%Y-%m-%d %H:%M', date) as date,title,price,rating,reviews,availability,url FROM scrapper WHERE title LIKE '%3080 Ti%' ORDER BY price ASC;")
    return query

# Function to extract Product Title
def get_title(soup):
	
	try:
		# Outer Tag Object
		title = soup.find("span", attrs={"id":'productTitle'})

		# Inner NavigatableString Object
		title_value = title.string

		# Title as a string value
		title_string = title_value.strip()

		# # Printing types of values for efficient understanding
		# print(type(title))
		# print(type(title_value))
		# print(type(title_string))
		# print()

	except AttributeError:
		title_string = ""	

	return title_string

# Function to extract Product Price
def get_price(soup):

	try:
		# price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()
		# price = soup.find("span", attrs={'class':'a-price-whole'}).string.strip()
		price = float(soup.find("span", attrs={'class':'priceToPay'}).find("span", attrs={'class':'a-offscreen'}).get_text().replace(',', '').replace('€', '').replace('.', '.').strip())
    
	except AttributeError:

		try:
			# If there is some deal price
			price = soup.find("span", attrs={'id':'priceblock_dealprice'}).string.strip()

		except:		
			price = ""	

	return price

# Function to extract Product Rating
def get_rating(soup):

	try:
		rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
		
	except AttributeError:
		
		try:
			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = ""	

	return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
	try:
		review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
		
	except AttributeError:
		review_count = ""	

	return review_count

# Function to extract Availability Status
def get_availability(soup):
	try:
		available = soup.find("div", attrs={'id':'availability'})
		available = available.find("span").string.strip()

	except AttributeError:
		available = "Not Available"	

	return available	

if __name__ == '__main__':

	# Headers for request
	HEADERS = ({'User-Agent':
	            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
	            'Accept-Language': 'en-US'})

	# fake = Faker() 
	# Faker.seed(fake.random_number()) 
	# fake_user_agent = fake.chrome() 
	# fake_user_agent = random.choice(list(open('ua.txt')))
	fake_user_agent = random.choice(open('ua.txt').readlines()).strip()
	
	HEADERS = ({'User-Agent': fake_user_agent, 'Accept-Language': 'en-US'})

	print(HEADERS)
	# The webpage URL
	# URL = "https://www.amazon.de/s?k=evga+nvidia+3080+ti"
	URL = "https://www.amazon.de/s?k=nvidia+3080+ti"
	URL_BASE = "https://www.amazon.de"
	
	# HTTP Request
	webpage = requests.get(URL, headers=HEADERS)

	# Soup Object containing all data
	soup = BeautifulSoup(webpage.content, "lxml")

	# Fetch links as List of Tag Objects
	links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

	# Store the links
	links_list = []

	# Loop for extracting links from Tag Objects
	for link in links:
		links_list.append(link.get('href'))


	# Loop for extracting product details from each link 
	# for link in links_list:

	# 	new_webpage = requests.get(URL_BASE + link, headers=HEADERS)

	# 	new_soup = BeautifulSoup(new_webpage.content, "lxml")
		
	# 	title = get_title(new_soup)
	# 	price = get_price(new_soup)
	# 	rating = get_rating(new_soup)
	# 	reviews = get_review_count(new_soup)
	# 	availability = get_availability(new_soup)


	# 	if (title != "") and (title != "Page 1 of 1") and (price != "") and (rating != "Previous page"):
	# 	# Function calls to display all necessary product information
	# 		print("Product Title =", title)
	# 		print("Product Price =", price)
	# 		print("Product Rating =", rating)
	# 		print("Number of Product Reviews =", reviews)
	# 		print("Availability =", availability)
	# 		print("URL =", URL_BASE + link)
	# 		print()
	# 		print()

	# 		conn = db_connect()
	# 		insert_row(conn, title, price, rating, reviews, availability, URL_BASE + link)

conn = db_connect()
rows = get_rows(conn)
print(rows)
for row in rows:
  print(row[0] + " " + row[1] + " " + row[2] + " " + row[3] + " " + row[4] + " " + row[5] + " " + row[6])