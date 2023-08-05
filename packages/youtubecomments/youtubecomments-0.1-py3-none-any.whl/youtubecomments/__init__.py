import requests
import json
import pandas as pd




def get_comments(key, videoid, outtype):

    url = "https://www.googleapis.com/youtube/v3/commentThreads?key=" + key + "&textFormat=plainText&part=snippet&videoId=" + videoid + "&maxResults=100"
    print("Getting comments data from youtube video...This may take sometime...")

    fulldata = []
    counter = 0
    while True:

        page = requests.get(url)
        pagedata = page.json()

        counter += int(pagedata["pageInfo"]["totalResults"])

        pagedata1 = pagedata["items"]

        for data in pagedata1:
            vid = data["snippet"]["videoId"]
            trc = data["snippet"]["totalReplyCount"]

            temp = data["snippet"]["topLevelComment"]["snippet"]
            adn = temp["authorDisplayName"]
            pat = temp["publishedAt"]
            uat = temp["updatedAt"]
            torg = temp["textOriginal"]
            tdis = temp["textDisplay"]
            lcount = temp["likeCount"]
            api = temp["authorProfileImageUrl"]
            acu = temp["authorChannelUrl"]
            vr = temp["viewerRating"]

            temp_dict = {"videoId":vid, "totalReplyCount":trc, "authorDisplayName":adn, "publishedAt":pat, "updatedAt":uat, "textOriginal":torg, "textDisplay":tdis, "likeCount":lcount, "authorProfileImageUrl":api, "authorChannelUrl":acu, "viewerRating":vr}
            fulldata.append(temp_dict)           

        #fulldata += data["items"]

        try:
        #print(data)
            pagetoken = pagedata["nextPageToken"]
            url = "https://www.googleapis.com/youtube/v3/commentThreads?key=" + key + "&textFormat=plainText&part=snippet&videoId=" + videoid + "&maxResults=100"
            url += "&pageToken=" + pagetoken
            print(str(counter) + " comments extracted.")
        except:
            print(str(counter) + " comments extracted.")
            break

    if outtype == "json":
        return fulldata
    elif outtype == "dataframe":
        return pd.DataFrame(fulldata)
