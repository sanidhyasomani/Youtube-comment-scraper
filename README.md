# Youtube-comment-scraper
A basic Python YouTube v3 API to fetch data from YouTube using public API-Key. It can fetch video comments for a given video URL and store the data into output directory in CSV files.

You are required to get the API key from Google API console inorder to use this script.
To create Google API key
https://developers.google.com/places/web-service/get-api-key

How to use
1. Pass --c after file name for fetching comments from videos
2. --max argument for defining the maximum result to return
3. --videourl argument for defining the YouTube URL Mandatory
4. --key argument for defining API key Mandatory

Example: python3 youtube-comment-scraper.py --c --max 10 --
videourl XXXX --key XXXX
