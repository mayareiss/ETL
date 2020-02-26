# ETL

This project is taking a snapshot at luxury goods that are available on two online resellers. According to reports (https://www.thefashionlaw.com/home/the-luxury-resale-market-is-growing-faster-than-the-primary-luxury-goods-segment-per-bcg), the secondary market for luxury goods is growing at a greater rate than the primary market, with the forecast that the secondary market will grow to $51 billion by 2023 (https://www.bloomberg.com/opinion/articles/2019-11-12/realreal-poshmark-other-resale-sites-are-good-even-for-gucci). The growth of the secondary market is due to multiple reasons, including combating climate change (buying from the secondary market has an exponentially lower carbon footprint than buying new items), saving money, and also more recently there is a trend for investment purposes, especially for higher end bags that hold on to their original value. 

The benefits of luxury resale are real, numerous and significant with regard to preserving the environment, saving money and investing in quality products (https://www.codogirl.com/blogs/news/why-millions-of-women-are-choosing-luxury-resale).

This ETL project collected luxury bag data from online secondary markets, specifically eBay.com, which has been the dominant online resale and auction site since its inception in 1005, and rebag.com, a relatively newcomer that specializes in selling luxury bags and recently introduced Clair, a.k.a. the Comprehensive Luxury Appraisal Index for Resale, an algorithmic tool that shows bag owners the resale spot prices of their bags if they were to liquidate them immediately by selling to Rebag.

Project steps:

1.	Extraction - I selected ten of the top most popular designers available on the secondary market, according to https://www.businessinsider.com/the-realreal-most-popular-brands-resale-list-2019-8. For each designer, I ran two scrapers:

Ebay:
Starting with an existing publicly available ebay scraper (https://github.com/cpatrickalves/scraping-ebay), which contains a script to scrape eBay product data using scrapy, I modified the search columns to include the name of the item, the item status, the price, as well as the shipping cost, time remaining on the auction, number of bis, as well as the url for the item. I ran the code in terminal for the top ten most searched luxury brands per a report by the RealReal (https://promotion.therealreal.com/resale-report-2019/), a leading online luxury secondary market retailer. The files were saved as csv

Rebag:
Ran a scraper to pull live data of available bags for sale from ten different designers. The scraper pulled the name of the bag, the price point, the designer name and the url page from where it was scraped. The files were saved as json.

2.	Transform:

Utilized Pandas functions in Jupyter notebook to upload each file
    
Reviewed files and turned into dataframes
    
Cleaned up data to remove duplicates, extraneous columns and reset index
    
Extracted information from data and added new columns to represent bag type and material

Merged the two separate files into one large file containing all data

3.	Load

The final stage was loading the file of all data into Postgres using SQL Alchemy

  


