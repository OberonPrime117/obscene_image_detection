import os
import requests
import concurrent.futures

def download_image(url):
    try:
        response = requests.get(url, timeout=5)
        print(url)
        url_list = url.split("/")
        url_last = url_list[-1]
        url_last = url_last.replace(":","_")
        url_last = url_last.replace("-","_")
        url_last = url_last.replace(".","_")
        url_last = url_last.replace(";","_")
        url_last = url_last.replace("?","_")
        url_last = url_last.replace("=","_")
        url_last = url_last.replace("!","_")
        with open("data/"+str(url_last)+".jpg", 'wb') as f:
            f.write(response.content)
    except:
        print("error")
        pass


# Define the directory path
dir_path = 'raw_data'

# Initialize an empty list to store the file contents
file_contents = []

# Loop through all the files in the directory and its subdirectories
for root, dirs, files in os.walk(dir_path):
    for file in files:
        # Get the full path of the file
        file_path = os.path.join(root, file)
        # Open the file and read its contents
        print(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            contents = f.read()
            data = contents.split('\n')
            # Append the contents to the list
            file_contents.extend(data)


with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    futures = [executor.submit(download_image, url) for url in file_contents]
    concurrent.futures.wait(futures)

# http://i.imgur.com/e3P6L.jpg