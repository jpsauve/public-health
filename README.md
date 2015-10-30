# public-health
##The problem

The project deals with public health in the tropics, specifically in Brazil where I currently live. There are several tropical diseases such as dengue fever, schistosomiasis, leprosy, malaria, trachoma and tuberculosis that are increasing and taxing the authorities capacity to respond. In Brazil, municipal governments are mostly responsible for these health issues. The worst diseases (mosquito-borne) can cause epidemics. This is currently the case for dengue fever in many regions: there are 3 times as many cases in 2015, compared to 2014. Some of these diseases (dengue fever in particular) are concentrated in certain neighborhoods of the city, even down to the street level. The authorities have difficulty in rapidly detecting the onset and spread of diseases, acting preventively, responding rapidly to avoid epidemics.

##Requirements of a solution

A solution must help: 1) discover problems early; 2) discover the disease involved; 3) discover where the focus areas are; and 4) sort instances by gravity.
(Exactly what information should be produced by a solution is still vague in my mind: I would  need to talk to the proper authorities to pin this down better.)

##Proposed solution using data science

Affected persons are among the first to know there is a problem. I have supposition (to be tested) that the population will mention these health problems in social medias. I plan to first use the public Twitter API, although other medias can also be included eventually (Facebook, Instagram, Google+, …).
I also assume that the posts will not only reveal the occcurence of disease but will frequently give an indication of geolocation.
I propose to extract Twitter data, and classify posts by disease and geography.
To classify by disease can be done by the disease's name(s), medication, but also by related phrases (eg. rain, for many mosquito-borne diseases).
Geography can be discovered when posts mention a city, a neighborhood, a street name, a point of interest, etc.
Open Street Map data can be used to locate phrases in the posts that can indicate geolocation. Also, GPS localization can be used, when available.

##Data Sources

I used data that I collected from the Twitter API. My objective was not to obtain data for this project but for a political campaign in the city of João Pessoa. However, the data tries to capture "what the population thinks" and I decided to use data for the last 30 days collected (2015-09-12 to 2015-10-12) for this preliminary analysis. The data extractor was written by myslef in python and the dta stored in mongodb. The search included any terms related to João Pessoa (160 search terms). Since the search was not specifically aimed at identifying health issues, better data could probably be obtained.

##Preliminary Analysis

Objectives: 

1) Can posts be used to identify diseases among the population. Does the population mention diseases such as dengue?

2) Is it possible to extract geolocation information by matching post text with Open Street Map data?

Done before the challenge: Data was collected from twitter only for the city of João Pessoa. A total of 136888 posts (112 MB) was collected; after filtering posts that relate to the city, 53849 posts were left (67 MB).

Done for the challenge: I extracted 30 days' worth of posts from mongodb and produced a 67MB json file.
The script written for the challenge locates posts that mention "dengue": there were 63 of them: to me, it appears that objective #1 is answered positively, at least preliminarily. The spike occuring on Oct 12, 2015 may or may not be meaningful but is indicative that something may be going on.
Of these, 44 yielded enough information to be geographically localized at the neighborhood level. That satisfies me preliminarily about objective #2.

##Future

1. Must talk to authorities to have real requirements.

2. To attain scale for a country like Brazil (5,500 cities) or India, I think I will be getting into medium or even big data. I currently think that an implementation could be based on Kafka, Spark Streaming, Elasticsearch (I have restrictions about mongodb), etc. The front end could be done with d3.js, dc.js or flask/bokeh which I have started to use due to the challenge :-)

##Link to public description of data source

https://dev.twitter.com/rest/public

##Link to 1st plot

https://jpsdengue.herokuapp.com/#vol

##Link to 2nd plot

https://jpsdengue.herokuapp.com/#neighborhood

##How much data did you analyze (in MB)?

64 MB

##How did you obtain your dataset?

I used a provided API

##Please provide the EMBED URL to your video

https://www.youtube.com/embed/ow3tWpY7XR4
