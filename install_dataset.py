import urllib.request
import zipfile
import os

# Set the URL of the zip file to be downloaded
url = "https://github.com/kshitijsriv/csm-gtfs-workshop/raw/master/GTFS.zip?raw=true"

# Set the name of the zip file to be downloaded
filename = "GTFS.zip"

if os.path.exists("GTFS.zip"):
    os.remove(filename)


# Download the zip file from the URL
print("Downloading Dataset...")
urllib.request.urlretrieve(url, filename)
print("Dataset downloaded")

# Extract the contents of the zip file to the current directory
with zipfile.ZipFile(filename, 'r') as zip_ref:
    zip_ref.extractall(os.getcwd()+'/GTFS/')

print("Extecting zip file")

# Remove the zip file after extraction
os.remove(filename)
