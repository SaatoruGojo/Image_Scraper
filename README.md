# Image Scraping Web Application

This is a web application that allows users to scrape images from Google Images based on a search query and store them in a MongoDB database. The application is built using Flask and provides a user-friendly interface for image scraping.

## Features

1. **Homepage**: The application provides a simple homepage where users can enter their search query and specify the number of images they want to scrape.

2. **Image Scraping**: Users can submit their query, and the application will send a request to Google Images to fetch the images related to the query. It scrapes the specified number of images and saves them in a local directory.

3. **MongoDB Integration**: The scraped images are stored in a MongoDB database. Each image is associated with an index and the image data itself. MongoDB is used for efficient storage and retrieval of image data.

4. **Logging**: The application logs important events, such as successful image loading and any errors encountered during the scraping process. This helps in monitoring and troubleshooting.

## Usage

1. Clone the repository to your local machine.
2. Make sure you have Python and the required libraries installed.
3. Create a `.env` file and add your MongoDB connection string as `MONGO_DB_CONNECTION`.
4. Run the `main.py` file to start the Flask web application.
5. Access the application in your web browser and follow the on-screen instructions to scrape images.

## Technologies Used

- Flask: Python web framework for building the web application.
- Requests: Library for making HTTP requests to fetch Google Images.
- BeautifulSoup: Library for parsing HTML content.
- MongoDB: NoSQL database for storing scraped image data.
- Decouple: Library for managing environment variables.
- Logging: Python built-in module for logging events and errors.
- dotenv: Library for loading environment variables from a `.env` file.
