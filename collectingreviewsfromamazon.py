import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import os

def get_response(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

#page_content = get_response(url)

fetched_reviews = []

# This code works for Amazon India..
def get_review_link(url):
    page_content = get_response(url)
    link = page_content.find('a', {"data-hook" : "see-all-reviews-link-foot"}).get('href')
    address = url[:url.find('.in')+3]
    review_page_link = address + link
    return review_page_link

#"https://p-nt-www-amazon-in-kalias.amazon.in/Xiaomi-Storage-Snapdragon-Flagship-Cameras/product-reviews/B09XBCCQJT/ref=cm_cr_arp_d_paging_btm_next_2?reviewerType=all_reviews&pageNumber=2"

#"https://p-nt-www-amazon-in-kalias.amazon.in/Xiaomi-Storage-Snapdragon-Flagship-Cameras/product-reviews/B09XBCCQJT?reviewerType=all_reviews"

# Navigating through the pages..
#print(get_review_link(url) + "&pageNumber=" + str(2))

def get_rating(review):
    rating = review.find('span', class_ = "a-icon-alt").text
    rating = rating.split("out")[0].strip()
    rating = float(rating)
    return rating

def get_star(rating):
    rating = int(rating)
    star = "⭐" * rating
    return star

def get_variant(product, review):
    variant = review.find('a', {'data-hook': 'format-strip'})
    # Filtering the 'None' type data..
    try:
        if variant != None:
            variant = variant.text
        elif variant == None:
            variant = product + " (Unavailable, Generated_from_Title)"
    except:
        variant = "Unavaliable"
    return variant

def get_vote(review):
    vote = review.find('span', class_ = "a-size-base a-color-tertiary cr-vote-text")
    if vote != None:
        vote = vote.text
    else:
        vote = "None"
    return vote

def get_review_images(review):
    img_links = []
    raw_img_links = []
    if review.find('div', class_ = "review-image-tile-section") == None:
        img_links.append("Not Available")
    else:
        raw_img_links = review.find_all('img', {'alt' : "Customer image"})
    for individual_links in raw_img_links:
        media_link = individual_links.get('src')
        if media_link != None:
            img_links.append(media_link)
    return ', '.join(img_links)

def save_to_csv(product, fetched_reviews):
    page_visit_details = datetime.now().strftime("%B %d %Y, %H-%M-%S")
    # Applying this filter because the file cannot be saved into the system with these special characters in file name..
    replace_characters = [':', '\\', '|', '/', '*', '?', '"', '<', '>']
    for char in replace_characters:
        if char in product:
            product = product.replace(char, "")
    # Too long name seems to be an issue while adding these files in github so set the limit of the filename to 60 characters..
    product = product[0:60]
    file_path = str(product) + '(Product Page, Visited on ' + str(page_visit_details) + ').csv'
    # write the information to a CSV file..
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Customer Name', 'Variant', 'Rating(Out of 5)', 'Rating', 'Date of Review', 'Comment', 'Review', 'Images attatched by Customer', 'Votes on the Review'])
        csv_writer.writerows(fetched_reviews)
    
    # Get the absolute path of the file
    absolute_path = os.path.abspath(file_path)
    # Print the absolute path
    print("\n\n___________________________________________________________________________________________________________________________________")
    print("-----------------------------------------------------------------------------------------------------------------------------------\n\n")
    print(f'The absolute path of the CSV file is: {absolute_path}\nVisited on {page_visit_details}')

def save_to_json():
    pass

# Getting information from the individual pages..
def scrape(soup):               # Replaced 'url' with 'soup'..
    #soup = get_response(url)
    product = soup.find('a', class_ = "a-link-normal").text.strip()
    print("\t\t\tP R O D U C T     :   ", product)
    print("---------->   LENGTH  :  ", len(soup.find_all('div', {'data-hook': "review"})))
    for review in soup.find_all('div', {'data-hook': "review"}):
        customer_name = review.find('span', class_ = "a-profile-name").text
        rating = get_rating(review)
        date = review.find('span', class_ = "a-size-base a-color-secondary review-date").text
        comment = review.find('a', class_ = "a-size-base a-link-normal review-title a-color-base review-title-content a-text-bold").text.strip()
        body = review.find('span', class_ = "a-size-base review-text review-text-content").text.strip()
        variant = get_variant(product, review)
        vote = get_vote(review)
        img_links = get_review_images(review)

        fetched_reviews.append([customer_name, variant, rating, get_star(rating), date, comment, body, img_links, vote])

        # Printing the details..
        print("\n\n\n\nNAME      :   ", customer_name)
        print("VARIANT   :   ", variant)
        print("RATING    :   ", rating)
        print("DATE      :   ", date.encode("utf-8"))       # '.encode("utf-8")' is required only in Visual Studio Code or CMD, not required if used in Colab..
        print("COMMENT   :   ", comment.encode("utf-8"))    # '.encode("utf-8")' is required only in Visual Studio Code or CMD, not required if used in Colab..
        print("BODY      :   ", body.encode("utf-8"))       # '.encode("utf-8")' is required only in Visual Studio Code or CMD, not required if used in Colab..
        print("IMAGES    :   ", img_links)
        print("VOTE      :   ", vote)
      
    return product

def get_no_of_reviews(content):
    no = content.find('div', class_ = "a-row a-spacing-base a-size-base").text.strip()
    no = no.split(", ")[-1]
    no = int(no.split(" with")[0])
    return no

def get_data(url):
    review_page = get_review_link(url) + "&pageNumber="
    scraping_completed = False
    n = 1
    #s_no = 0
    no_of_reviews = 0
    while scraping_completed == False:
        #print("S. No.     :   ", s_no + 1)
        print("\n\n\tCurrently on Page : ", n)
        content = get_response(review_page + str(n))
        product = scrape(content)
        n = n + 1
        no_of_reviews = get_no_of_reviews(content)
        #no_of_reviews = no_of_reviews + 1
        # For now scraping only first 10 pages..
        if no_of_reviews == 0:
            scraping_completed = True

    print("\n\n\tScraping completed, writing into a file..")
    save_to_csv(product, fetched_reviews)

url = "https://p-nt-www-amazon-in-kalias.amazon.in/Xiaomi-Storage-Snapdragon-Flagship-Cameras/dp/B09XBCCQJT/ref=cm_cr_arp_d_product_top?ie=UTF8&th=1"

get_data(url)