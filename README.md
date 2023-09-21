
# Flask Movie Database

A simple web application built with Flask that allows users to query a movie database and retrieve information about movies.

##Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

##Features

- Look up information about movies, such as title, rating, genre, year, and more.
- Find the top-rated movie in the database.
- Get a random movie recommendation.
- List movie genres available in the dataset.
- Search for movies directed by a specific director.
- Filter movies by genre, rating, release year, and other criteria.
- Clear conversation history.

##Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x: Make sure you have Python 3.x installed on your system.
- [Flask](https://flask.palletsprojects.com/en/2.1.x/): This project uses Flask, so you need to have it installed. You can install it using pip:

  ```bash
  pip install Flask
  ```

- [Pandas](https://pandas.pydata.org/): Pandas is used for data manipulation. Install it with pip:

  ```bash
  pip install pandas
  ```

- [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy): FuzzyWuzzy is used for fuzzy text matching. Install it with pip:

  ```bash
  pip install fuzzywuzzy
  ```

##Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/flask-movie-database.git
   ```

2. Change the working directory:

   ```bash
   cd flask-movie-database
   ```

3. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   On Windows:

   ```bash
   venv\Scripts\activate
   ```

   On macOS and Linux:

   ```bash
   source venv/bin/activate
   ```

5. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

##Usage

1. Start the Flask application:

   ```bash
   python app.py
   ```

2. Open a web browser and go to `http://localhost:5000` to access the application.

3. You can interact with the chatbot by typing queries in the input box and pressing Enter.

4. The chatbot can answer various queries about movies, including searching by title, director, genre, rating, and more.

5. To exit the chat, type "quit."

6. You can clear the chat history by clicking the "Clear Chat" button.

##Contributing

Contributions are welcome! If you have any improvements or suggestions, please open an issue or create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
