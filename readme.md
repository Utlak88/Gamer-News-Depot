## Gamer News Depot
 
This is a gaming news site with the primary purpose of fetching, compiling, and serving to users 1000s of gaming-related news articles per day from 30+ gaming websites with article updates every hour. The scope of this site continues to expand over time.

Django was the primary framework used to construct the site with essential functionalities consisting of Celery tasks and asynchronous REST API consumption.

tasks.py within the 'homepage' folder contains asynchronous fetching code as well as a complex filtering process that identifies the highest quality news articles from the total fetched results.

The website feature of hourly news updates is enabled by the Celery task queue and crontab code located in celery.py within the 'news' folder.

###### Credits

Developed by Stephen Utlak.

###### License

This software is available under the MIT license.