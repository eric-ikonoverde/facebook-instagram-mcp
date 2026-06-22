import requests
from typing import Any
from config import GRAPH_API_BASE_URL, INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_USER_ID


class InstagramAPI:
    def _request(self, method: str, endpoint: str, params: dict[str, Any], json: dict[str, Any] = None) -> dict[str, Any]:
        url = f"{GRAPH_API_BASE_URL}/{endpoint}"
        params["access_token"] = INSTAGRAM_ACCESS_TOKEN
        response = requests.request(method, url, params=params, json=json)
        return response.json()

    def post_image(self, image_url: str, caption: str) -> dict[str, Any]:
        container = self._request(
            "POST",
            f"{INSTAGRAM_USER_ID}/media",
            {"image_url": image_url, "caption": caption},
        )
        creation_id = container.get("id")
        if not creation_id:
            return container
        return self._request("POST", f"{INSTAGRAM_USER_ID}/media_publish", {"creation_id": creation_id})

    def post_video(self, video_url: str, caption: str, media_type: str = "REELS") -> dict[str, Any]:
        container = self._request(
            "POST",
            f"{INSTAGRAM_USER_ID}/media",
            {"media_type": media_type, "video_url": video_url, "caption": caption},
        )
        creation_id = container.get("id")
        if not creation_id:
            return container
        return self._request("POST", f"{INSTAGRAM_USER_ID}/media_publish", {"creation_id": creation_id})

    def reply_to_comment(self, comment_id: str, message: str) -> dict[str, Any]:
        return self._request("POST", f"{comment_id}/replies", {"message": message})

    def get_posts(self) -> dict[str, Any]:
        fields = "id,caption,media_type,media_url,permalink,timestamp,like_count,comments_count"
        return self._request("GET", f"{INSTAGRAM_USER_ID}/media", {"fields": fields})

    def get_comments(self, media_id: str) -> dict[str, Any]:
        return self._request("GET", f"{media_id}/comments", {"fields": "id,text,username,timestamp,like_count,replies"})

    def delete_media(self, media_id: str) -> dict[str, Any]:
        return self._request("DELETE", media_id, {})

    def delete_comment(self, comment_id: str) -> dict[str, Any]:
        return self._request("DELETE", comment_id, {})

    def hide_comment(self, comment_id: str) -> dict[str, Any]:
        return self._request("POST", comment_id, {"hide": True})

    def unhide_comment(self, comment_id: str) -> dict[str, Any]:
        return self._request("POST", comment_id, {"hide": False})

    def get_insights(self, media_id: str, metric: str, period: str = "lifetime") -> dict[str, Any]:
        return self._request("GET", f"{media_id}/insights", {"metric": metric, "period": period})

    def get_bulk_insights(self, media_id: str, metrics: list[str], period: str = "lifetime") -> dict[str, Any]:
        return self.get_insights(media_id, ",".join(metrics), period)

    def get_media_counts(self, media_id: str) -> dict[str, Any]:
        return self._request("GET", media_id, {"fields": "like_count,comments_count"})

    def send_private_reply(self, comment_id: str, message: str) -> dict[str, Any]:
        return self._request("POST", f"{comment_id}/private_replies", {"message": message})

    def get_comment_replies(self, comment_id: str) -> dict[str, Any]:
        return self._request("GET", f"{comment_id}/replies", {"fields": "id,text,username,timestamp,like_count"})

    def get_permalink(self, media_id: str) -> dict[str, Any]:
        return self._request("GET", media_id, {"fields": "permalink"})

    def get_account_info(self) -> dict[str, Any]:
        fields = "id,username,name,biography,website,followers_count,follows_count,media_count,profile_picture_url"
        return self._request("GET", INSTAGRAM_USER_ID, {"fields": fields})
