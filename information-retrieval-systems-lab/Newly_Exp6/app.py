from flask import Flask, render_template, request, jsonify, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService # Correct Service import
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
import requests
from urllib.parse import urljoin, quote_plus
import re
import random
import os
import io

app = Flask(__name__)

# --- User-Agent rotation ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
]

# --- BBC Configuration ---
BBC_CONFIG = {
    "search_url": "https://www.bbc.co.uk/search?q={query}",
    "search_selector": "a.ssrcss-163mj99-PromoLink", # Adjusted selector based on potential BBC changes
    "base_url": "https://www.bbc.co.uk"
}

# --- BBC Scraping Function (using Requests) ---
def scrape_bbc_keyword_detailed(keyword):
    search_url = BBC_CONFIG["search_url"].format(query=quote_plus(keyword))
    selector = BBC_CONFIG["search_selector"]
    base_url = BBC_CONFIG["base_url"]

    print(f"\n🔍 Searching BBC for: {keyword}")
    try:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/"
        }
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Updated selector based on BBC's current structure (might need adjustment)
        links = soup.select('a[data-testid="external-link"]') # Example selector, might need inspection
        if not links:
            # Fallback to potentially older or different structures
            links = soup.select('div[data-testid="default-promo"] a')
        if not links:
             # Another fallback based on common patterns
             links = soup.select('ul[role="list"] li a')

        urls = set()
        for link in links:
            href = link.get('href')
            if href:
                full_url = urljoin(base_url, href)
                # Filter out non-article links if possible (e.g., '/sounds', '/sport')
                if '/news/' in full_url or '/future/' in full_url: # Adjust as needed
                    urls.add(full_url)

        print(f"✅ Found {len(urls)} potential articles on BBC.")
        final_data = []
        total_articles = len(urls)
        print(f"--- Extracting BBC Article Details ---")

        for i, url in enumerate(list(urls), 1):
            print(f"  > ({i}/{total_articles}) Scraping: {url[:70]}...")
            article_info = scrape_article_details(url, "BBC") # Pass source name
            if article_info:
                final_data.append(article_info)
            time.sleep(random.uniform(0.5, 1.5)) # Small delay between requests

        df = pd.DataFrame(final_data)
        # Ensure Date is datetime, handling potential parsing issues
        if "Date" in df.columns:
            df["Date"] = pd.to_datetime(df["Date"], errors='coerce').dt.strftime('%Y-%m-%d')
        df["Date"] = df["Date"].fillna(datetime.now().strftime('%Y-%m-%d'))

        return df

    except requests.exceptions.HTTPError as e:
         print(f"❌ HTTP error scraping BBC search: {e.response.status_code}")
         return pd.DataFrame()
    except Exception as e:
        print(f"❌ Failed BBC: {e}")
        return pd.DataFrame()

