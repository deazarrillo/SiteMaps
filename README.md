# SiteMaps
TimeMap crawler

Current Crawler & Progress Notes:

general.py -
As it stands, the program starts by taking two inputs: project name, and URL. 
It creates a directory from the project name, as well as two files (queued & crawled) that sit within the project directory and only writes in unique URLs that are not currently in one of the two i/o files
This file is mainly for base functions that are needed throughout the rest of the program
Other functions created also delete files from the queue if it exists in the crawled file, convert a file to a set, and vice versa

link_finder.py -
This part of the program creates a class function to parse the input URL’s HTML and collect all links on that page
Includes error/exception handling

spider.py -
The spider program creates a class function with global set variables so each spider is referencing the same queued and crawled files rather than individual ones 
It first create the directory and files
Then crawls the page giving readable cues in the command line as the spiders run
It converts raw data into readable format/checks HTML (exception handling)
It then adds links to the queue, and updates sets and files
The spiders bypass external URLs from archive.org, as well as any URLs that do not contain ‘howard.edu’ (this needs to be updated to be more dynamic?)

domain.py -
This part of the program parses the input URL to capture the domain name (for our purposes, archive.org) to ensure the spider only crawls pages with this domain name. Part of the filtering process in the spider.py file

main.py - 
This file brings everything together while creating worker threads, defining jobs, and telling workers the criteria for doing jobs (i.e. crawling and scraping links - each link is a job)
From this file, you can input PROJECT_NAME (university/directory name), and HOMEPAGE (the seed URL)

