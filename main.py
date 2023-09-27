from flask import Flask,render_template,request,jsonify,redirect,url_for
from flask_cors import CORS,cross_origin
import pymongo
import os.path
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq
import logging as lg

# Configure the logging format
log_format = '%(asctime)s - %(levelname)s - %(message)s'
log_file = 'image_scrapping_log.log'
lg.basicConfig(filename=log_file, level=lg.INFO, format=log_format)

app = Flask(__name__)

@app.route("/", methods=['GET'])
def homepage():
    return render_template("index.html")

@app.route("/scrapp", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            query = request.form['content'].replace(' ', '')
            save_dir = "images/"
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)
            header = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15"
            }
            response = requests.get(
                f"https://www.google.com/search?sca_esv=568527130&sxsrf=AM9HkKlsPD2WQggOna1LyYOt7LYoPCnOQA:1695740948785&q={query}&tbm=isch&source=lnms&sa=X&ved=2ahUKEwjBh4inx8iBAxW7XGwGHfRHDBUQ0pQJegQIDRAB&biw=1536&bih=796&dpr=1.25")
            soup = BeautifulSoup(response.content, 'html.parser')
            image_tags = soup.find_all("img")
            del image_tags[0]
            img_data_mongo = []
            for i in image_tags:
                image_url = i['src']
                image_data = requests.get(image_url).content
                myDict = {"index": image_url, "image": image_data}
                img_data_mongo.append(myDict)
                with open(os.path.join(save_dir, f"{query}_{image_tags.index(i)}.jpg"), 'wb') as f:
                    f.write(image_data)

            # Log successful image loading
            lg.info(f"Images loaded for query: {query}")
            return render_template('result.html')
        except Exception as e:
            # Log errors with traceback information
            lg.error(f"Error while processing query '{query}': {str(e)}", exc_info=True)
            return 'Something went wrong'

    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8000')





# client = pass
# db=client['image_scrap']
# coll_img= db['image_scrap']
# coll_img.insert_many(img_data_mongo)

