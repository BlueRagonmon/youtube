from googleapiclient.discovery import build
import requests
from datetime import datetime


def extract_video_id(url_or_id: str) -> str:
    if "v=" in url_or_id:
        return url_or_id.split("v=")[1].split("&")[0]
    elif "youtu.be" in url_or_id:
        return url_or_id.split("/")[-1]
    return url_or_id


def get_youtube_client(api_key: str):
    return build("youtube", "v3", developerKey=api_key)


def get_video_info(youtube, video_id: str):
    response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()

    if not response["items"]:
        return None

    video = response["items"][0]
    snippet = video["snippet"]
    stats = video["statistics"]

    return {
        "video_id": video_id,
        "title": snippet["title"],
        "channel": snippet["channelTitle"],
        "published_date": datetime.strptime(
            snippet["publishedAt"], "%Y-%m-%dT%H:%M:%SZ"
        ).strftime("%Y-%m-%d"),
        "view_count": int(stats.get("viewCount", 0)),
        "like_count": int(stats.get("likeCount", 0)),
        "comment_count": int(stats.get("commentCount", 0)),
        "thumbnail_url": snippet["thumbnails"]["high"]["url"],
    }


def download_thumbnail(url: str):
    return requests.get(url).content


def get_comments(youtube, video_id: str, max_results=50):
    comments = []

    response = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=max_results,
        textFormat="plainText"
    ).execute()

    for item in response["items"]:
        snippet = item["snippet"]["topLevelComment"]["snippet"]
        comments.append({
            "작성자": snippet["authorDisplayName"],
            "댓글": snippet["textDisplay"],
            "좋아요": snippet["likeCount"],
            "작성일": snippet["publishedAt"][:10]
        })

    return comments
