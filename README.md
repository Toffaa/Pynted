# Pynted
 
Pynted is a web scraper based on **scrapy** designed to get data from [Vinted.fr](https://www.vinted.fr/).
It gets all the data from user ads (item information, price, upload date, user rate...), and the pictures of the item.

I deployed this scraper on AWS, using the free tier of Amazon EC2 to run the spider, and Amazon S3 to store the result.
With this configuration, I've been able to scrape the entire website in less than 30 minutes (23 exactly), gathering 5188 ads, and 23547 pictures (total size = 1.3GB). You can see the log of this operation [here](results/scraping.log).
The cost for a full scraping of Vinted and storage on S3 is approximatively $0.10 .

Even if this project is quite small, it's using scrapy items to ease the developpement (especially the cleaning and transformation of raw data) and make the spider code cleaner.
Also, the spider uses as much as possible nested loaders and relative XPATH, making it easily updatable if the ad page structure changes. You can check the code in the spider *VintedAd.py*.

I also provided an example of scrapped data [here](results/example.json). I've checked the consistancy of the entire dataset using *pandas*, the only missing values are also missing in the ads (for example, a ad for a videogame doesn't have a size). Please note, if you want to import data into pandas, to use the argument *lines=True* in *pandas.read_json*, as the scraper is providing a *jsonlines* file.

# Usage

```
scrapy crawl VintedAd -a url=myvintedresearch -a download_images=True -a thread=mythread
```

As you can notice, there is three arguments :

* **url** is the url of the Vinted research that you want to scrape. The easiest way to get it is simply make the research on the website, and copy paste the url. For example, passing https://www.vinted.fr/vetements?brand_id[]=303950&catalog[]=76 will make the spider scrape items from the brand "BonneGueule", and only the tops and t-shirts.
Without given argument, the spider will scrap **all ads**, without filter.

* **download_images** Makes the spider downloading ads' images. Without given argument, the value will be set to **False**.

* **thread** is used to define the path where the feed exporter will write the scraped data, as defined in *settings.py*. Without given argument, the value will be set to **default**.

# Installation

As Scrapy does, I recommend using a Python **virtualenv** dedicated to this scraper, to avoid version conflicts.

```console 
git clone https://github.com/Toffaa/Pynted
cd Pynted
# You should create or activate your virtual env here
pip install -r requirements.txt
```

# Settings

Settings like your AWS credentials, your bucket and the desired location of the exported_data must be defined in *settings.py*. You can also provide local path if you don't want to use Amazon S3.
 
# Improvements and development

There is many things that could be done to improve this project, like managing delta loading, to avoid to reload ads already scraped.
Feel free to contact me if you have a request or a question concerning this project ! :)





