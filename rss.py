import feedparser 
from prettytable import PrettyTable

URLs = ["https://blog.bytebytego.com/feed"]

items = []

def generate_table(items):
    table = PrettyTable()
    table.field_names = ["Title", "Link", "Description"]
    for item in items:
        table.add_row([item['title'], item['link'], item['description']])
    return table.get_string()

def update_readme(readme_path, table_content):
    with open(readme_path, 'r') as file:
        content = file.readlines()



    new_content = ['## Latest Articles\n', table_content, '\n']

    with open(readme_path, 'w') as file:
        file.writelines(new_content)

for URL in URLs:
    feed = feedparser.parse(URL)
    for entry in feed.entries:
        title = entry.title
        link = entry.link
        description = entry.description
        pubDate = entry.published
        items.append({'title': title, 'link': link, 'description': description, 'published': pubDate})

table_content = generate_table(items)
update_readme(readme_file, table_content)
