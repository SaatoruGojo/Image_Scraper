# Import necessary libraries
from flask import Flask, render_template, request, jsonify, redirect, url_for
from decouple import config
import os.path
import requests
from bs4 import BeautifulSoup
import pymongo
import logging as lg
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Configure logging settings
log_format = '%(asctime)s - %(levelname)s - %(message)s'
log_file = 'image_scrapping_log.log'
lg.basicConfig(filename=log_file, level=lg.INFO, format=log_format)

# Create a Flask web application
app = Flask(__name__)

# Get MongoDB connection string from environment variables
mongo_db_connection = config('MONGO_DB_CONNECTION')

# Define the homepage route
@app.route("/", methods=['GET'])
def homepage():
    return render_template("index.html")

# Define the image scraping route
@app.route("/scrapp", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            # Get user input and configure save directory
            query = request.form['content'].replace(' ', '')
            num_images = int(request.form['num_images'])
            save_dir = "images/"
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)

            # Configure user-agent header for scraping
            header = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/605.1.15 (KHTML, like Gecko)Version/12.1.1 Safari/605.1.15"
            }

            # Send a request to Google Images and parse the response
            response = requests.get(
                f"https://www.google.com/search?sca_esv=568527130&sxsrf=AM9HkKlsPD2WQggOna1LyYOt7LYoPCnOQA:1695740948785&q={query}&tbm=isch&source=lnms&sa=X&ved=2ahUKEwjBh4inx8iBAxW7XGwGHfRHDBUQ0pQJegQIDRAB&biw=1536&bih=796&dpr=1.25")
            soup = BeautifulSoup(response.content, 'html.parser')
            image_tags = soup.find_all("img")
            del image_tags[0]

            # Prepare data for MongoDB and download images
            img_data_mongo = []
            for index, i in enumerate(image_tags):
                if index >= num_images:
                    break
                image_url = i['src']
                image_data = requests.get(image_url).content
                myDict = {"Image": index, "image": image_data}
                img_data_mongo.append(myDict)
                with open(os.path.join(save_dir, f"{query}_{index}.jpg"), 'wb') as f:
                    f.write(image_data)

            # Connect to MongoDB and insert image data
            client = pymongo.MongoClient(mongo_db_connection)
            db = client['image_Scrap']
            result_coll = db['image_scrap_data']
            result_coll.insert_many(img_data_mongo)

            # Log successful image loading
            lg.info(f"Images loaded for query: {query}")

            return render_template('result.html')
        except Exception as e:
            # Log errors with traceback information
            lg.error(f"Error while processing query '{query}': {str(e)}", exc_info=True)
            return 'Something went wrong'
    else:
        return render_template("index.html")

# Run the Flask app
if __name__ == "__main__":
    # Use the PORT environment variable or default to 10000
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
