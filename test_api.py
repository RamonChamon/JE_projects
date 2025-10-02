import requests

# The Way (book_id=12)
chapters_url = "https://escriva.org/api/v1/chapters?book_id=12&lang=en"
chapters = requests.get(chapters_url).json()["results"]

# Take the first chapter for testing
first_chapter_id = chapters[0]["id"]
print(f"Testing with chapter_id={first_chapter_id}")

# Fetch points from this chapter
points_url = f"https://escriva.org/api/v1/points?chapter_id={first_chapter_id}&lang=en"
points = requests.get(points_url).json()["results"]

# Print the first 5 points to see all available fields
for p in points[:5]:
    print("\n--- Point ---")
    for key, value in p.items():
        print(f"{key}: {value}")