# --- AP News Scraping Function (using Selenium) ---
def scrape_ap_news_keyword_detailed(keyword):
    formatted_keyword = quote_plus(keyword)
    url = f'https://apnews.com/search?q={formatted_keyword}'

    print(f"\n🔍 Searching AP News for: {keyword} at {url}")
    print("  > Initializing Selenium browser in VISIBLE (lightweight) mode...")

    options = Options()
    # Lightweight visible options (disable images, eager load)
    options.page_load_strategy = 'eager'
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

    driver = None
    data = []
    SCROLL_COUNT = 3

    try:
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        driver.maximize_window()

        print("  > Attempting to load page (eager strategy)...")
        driver.get(url)
        time.sleep(2) # Give 'eager' page time to settle

        # --- HANDLE COOKIE BANNER ---
        print("  > Looking for cookie banner...")
        try:
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            print("  > Cookie banner found. Clicking 'Accept All Cookies'...")
            driver.execute_script("arguments[0].click();", cookie_button)
            time.sleep(1)
        except TimeoutException:
            print("  > No cookie banner found. Continuing...")

        # --- HANDLE 'SUBSCRIBE' POP-UP ---
        print("  > Looking for 'Subscribe' pop-up...")
        try:
            later_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Later']"))
            )
            print("  > 'Subscribe' pop-up found. Clicking 'Later'...")
            driver.execute_script("arguments[0].click();", later_button)
            time.sleep(1)
        except TimeoutException:
            print("  > No 'Subscribe' pop-up found. Continuing...")

        # --- SCROLL FIRST ---
        print(f"  > Scrolling down {SCROLL_COUNT} times...")
        for i in range(SCROLL_COUNT):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            print(f"    - Scrolled {i+1}/{SCROLL_COUNT}. Waiting 3 seconds...")
            time.sleep(3) # Wait for new content to load

        # --- GRAB HTML *AFTER* SCROLLING ---
        print("\n  > Finished scrolling. Grabbing all loaded HTML...")
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # --- FIND ALL DATA ---
        results_list = soup.find('div', class_='PageList-items')

        if not results_list:
            print("❌ Could not find the main 'PageList-items' container.")
        else:
            search_results = results_list.find_all('div', class_='PageList-items-item')

            if not search_results:
                print("❌ Found list container, but no 'PageList-items-item' inside.")
            else:
                print(f"✅ Found {len(search_results)} articles on AP News. Processing...")
                for item in search_results:
                    headline_tag = item.select_one('bsp-custom-headline span')
                    link_tag = item.select_one('bsp-custom-headline a')
                    snippet_tag = item.select_one('div.PagePromo-description')
                    date_tag = item.select_one('span.Timestamp')

                    headline = headline_tag.text.strip() if headline_tag else 'N/A'
                    link = link_tag['href'] if link_tag else 'N/A'
                    snippet = snippet_tag.text.strip() if snippet_tag else 'N/A'
                    date = date_tag.text.strip() if date_tag else datetime.now().strftime('%Y-%m-%d') # Default date
                    # Attempt to parse date string if found
                    if date_tag:
                         try:
                              # Try common date formats found on AP News
                              parsed_date = pd.to_datetime(date, errors='coerce')
                              if pd.notna(parsed_date):
                                   date = parsed_date.strftime('%Y-%m-%d')
                         except Exception:
                              pass # Keep original string or default if parsing fails

                    # Image might be within a figure or picture tag
                    image_tag = item.select_one('picture img') or item.select_one('figure img')
                    image_url = image_tag['src'] if image_tag and 'src' in image_tag.attrs else 'N/A'

                    # For AP News, we'll use snippet as full content since we're getting from search results
                    # In a real scenario, you'd want to visit each article URL to get full content
                    full_content = snippet if snippet != 'N/A' else "Full content not available."

                    data.append({
                        'Source': 'AP News',
                        'Headline': headline,
                        'Date': date,
                        'Author': 'N/A', # Author is typically not on AP search results
                        'URL': link,
                        'Content_Snippet': snippet,
                        'Full_Content': full_content,
                        'Image URL': image_url
                    })

        df = pd.DataFrame(data)
        return df

    except Exception as e:
        print(f"❌ An error occurred scraping AP News: {e}")
        if driver:
             try:
                driver.save_screenshot('apnews_error.png')
                print("  > Screenshot saved to apnews_error.png")   
             except:
                pass
        return pd.DataFrame()
    finally:
        if driver:
            driver.quit()
            print("  > Closed AP News browser.")


# --- Helper: Extract full article content ---
def extract_full_article_content(soup, url):
    """Extract full article text content from BeautifulSoup object"""
    try:
        # Remove unwanted elements
        for element in soup(['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe', 'form', 'button']):
            element.decompose()
        
        # Try to find article content in common containers
        article_content = None
        content_selectors = [
            'article', 
            '[role="main"]', 
            '.article-content', 
            '.story-content',
            '.article-body',
            '.content-body',
            'main'
        ]
        
        for selector in content_selectors:
            article_content = soup.select_one(selector)
            if article_content:
                break
        
        if not article_content:
            article_content = soup.find('body')
        
        # Extract all paragraphs
        paragraphs = article_content.find_all('p') if article_content else []
        full_text_parts = []
        
        for p in paragraphs:
            p_text = p.get_text(strip=True)
            # Filter out very short paragraphs (likely not content)
            if len(p_text) > 30:
                full_text_parts.append(p_text)
        
        full_text = '\n\n'.join(full_text_parts)
        
        return full_text if full_text else "Full content not available."
    
    except Exception as e:
        print(f"      - Error extracting full content: {e}")
        return "Unable to extract full content."

