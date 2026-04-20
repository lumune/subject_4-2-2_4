import argparse
import os
from pathlib import Path
from typing import Optional
import requests


def load_dotenv(dotenv_path: str = ".env") -> None:
    path = Path(dotenv_path)
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key and key not in os.environ:
            os.environ[key] = value


def search_youtube_videos(
    api_key: str, keyword: str, max_results: int = 5, order: Optional[str] = None
):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": keyword,
        "type": "video",
        "maxResults": max_results,
        "key": api_key,
    }
    if order:
        params["order"] = order

    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    videos = []
    for item in data.get("items", []):
        video_id = item["id"]["videoId"]
        title = item["snippet"]["title"]
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        videos.append({"title": title, "url": video_url})

    return videos


def ask_keyword() -> str:
    while True:
        keyword = input("検索キーワードを入力してください: ").strip()
        if keyword:
            return keyword
        print("キーワードは空にできません。")


def ask_sort_option() -> str:
    print("\n並び替えを選んでください:")
    print("  1) 再生回数順")
    print("  2) 最新動画順")
    print("  3) 指定なし")
    while True:
        choice = input("番号を入力 (1/2/3): ").strip()
        if choice == "1":
            return "views"
        if choice == "2":
            return "latest"
        if choice == "3":
            return "none"
        print("1, 2, 3 のいずれかを入力してください。")


def main():
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError(".env に YOUTUBE_API_KEY を設定してください。")

    parser = argparse.ArgumentParser(description="YouTube Data APIで動画検索を行います。")
    parser.add_argument("keyword", nargs="?", help="検索キーワード（未指定なら対話入力）")
    parser.add_argument(
        "--sort",
        choices=["views", "latest", "none"],
        default=None,
        help="並び順: views(再生回数順) / latest(最新動画順) / none(指定なし)（未指定なら対話入力）",
    )
    args = parser.parse_args()

    keyword = args.keyword if args.keyword else ask_keyword()
    sort_option = args.sort if args.sort else ask_sort_option()

    order_map = {
        "views": "viewCount",
        "latest": "date",
        "none": None,
    }
    selected_order = order_map[sort_option]

    results = search_youtube_videos(
        api_key,
        keyword,
        max_results=5,
        order=selected_order,
    )

    print(f'\n検索キーワード: "{keyword}"')
    print("上位5件の結果:\n")
    for i, video in enumerate(results, start=1):
        print(f"{i}. タイトル: {video['title']}")
        print(f"   URL: {video['url']}\n")


if __name__ == "__main__":
    main()
