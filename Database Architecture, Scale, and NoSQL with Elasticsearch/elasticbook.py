from elasticsearch import Elasticsearch, RequestsHttpConnection
import os
import hashlib
import json
import time
import hidden

# Load the secrets
secrets = hidden.elastic()

# Elasticsearch setup
es = Elasticsearch(
    [secrets['host']],
    http_auth=(secrets['user'], secrets['pass']),
    url_prefix=secrets['prefix'],
    scheme=secrets['scheme'],
    port=secrets['port'],
    connection_class=RequestsHttpConnection,
)

# Set the index name to the Elasticsearch username
indexname = secrets['user']

# Delete the existing index (if any) and create a fresh one
mapping = {
    "mappings": {
        "properties": {
            "content": {"type": "text"},
            "offset": {"type": "integer"}
        }
    }
}

res = es.indices.delete(index=indexname, ignore=[400, 404])
print("Dropped index:", indexname)

res = es.indices.create(index=indexname, body=mapping)
print("Created index:", indexname)

# Prompt user for book file
bookfile = input("Enter book file (i.e. pg18866.txt): ").strip()
if not bookfile:
    raise Exception("Empty string detected. Please enter a valid book file.")

if not os.path.isfile(bookfile):
    raise FileNotFoundError(f"The file '{os.path.abspath(bookfile)}' does not exist. Please check the file name.")

# Process the book file and index paragraphs
with open(bookfile, "r", encoding="utf-8") as fhand:
    para = ''
    pcount = 0
    for line in fhand:
        line = line.strip()
        if not line and para:
            # New paragraph
            pcount += 1
            doc = {
                "offset": pcount,
                "content": para
            }
            print(f"Debug: Paragraph {pcount}: {para[:100]}...")  # Debugging line

            # Generate a unique ID for the document using SHA256
            pkey = hashlib.sha256(json.dumps(doc).encode()).hexdigest()
            es.index(index=indexname, id=pkey, body=doc)
            print(f"Indexed paragraph {pcount}: {pkey}")

            para = ''  # Reset paragraph
        else:
            para += ' ' + line

# Refresh the index
es.indices.refresh(index=indexname)
print(f"Index refreshed: {indexname}")
print(f"Debug: Paragraph {pcount}: {para}")