# --- Shared: Scrape article details (used by BBC) ---
def scrape_article_details(url, source_name="Unknown"): # Added source_name
    try:
        headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Referer": "https://www.google.com/"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- Headline Extraction (More Robust) ---
        headline = "N/A"
        headline_tag = soup.find('h1')
        if headline_tag:
             headline = headline_tag.get_text(strip=True)
        elif soup.title:
             headline = soup.title.get_text(strip=True)


        # --- Date Extraction (More Robust) ---
        date = datetime.now().strftime('%Y-%m-%d') # Default to today
        date_tag = soup.find('time')
        if date_tag and date_tag.has_attr('datetime'):
             date_str = date_tag['datetime']
        else:
             # Look for meta tags (common pattern)
             meta_date = soup.find('meta', attrs={'property': re.compile(r'published_time|datePublished', re.I)}) or \
                         soup.find('meta', attrs={'name': re.compile(r'date|DC.date.issued', re.I)})
             date_str = meta_date['content'].strip() if meta_date and 'content' in meta_date.attrs else None

        if date_str:
            try:
                # Attempt to parse various date formats
                parsed_date = pd.to_datetime(date_str, errors='coerce')
                if pd.notna(parsed_date):
                     date = parsed_date.strftime('%Y-%m-%d')
            except Exception as parse_error:
                print(f"      - Date parsing error for {url}: {parse_error}")
                pass # Keep default date if parsing fails


        # --- Author Extraction (More Robust) ---
        author = "Unknown"
        # Try meta tags first
        meta_author = soup.find('meta', attrs={'name': re.compile(r'author|creator|byl', re.I)}) or \
                      soup.find('meta', attrs={'property': re.compile(r'author', re.I)})
        if meta_author and 'content' in meta_author.attrs:
             author = meta_author['content'].strip()
             # Clean common prefixes like "By "
             if author.lower().startswith("by "):
                  author = author[3:].strip()
        else:
            # Fallback to common class names
            author_tag = soup.find(['span', 'div', 'p', 'a'], class_=re.compile(r'author|byline|writer|contributor', re.I))
            if author_tag:
                 author = author_tag.get_text(strip=True)
                 if author.lower().startswith("by "):
                      author = author[3:].strip()

        # --- Content Snippet (Improved) ---
        content_snippet = "N/A"
        meta_desc = soup.find('meta', attrs={'name': 'description'}) or \
                    soup.find('meta', attrs={'property': 'og:description'})
        if meta_desc and 'content' in meta_desc.attrs:
            content_snippet = meta_desc['content'].strip()
        else:
             # Get first few meaningful paragraphs
             paragraphs = soup.find_all('p')
             text_content = []
             char_count = 0
             for p in paragraphs:
                  p_text = p.get_text(strip=True)
                  if len(p_text) > 20: # Filter out short/empty paragraphs
                       text_content.append(p_text)
                       char_count += len(p_text)
                       if char_count > 200: # Limit snippet length
                            break
             content_snippet = ' '.join(text_content)[:250] + "..." if text_content else "N/A"


        # --- Image URL (More Robust) ---
        image_url = "N/A"
        og_image = soup.find('meta', attrs={'property': 'og:image'})
        if og_image and 'content' in og_image.attrs:
             image_url = urljoin(url, og_image['content'])
        else:
            # Fallback to finding the most prominent image
            main_image = soup.find('figure img') or soup.find('picture img') or soup.find('article img') or soup.find('img')
            if main_image and main_image.get('src'):
                 # Handle potentially relative URLs
                 img_src = main_image.get('src')
                 if img_src and not img_src.startswith(('http:', 'https:', '//')):
                     image_url = urljoin(url, img_src)
                 elif img_src:
                     image_url = img_src
            # Handle cases where src is in data-src (lazy loading)
            elif main_image and main_image.get('data-src'):
                 img_src = main_image.get('data-src')
                 if img_src and not img_src.startswith(('http:', 'https:', '//')):
                     image_url = urljoin(url, img_src)
                 elif img_src:
                     image_url = img_src

        # --- Extract Full Content ---
        full_content = extract_full_article_content(soup, url)

        return {
            "Source": source_name, # Use the passed source name
            "Headline": headline,
            "Date": date,
            "Author": author,
            "URL": url,
            "Content_Snippet": content_snippet,
            "Full_Content": full_content,
            "Image URL": image_url
        }

    except requests.exceptions.RequestException as req_err:
         print(f"      - Network error scraping {url}: {req_err}")
         return None
    except Exception as detail_err:
        print(f"      - Error scraping details for {url}: {detail_err}")
        return None

