# ElasticTweet

ElasticTweet is a Python application that allows users to index and search tweets using Elasticsearch. This project demonstrates how to interact with Elasticsearch to store and retrieve tweet data efficiently.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- Index tweets from a text file into Elasticsearch.
- Each tweet is stored with an author name and timestamp.
- Drop existing indices before inserting new tweets to ensure data integrity.
- Simple command-line interface for user interaction.

## Requirements

- Python 3.x
- Elasticsearch (version 7.x or compatible)
- Required Python packages:
  - `elasticsearch`
  - `requests`

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/elasticTweet.git
   cd elasticTweet
   ```

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Elasticsearch:**
   - Ensure you have Elasticsearch running on your machine or server. You can download it from [Elasticsearch Downloads](https://www.elastic.co/downloads/elasticsearch).

4. **Configure credentials:**
   - Create a `hidden.py` file in the project directory with the following structure:
     ```python
     def elastic():
         return {
             'host': 'localhost',  # Elasticsearch host
             'user': 'your_username',  # Elasticsearch username
             'pass': 'your_password',  # Elasticsearch password
             'prefix': '',  # Optional URL prefix
             'scheme': 'http',  # or 'https'
             'port': 9200  # Default Elasticsearch port
         }
     ```

## Usage

1. **Run the application:**
   ```bash
   python elastictweet.py
   ```

2. **Input the tweets file:**
   - When prompted, enter the path to your text file containing tweets (one tweet per line).

3. **View results:**
   - The application will index the tweets and provide feedback on the number of tweets loaded.

## File Structure

- `elastictweet.py`: Main script for indexing tweets
- `hidden.py`: Contains Elasticsearch credentials
- `requirements.txt`: Python package dependencies
- `README.md`: Project documentation

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.