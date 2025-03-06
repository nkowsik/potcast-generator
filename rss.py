import feedparser 
from datetime import datetime
import config


items = []



def update_readme(readme_path, table_content):
    with open(readme_path, 'r') as file:
        content = file.readlines()



    new_content = ['\n', table_content, '\n']

    with open(readme_path, 'w') as file:
        file.writelines(new_content)

date_format = "%a, %d %b %Y %H:%M:%S %z"  # Use %z for timezone-aware parsing

def parse_date(date_str):
    # Replace "GMT" with "+0000" for consistency in parsing
    normalized_date_str = date_str.replace("GMT", "+0000")
    return datetime.strptime(normalized_date_str, date_format)


for feeds in config.URLs:
    URL = feeds['feed']
    author = feeds['author']
    feed = feedparser.parse(URL)
    for entry in feed.entries:
        title = entry.get("title", "")
        link = entry.get("link", "")
        description = entry.get("description", "")
        #print("###############")
        #print(entry)
        pubDate = entry.get("published", "")
        if pubDate:
            pubDate = parse_date(pubDate)
            pubDate = pubDate.strftime("%Y-%m-%d %H:%M:%S")
        #print(title, ' - ', author)
        items.append({'title': title, 'link': link, 'description': description, 'published': pubDate, 'company': author})

# sort the items on published date

items = sorted(items, key=lambda x: x['published'], reverse=True)

#print(items)
# Function to generate HTML content
def generate_html(items):
    html_start = """
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
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
    <h1>Latest Technology Blog</h1>
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
        <a target="_blank" href="{item['link']}">
        <h2>{item['title']}</h2>
        </a>
            
            <p><span class="company">{item['company']}</span>: {item['description']}</p>
        </li>
"""
    
    # Combine all parts
    return html_start + list_items + html_end

# Generate the HTML content
html_content = generate_html(items)

# Write the HTML content to a file
update_readme('README.md', html_content)
