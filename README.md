# SiteMaps
TimeMap crawler

**Goal:**
The goal of this crawler is twofold. First, to use a [timemap](https://github.com/HBCUMobility/datacollection/tree/main/timemaps/20220104) file as a crawl frontier in order to identify and collect the historical URIs which are missing from the given ttimemap, and second to identify the historical locations of faculty listings for the [HBCU Mobility](https://github.com/HBCUMobility) project. 

Next steps:

1. Current code takes only a single URI as input. Needs to be updated to work with timemap files and potentially additional archives. 
2. Current code has the test site "howard.edu" filter hard coded into the script. May need updating to be more dynamic.
3. Current code is time consuming and not efficient. Need to implement heuristics as a way to create priority buckets for what type of URIs should be moved to the top of the crawler queue (i.e. whether a URI was visited by X years ago, institutional domain name, whether certain words appear in the URI like 'faculty' or 'directory', etc.) 


**Current Crawler & Progress Notes:
**
_general.py -_
As it stands, the program starts by taking two inputs: project name, and URL. 
It creates a directory from the project name, as well as two files (queued & crawled) that sit within the project directory and only writes in unique URLs that are not currently in one of the two i/o files
This file is mainly for defining base functions that are needed throughout the rest of the program
Other functions created also delete files from the queue if it exists in the crawled file, convert a file to a set, and vice versa

Examples of crawled and queued lists can be found [here](https://github.com/deazarrillo/SiteMaps/tree/master/howard)

_link_finder.py -_
This part of the program creates a class function to parse the input URL’s HTML and collect all links on that page
Includes error/exception handling

_spider.py -_
The spider program creates a class function with global set variables so each spider is referencing the same queued and crawled files rather than individual ones 
It first create the directory and files, then crawls the page giving readable cues in the command line as the spiders run.
It converts raw data into readable format/checks HTML (exception handling). It then adds links to the queue, and updates sets and files.
The spiders bypass external URLs from archive.org, as well as any URLs that do not contain ‘howard.edu’ (this likely needs to be updated to be more dynamic)

_domain.py -_
This part of the program parses the input URL to capture the domain name (for our purposes, archive.org) to ensure the spider only crawls pages with this domain name. Part of the filtering process in the spider.py file ensures the crawler stays within an additional domain by passing over any URL that does not include the HBCUs domain. 

_main.py - _
This file brings everything together while creating worker threads, defining jobs, and telling workers the criteria for doing jobs (i.e. crawling and scraping links - each link is a job)

From this file, you can input PROJECT_NAME (university/directory name), and HOMEPAGE (the seed URL)

