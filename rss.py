import feedparser 
from prettytable import PrettyTable

URLs = ["https://blog.bytebytego.com/feed"]

items = []

def generate_table(items):
    table = PrettyTable()
    table.field_names = ["Title", "Link", "Description"]
    for item in items:
        table.add_row([item['title'], item['link'], item['description'], company])
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
        items.append({'title': title, 'link': link, 'description': description, 'published': pubDate, 'company': 'ByteByteGo'})

#table_content = generate_table(items)






# Function to generate HTML content
def generate_html(items):
    html_start = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Latest Tech Company Developer Forum News</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }
        h1 {
            color: #333;
            text-align: center;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            background-color: #fff;
            margin-bottom: 20px;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h2 {
            color: #2c3e50;
            margin-top: 0;
        }
        p {
            color: #34495e;
        }
        .company {
            font-weight: bold;
            color: #3498db;
        }
    </style>
</head>
<body>
    <h1>Latest Tech Company Developer Forum News</h1>
    <ul>
"""
    
    html_end = """
    </ul>
</body>
</html>
"""

    # Generate list items dynamically
    list_items = ""
    for item in items:
        list_items += f"""
        <li>
            <h2>{item['title']}</h2>
            <p><span class="company">{item['company']}</span>: {item['description']}</p>
        </li>
"""
    
    # Combine all parts
    return html_start + list_items + html_end

# Generate the HTML content
html_content = generate_html(items)

# Write the HTML content to a file
update_readme('README.md', html_content)
