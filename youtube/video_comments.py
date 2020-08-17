from collections import defaultdict
import json
import pandas as pd
import requests

def openURL(URL, params):
    r = requests.get(URL + "?", params=params)
    return r.text

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"
YOUTUBE_COMMENT_URL = "https://www.googleapis.com/youtube/v3/commentThreads"
SAVE_PATH = "output/"

class VideoComment:
    def __init__(self, maxResults, videoId, key ):
        self.comments = defaultdict(list)
        self.replies = defaultdict(list)
        self.params = {
                    'part': 'snippet,replies',
                    'maxResults': maxResults,
                    'videoId': videoId,
                    'textFormat': 'plainText',
                    'key': key
                }

    def load_comments(self, mat):
        for item in mat["items"]:
            comment = item["snippet"]["topLevelComment"]
            self.comments["id"].append(comment["id"])
            self.comments["comment"].append(comment["snippet"]["textDisplay"])
            self.comments["author"].append(comment["snippet"]["authorDisplayName"])
            self.comments["likecount"].append(comment["snippet"]["likeCount"])
            self.comments["publishedAt"].append(comment["snippet"]["publishedAt"])

            if 'replies' in item.keys():
                for reply in item['replies']['comments']:
                    self.replies["parentId"].append(reply["snippet"]["parentId"])
                    self.replies["authorDisplayName"].append(reply['snippet']['authorDisplayName'])
                    self.replies["replyComment"].append(reply["snippet"]["textDisplay"])
                    self.replies["publishedAt"].append(reply["snippet"]["publishedAt"])
                    self.replies["likeCount"].append(reply["snippet"]["likeCount"])

    def get_video_comments(self):
        url_response = json.loads(openURL(YOUTUBE_COMMENT_URL, self.params))
        nextPageToken = url_response.get("nextPageToken")
        self.load_comments(url_response)

        while nextPageToken:
            self.params.update({'pageToken': nextPageToken})
            url_response = json.loads(openURL(YOUTUBE_COMMENT_URL, self.params))
            nextPageToken = url_response.get("nextPageToken")
            self.load_comments(url_response)
        self.create_df()


    def create_df(self):
        df = pd.DataFrame().from_dict(self.comments)
        df.to_csv(SAVE_PATH+"parent_video_comment.csv")

        df = pd.DataFrame().from_dict(self.replies)
        df.to_csv(SAVE_PATH+"comment_reply.csv")
