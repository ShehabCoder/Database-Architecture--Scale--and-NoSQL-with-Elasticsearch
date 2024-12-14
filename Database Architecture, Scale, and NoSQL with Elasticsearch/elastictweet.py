from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection
import os
import uuid
import time

import hidden  # Make sure this module provides the correct credentials.

# Fetch Elasticsearch credentials
secrets = hidden.elastic()

# Set up the Elasticsearch connection
es = Elasticsearch(
    [secrets['host']],
    http_auth=(secrets['user'], secrets['pass']),
    url_prefix=secrets['prefix'],
    scheme=secrets['scheme'],
    port=secrets['port'],
    connection_class=RequestsHttpConnection,
)

# Set index name to the user's name
indexname = secrets['user']

# Load the tweets from the specified text file
tweets_file = input("Enter the tweets file (i.e. tweets.txt): ")
print(f"Debug: User entered tweets file: '{tweets_file}'")  # Debugging line

if tweets_file.strip() == '':
    raise Exception("empty string detected, please try again to enter a tweets file")

# Check if the tweets file exists
if not os.path.isfile(tweets_file):
    raise FileNotFoundError(f"The file '{os.path.abspath(tweets_file)}' does not exist. Please check the file name and try again.")

# Drop the existing index if it exists
res = es.indices.delete(index=indexname, ignore=[400, 404])
print("Dropped index", indexname)
print(res)

# Create a new index
res = es.indices.create(index=indexname)
print("Created the index...")
print(res)

# Open the tweets file
with open(tweets_file, 'r', encoding='utf-8') as fhand:
    # Initialize variables for reading the tweets
    tweet_count = 0

    # Read the tweets line by line
    for line in fhand:
        tweet = line.strip()
        if tweet:  # Only process non-empty lines
            tweet_count += 1
            doc = {
                'author': 'kimchycd',
                  "type": "tweet",  # Replace with actual author name if needed
                'text': tweet,  # Store the tweet in the document
                'timestamp': datetime.now().isoformat()  # Use current date and time
            }

            # Use a GUID for the primary key
            pkey = str(uuid.uuid4())

            # Index the document
            res = es.index(index=indexname, id=pkey, body=doc)
            print('Added document', pkey)

            # Print progress every 100 tweets
            if tweet_count % 100 == 0:
                print(tweet_count, 'tweets loaded...')
                time.sleep(1)

    # Refresh the index to make sure all documents are searchable
    res = es.indices.refresh(index=indexname)
    print("Index refreshed", indexname)
    print(res)

print(' ')
print('Loaded', tweet_count, 'tweets')
