from Webscraper.Helpers import *


class Webscraper:
    
    def __init__(self):
        pass


    @staticmethod
    def trafilatura_scraper(url, output_format="json", include_comments=False):
        start_time = time.time()

        downloaded = fetch_url(url)
        result = extract(downloaded, 
                         output_format=output_format, 
                         include_comments=include_comments)
        
        elapsed_time = time.time() - start_time
        print(f"Trafilatura Scraper took {elapsed_time:.2f} seconds.")
        return result


    @staticmethod
    def bs_scraper(url):
        start_time = time.time()

        try:
            url_2 = requests.get(url, timeout=5, verify=False)
            code = url_2.status_code

            if code == 200:
                html = url_2.text
                soup = BeautifulSoup(html, "html.parser")

                for script in soup(['script', 'style']):  # Fixed script tag
                    script.extract()    # rip it out

                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)

            elif code == 404:
                text = "404 Error"
            else:
                text = "Error"

        except:
            text = "Error"
        
        elapsed_time = time.time() - start_time
        print(f"Beautiful Soup Scraper took {elapsed_time:.2f} seconds.")
        return text


    ##### IN PROGRESS #####
    @staticmethod
    def selenium_scraper(url, title=True, text=False):
        start_time = time.time()

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)

        page_result = ""

        if title:
            page_result += driver.title

        if text:
            page_text = driver.find_element_by_tag_name("body").text
            if title:
                page_result += "\n"
            page_result += page_text

        driver.quit()
        
        elapsed_time = time.time() - start_time
        print(f"Selenium Scraper took {elapsed_time:.2f} seconds.")
        return page_result
    ########################