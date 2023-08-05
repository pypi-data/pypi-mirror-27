# Microsoft Cognitive Services API for Machine Learning
This is a thin python wrapper for Microsoft's Microsoft Cognitive Services API focused on collecting image training data for use in machine learning. I have based this library off of another repoisitory created by __[tristantao](https://github.com/tristantao)__ called __[py-ms-cognitive](https://github.com/tristantao/py-ms-cognitive)__.

Introduction
=====
This module requires that you sign up for Microsoft's Microsoft Cognitive Services and acquire an application key.

#### Steps

1. Visit __[Microsoft Cognitive Services Signup Page](https://azure.microsoft.com/en-us/try/cognitive-services/)__.
2. Select the 'Search' tab.
3. Click 'Get API Key' on 'Bing Search APIs v7' and agree to both checkboxes.
4. Select 'Next' and register using one of the options.
5. This will take you to a page where you need to copy either 'Key 1' or 'Key 2' at the bottom of the 'Endpoints' list.

Installation
=====
To install py-ms-cognitive-ml I recommend using `virtualenv`.

#### Quick instructions for Python 3.*

```sh
pip3 install py-ms-cognitive-ml
```

#### Full instructions for Python 3.*

1. Install Python 3: `sudo apt-get install python3-pip`
2. Install Virtual Environments: `pip install virtualenv`
3. Change to the directory that you want to create your project in and setup an output folder. For example `cd ~/Desktop/ && mkdir bing-api && cd bing-api && mkdir output`
4. Create a Virtual Environment for your project: `virtualenv -p python3 bing-api-env`
5. Install py-ms-cognitive-ml library: `pip3 install py-ms-cognitive-ml`

* Note that py-ms-cognitive-ml requires the requests library.

Usage
=====

Remember to set the `API_KEY` as your own.

#### Getting Images

```py
# Imports
import requests
import os
from py_ms_cognitive_ml import PyMsCognitiveImageSearch

# Settings
search_terms = ["keys", "cats", "dogs"]
serach_quota_per_term = 5
results = []
total_downloads = 0

if not os.path.exists("output"):
    os.mkdir("output")

# Main
for search_term in search_terms:
    
    # Make API call
    search_service = PyMsCognitiveImageSearch('API_KEY', search_term)
    result_list = search_service.search_all(quota=serach_quota_per_term)

    # Scrape images
    if not os.path.exists("output/" + str(search_term)):
        os.mkdir("output/" + str(search_term))

    print("\nDownloading images for term: '" + str(search_term) + "'")

    i = 0
    urls = []
    for i in range(0, len(result_list)):
        print ("Downloading image from " + str(result_list[i].name))

        # Download the image
        try:
            if result_list[i].url not in urls:

                image_file = requests.get(result_list[i].url, stream=True)

                if image_file.status_code == 200:
                    with open("output/" + search_term + "/" + str(i) + "." + result_list[i].extension, 'wb') as f:
                        f.write(image_file.content)
                    
                    urls.append(result_list[i].url)
                else:
                    raise requests.exceptions.RequestException

            else:
                print("Image already downloaded. Skipping image.")

        except requests.exceptions.RequestException:
            print("Something went wrong with the request. Skipping image.")

        i += 1

    results.append(str(len(urls)) + " images downloaded for term '" + str(search_term) + "'.")
    total_downloads += len(urls)

print("\n")

for result in results:
    print(result)

print(str(total_downloads) + " images based on " + str(len(search_terms)) + " search term(s) downloaded.")
```