# --- Flask Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        keyword = data.get('keyword', '').strip()
        source = data.get('source', 'all').lower()

        if not keyword:
            return jsonify({'error': 'Keyword cannot be empty'}), 400

        combined_df = pd.DataFrame()

        if source == "bbc":
            combined_df = scrape_bbc_keyword_detailed(keyword)
        # --- ADDED AP NEWS ---
        elif source == "ap news":
            combined_df = scrape_ap_news_keyword_detailed(keyword)
        elif source == "all":
            print("\n--- Scraping ALL sources ---")
            bbc_df = scrape_bbc_keyword_detailed(keyword)
            ap_news_df = scrape_ap_news_keyword_detailed(keyword) # Call AP News function
            combined_df = pd.concat([bbc_df, ap_news_df], ignore_index=True) # Combine all three
        else:
            return jsonify({'error': 'Invalid source specified. Use "bbc", "ap news", or "all".'}), 400

        if not combined_df.empty:
             # Ensure consistent date format before sending/saving
            if "Date" in combined_df.columns:
                 combined_df['Date'] = pd.to_datetime(combined_df['Date'], errors='coerce')
                 # Sort by date in descending order (latest/most recent first)
                 combined_df = combined_df.sort_values(by='Date', ascending=False)
                 # Convert back to string format after sorting
                 combined_df['Date'] = combined_df['Date'].dt.strftime('%Y-%m-%d')
                 combined_df['Date'] = combined_df['Date'].fillna(datetime.now().strftime('%Y-%m-%d'))

            results = combined_df.to_dict('records')
            
            # Use io.BytesIO for in-memory CSV creation
            csv_output = io.BytesIO()
            combined_df.to_csv(csv_output, index=False, encoding='utf-8')
            csv_output.seek(0) # Rewind the buffer

            # Store the CSV data in a global or session variable for download
            # For simplicity here, we save temporarily. In production, use session or a temporary storage.
            filename = f"News_Scraping_{source.replace(' ', '_')}_{keyword.replace(' ', '_')}_{pd.Timestamp('now').strftime('%Y%m%d_%H%M%S')}.csv"
            
            # Instead of saving to disk, we'll store the filename to reference the data
            # A more robust solution might store the data in memory keyed by filename
            # For this example, we'll still save temporarily but delete later maybe
            with open(filename, 'wb') as f:
                 f.write(csv_output.getvalue())
            app.config[filename] = csv_output.getvalue() # Store data in memory


            return jsonify({
                'success': True,
                'count': len(results),
                'results': results,
                'filename': filename # Send filename for download link
            })
        else:
            return jsonify({
                'success': False,
                'message': f'No results found for "{keyword}" from source: {source}'
            })

    except Exception as e:
        print(f"!!! SERVER ERROR in /scrape: {e}") # Log server errors
        return jsonify({'error': f'An internal server error occurred: {str(e)}'}), 500

@app.route('/download/<filename>')
def download(filename):
    # Retrieve the CSV data from memory or temporary storage
    # This example assumes it was stored in app.config, adjust if using sessions etc.
    csv_data = app.config.get(filename)

    if csv_data:
         # Clean up the temporary storage
         app.config.pop(filename, None)
         try:
            os.remove(filename) # Also remove temp file if saved
         except OSError:
            pass # Ignore if file already removed or never existed

         return send_file(
             io.BytesIO(csv_data),
             mimetype='text/csv',
             as_attachment=True,
             download_name=filename # Use the generated filename for download
         )
    else:
         # Try sending the file from disk if it exists (fallback for previous method)
         if os.path.exists(filename):
             try:
                 response = send_file(filename, as_attachment=True)
                 # Clean up the file after sending
                 # Use try-finally or a background task for robust cleanup
                 try:
                     os.remove(filename)
                 except OSError as remove_error:
                     print(f"Error removing temporary file {filename}: {remove_error}")
                 return response
             except Exception as send_err:
                  print(f"Error sending file {filename}: {send_err}")
                  return jsonify({'error': 'Error sending file.'}), 500
         else:
             print(f"File {filename} not found for download.")
             return jsonify({'error': 'File not found or expired.'}), 404


@app.route('/article_doc')
def article_doc():
    # This will render the article documentation page
    # The article data will be passed via URL parameters or session
    return render_template('article_doc.html')

if __name__ == '__main__':
    # Create a temporary dictionary in app.config to hold CSV data
    app.config['DOWNLOAD_FILES'] = {}
    app.run(debug=True, host='127.0.0.1', port=5000)