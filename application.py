import requests
import urllib
from flask import Flask, render_template, request,jsonify
from flask_cors import CORS,cross_origin
from bs4 import BeautifulSoup
#from urllib.request import urlopen as uReq
import logging
import pymongo
import csv
logging.basicConfig(filename='rev.logs',level=logging.INFO)
application=Flask(__name__)

@application.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@application.route('/product_review',methods=['POST','GET'])
def product():
    if request.method == 'POST':
                try:
                    query= request.form['content'].replace(' ','')  
                    url=f"https://www.flipkart.com/search?q={query}"
                    response= requests.get(url)
                    if response.status_code==200:
                        soup = BeautifulSoup(response.text,'html.parser')
                        product_links=[]
                        product_elements = soup.find_all("a", class_="_1fQZEK")
                        for product_element in product_elements:
                            product_links.append("https://www.flipkart.com"+product_element.get('href'))
                                
                        product_details=[]
                        for link in product_links:
                            res=requests.get(link)
                            if res.status_code==200:
                                detail_soup=BeautifulSoup(res.text,'html.parser')
                                product_name= detail_soup.find('span',class_='B_NuCI').text.strip()
                                Total_rating = detail_soup.find('div', class_='_2d4LTz').text.strip()
                                price = detail_soup.find('div', class_='_30jeq3 _16Jk6d').text.strip()
                                Highlights = detail_soup.find('div', class_='_2418kt').text.strip()
                                product_details.append([product_name,
                                   Total_rating,
                                  price,
                                   Highlights])          
                        csv_filename=f"{query}_product_details.csv"
                        with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
                            writer = csv.writer(csv_file)
                            writer.writerow(["Product Name", "Total Rating", "Price", "Highlights"])
                            writer.writerows(product_details)
                        return f"Product details saved to {csv_filename}"

                    else:
                        return 'Failed to fetch Flipkart search results'
                except Exception as e:
                    logging.info(e)
                    return 'Something went wrong'

    else:
        return render_template('index.html')

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8000)    
                                    
                                
                                
                                
                                

                                
                                
                                
                                                 
                                                 