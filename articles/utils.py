import requests
from bs4 import BeautifulSoup
import cssutils
from datetime import datetime
from .templatetags.custom_filters import format_kaa_date



def normalize_text(text):
    if not text:
        return ""
    text = text.lower() 
    replacements = {
        'ú': 'u', 
        'ǵ': 'g',
        'ó': 'o',
        'á': 'a',
        'ń': 'n',
        'ı': 'i',
    }
    for src, dest in replacements.items():
        text = text.replace(src, dest)

    return text

def get_comment_widget(post_url):
    response = requests.get(post_url+'?embed=1&discussion=1')

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        login_div = soup.find('div', class_='tgme_post_discussion_login')
        if login_div:
            login_div.decompose()
        
        tgme_post_discussion_header_wrap = soup.find('div', class_='tgme_post_discussion_header_wrap')
        if tgme_post_discussion_header_wrap:
            tgme_post_discussion_header_wrap.decompose()
        
        for a in soup.find_all('a'):
            a.name = 'span'
        
        for base in soup.find_all('base'):
            base.decompose()    

        for script in soup.find_all('script'):
            script.decompose()
        
        for time in soup.find_all('time'):
            datetime_str = time.get('datetime')
            if datetime_str:
                print(datetime_str) 
                dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S%z')
                time.string = format_kaa_date(dt)
        
        for emoji in soup.find_all(class_='emoji'):
            del[emoji['style']]

        
        
        cleaned_html = str(soup)
        return cleaned_html
    else:
        return None