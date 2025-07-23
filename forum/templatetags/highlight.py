# templatetags/highlight.py  
import re  
from django import template  

register = template.Library()  

@register.filter  
def highlight_urls(text):  
    url_pattern = r'(?P<url>https?://[^\s]+)'    
    return re.sub(url_pattern, r'<span class="highlight">\1</span>', text)  