import os
import requests
import yaml

API_KEY = os.environ.get("HARDCOVER_API_KEY")

query = """
{
  me {
    user_books(where: {status_id: {_eq: 2}}) {
      book {
        title
        slug
        cached_contributors
        image {
          url
        }
      }
    }
  }
}
"""
# status_id 2 = currently reading

response = requests.post(
    "https://api.hardcover.app/v1/graphql",
    json={"query": query},
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "User-Agent": "jekyll-blog-currently-reading/1.0"
    }
)

ddata = response.json()
print("Status code:", response.status_code)
print("Response:", data)
user_books = data["data"]["me"][0]["user_books"]

books = []
for ub in user_books:
    book = ub["book"]
    contributors = book.get("cached_contributors", [])
    author = contributors[0]["author"]["name"] if contributors else "Unknown"
    books.append({
        "title": book["title"],
        "author": author,
        "url": f"https://hardcover.app/books/{book['slug']}",
        "cover": book["image"]["url"] if book.get("image") else None
    })

os.makedirs("_data", exist_ok=True)
with open("_data/currently_reading.yml", "w") as f:
    yaml.dump(books, f, allow_unicode=True)

print(f"Wrote {len(books)} book(s) to _data/currently_reading.yml")