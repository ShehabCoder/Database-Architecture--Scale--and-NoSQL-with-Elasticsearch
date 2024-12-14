import requests

def download_file(url, filename):
    """
    Download a file from the given URL and save it to the specified filename.

    Parameters:
        url (str): The URL of the file to download.
        filename (str): The name of the file to save.
    """
    try:
        print(f"Starting download from {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"File downloaded successfully and saved as '{filename}'")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")

# Example Usage
if __name__ == "__main__":
    # URL of the book to download
    url = "https://www.gutenberg.org/files/2591/2591-0.txt"
    # Desired filename
    filename = "pg2591.txt"
    download_file(url, filename)
