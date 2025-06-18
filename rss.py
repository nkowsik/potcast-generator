import feedparser 
from datetime import datetime
import config
import re
from bs4 import BeautifulSoup

items = []

def update_readme(readme_path, table_content):
    with open(readme_path, 'r') as file:
        content = file.readlines()

    new_content = ['\n', table_content, '\n']

    with open(readme_path, 'w') as file:
        file.writelines(new_content)

date_format = "%a, %d %b %Y %H:%M:%S %z"  # Use %z for timezone-aware parsing

def remove_img_tags(description):
    # Regex to match <img ... /> tags
    img_tag_pattern = re.compile(r'<img[^>]*>')
    return img_tag_pattern.sub('', description)
    
def parse_date(date_str):
    # Replace "GMT" with "+0000" for consistency in parsing
    normalized_date_str = date_str.replace("GMT", "+0000")
    return datetime.strptime(normalized_date_str, date_format)

def remove_html_tags(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    # Extract and return the raw text
    return soup.get_text()

for feeds in config.URLs:
    URL = feeds['feed']
    author = feeds['author']
    feed = feedparser.parse(URL)
    for entry in feed.entries:
        title = entry.get("title", "")
        link = entry.get("link", "")
        description = entry.get("description", "")
        description = remove_html_tags(description)
        

        description = description[0:500]
        if description != "null":
            description = description + "..."
            
        #print("-----")
        #print(description)
        pubDate = entry.get("published", "")
        if pubDate:
            pubDate = parse_date(pubDate)
            pubDate = pubDate.strftime("%Y-%m-%d %H:%M:%S")
        items.append({'title': title, 'link': link, 'description': description, 'published': pubDate, 'company': author})

# Sort the items by published date
items = sorted(items, key=lambda x: x['published'], reverse=True)


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
        padding: 0;
        background-color: #f9f9f9;
        color: #333;
        }
        h1 {
        font-size: 3em;
        color: #0073e6;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
        letter-spacing: 2px;
        background: linear-gradient(to right, #0073e6, #00c6ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        }

    .filter-section {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }

    .filter-section label {
        font-size: 1.2em;
        font-weight: bold;
        margin-right: 10px;
        color: #333;
    }

    .filter-section select {
        padding: 8px 12px;
        font-size: 1em;
        border: 1px solid #ccc;
        border-radius: 5px;
        background-color: #fff;
        color: #333;
        transition: border-color 0.3s;
    }

    .filter-section select:focus {
        border-color: #0073e6;
        outline: none;
    }

    h2 {
        font-size: 1.5em;
        color: #0073e6;
        margin: 0 0 10px;
    }

    a {
        text-decoration: none;
        color: inherit;
    }

    a:hover h2 {
        text-decoration: underline;
    }

    .company {
        font-weight: bold;
        color: #555;
    }

    ul {
        list-style: none;
        padding: 0;
    }
    li {
        background: #fff;
        margin: 15px 0;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s, box-shadow 0.2s;
    }

    li:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }

    p {
        margin: 10px 0 0;
    }
    .banner {
        background: linear-gradient(to right, #0073e6, #00c6ff);
        color: white;
        text-align: center;
        padding: 20px;
        font-size: 1.5em;
        font-weight: bold;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

        /* Responsive Design */
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            li {
                padding: 15px;
                font-size: 14px;
            }

            h2 {
                
                font-size: 18px;
                margin-bottom: 10px;
            }
            p {
                font-size: 14px;
                line-height: 1.4;
            }
        }

        @media (max-width: 480px) {
            h1 {
                font-size: 20px;
                margin-bottom: 15px;
            }
            li {
                padding: 10px;
                font-size: 12px;
            }
            h2 {
                font-size: 16px;
                margin-bottom: 8px;
            }
            p {
                font-size: 12px;
                line-height: 1.3;
            }
        }
            .pagination {
        text-align: center;
        margin-top: 20px;
    }

    .pagination button {
        padding: 10px 20px;
        margin: 0 5px;
        border: none;
        border-radius: 5px;
        background-color: #007bff; /* Primary blue color */
        color: white;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .pagination button:hover {
        background-color: #0056b3; /* Darker blue on hover */
        transform: translateY(-2px); /* Slight lift effect */
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
    }

    .pagination button:disabled {
        background-color: #cccccc; /* Gray for disabled buttons */
        color: #666666;
        cursor: not-allowed;
        box-shadow: none;
        transform: none;
    }

    .pagination span {
        font-size: 18px;
        font-weight: bold;
        margin: 0 10px;
        color: #333333;
    }

    </style>
</head>
<body>
    <div class="banner">
        Welcome to ByteBuzz, where we bring you the latest insights and trends in technology!
    </div>
        <div class="filter-section">
        <label for="company-filter">Filter by Company:</label>
        <select id="company-filter" onchange="filterByCompany()">
            <option value="all">All</option>
            <option value="American Express Technology">American Express Technology</option>
            <option value="ByteByteGo Newsletter">ByteByteGo Newsletter</option>
            <option value="Capital One Tech Blog">Capital One Tech Blog</option>
            <option value="Cloudera Blog">Cloudera Blog</option>
            <option value="Developer Archives - Work Life by Atlassian">Developer Archives - Work Life by Atlassian</option>
            <option value="Docker">Docker</option>
            <option value="Dropbox Tech Blog">Dropbox Tech Blog</option>
            <option value="eBay Tech Blog">eBay Tech Blog</option>
            <option value="Groupon Product and Engineering">Groupon Product and Engineering</option>
            <option value="Instagram Archives">Instagram Archives</option>
            <option value="Instagram Engineering">Instagram Engineering</option>
            <option value="Linked In">Linked In</option>
            <option value="Meta Tech PodCast One">Meta Tech PodCast</option>
            <option value="Shopify Engineering Blog">Shopify Engineering Blog</option>
            <option value="Slack Engineering">Slack Engineering</option>
            <option value="SoundCloud Backstage Blog">SoundCloud Backstage Blog</option>
            <option value="Spotify Engineering">Spotify Engineering</option>
            <option value="Square Corner Blog Feed">Square Corner Blog Feed</option>
            <option value="Tech-at-instacart">Tech-at-instacart</option>
            <option value="The Airbnb Tech Blog">The Airbnb Tech Blog</option>
            <option value="Thumbtack Engineering">Thumbtack Engineering</option>
            <option value="Uber Blog">Uber Blog</option>
            <option value="Zoom Developer Blog">Zoom Developer Blog</option>

        </select>
    </div>
    <ul id="articles-list">
"""
    
    html_end = """
    </ul>
    <div id="pagination" class="pagination">
        <button id="prev-btn" onclick="changePage(-1)" disabled>Previous</button>
        <span id="page-info"></span>
        <button id="next-btn" onclick="changePage(1)">Next</button>
    </div>
        <script>
            const articlesPerPage = 10;
        let currentPage = 1;

        function paginateArticles() {
            const articles = document.querySelectorAll('#articles-list li:not(.hidden)');
            const totalPages = Math.ceil(articles.length / articlesPerPage);

            // Hide all articles
            document.querySelectorAll('#articles-list li').forEach(article => article.style.display = 'none');

            // Show articles for the current page
            const start = (currentPage - 1) * articlesPerPage;
            const end = start + articlesPerPage;
            for (let i = start; i < end && i < articles.length; i++) {
                articles[i].style.display = '';
            }

            // Update pagination buttons
            document.getElementById('prev-btn').disabled = currentPage === 1;
            document.getElementById('next-btn').disabled = currentPage === totalPages;
            document.getElementById('page-info').textContent = `Page ${currentPage} of ${totalPages}`;
        }

        function changePage(direction) {
            currentPage += direction;
            paginateArticles();
        }

        // Initialize pagination
        paginateArticles();
        function filterByCompany() {
            const filterValue = document.getElementById('company-filter').value;
            const articles = document.querySelectorAll('#articles-list li');
            console.log(articles);
            articles.forEach(article => {
                    const company = article.getAttribute('data-company'); // Extract the data-company attribute
                    if (filterValue === 'all' || company === filterValue) {
                        article.style.display = ''; // Show the article if it matches the filter or if "All" is selected
                        article.classList.remove('hidden');
                    } else {
                        article.style.display = 'none'; // Hide the article if it doesn't match
                        article.classList.add('hidden');
                    }
            });
            currentPage = 1;
            paginateArticles();
        }
    </script>
</body>
</html>
"""

    # Generate list items dynamically
    list_items = ""
    for item in items:
        list_items += f"""
        
        <li data-company="{item['company']}">
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
update_readme('index.html', html_content)
