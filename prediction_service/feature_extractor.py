from src.Phishing_Detector.sec import *
from urllib.parse import urlparse
import re
from bs4 import BeautifulSoup
import socket
import requests
import numpy as np
from datetime import datetime
from urllib.parse import urlparse
import ssl
from urllib.parse import urljoin
from tld import get_tld

class FeatureExtractor:
    
    def __init__(self, url):
        self.url = url
        self.gsb_api =  GSB_API
        self.vt_api = VT_API
        self.us_api = US_API
        self.whois_api = WHOIS_API
        self.opr_api = OPR_API
        self.tld_list_path = 'prediction_service/files/tlds.txt'
        trial_domain = self._get_domain()
        print(trial_domain)

    def general_url_analysis(self):

        parsed_url = urlparse(self.url)
        
        if not parsed_url.scheme:
            url = "https://" + self.url
        else: 
            url = self.url

        with open(self.tld_list_path, 'r') as file:
            tld_list =  [line.rstrip() for line in file]

        def _get_tld(url):
            tld_name = get_tld(url)
            if tld_name.find('.') != -1:
                return tld_name.split('.')
            return tld_name

        def get_domain(url):
            try:
                domain = urlparse(url).netloc
                if domain == "":
                    domain_regex = r'^(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)'
                    match = re.match(domain_regex, url)
                    if match:
                        domain = match.group(1)
                return 0
            except Exception as e:
                return 'Not able to extract domain!'

        def check_tld_limit(url):
            tld = _get_tld(url)
            if type(tld) == str:
                if len(tld) > 10:
                    return 'Abnormal TLD'
            
            if type(tld) == list:
                for i in tld:
                    if len(i) > 10:
                        return 'Abnormal TLD'

            return 0

        def check_tld_common(url):
            tld = _get_tld(url)
            print(tld)
            if type(tld) == str:
                if tld not in tld_list:
                    return 'Uncommon TLD'
            
            if type(tld) == list:
                for i in tld:
                    if i not in tld_list:
                        return 'Uncommon TLD'
            return 0

        report = {
            'domain_status' :  get_domain(url),
            'tld_limit_status' : check_tld_limit(url),
            'common_tld_status' : check_tld_common(url)
        }

        # for res in report.values():
        #     if res != 0:
        #         return report

        return report

    def _get_domain(self):
        try:
            domain = urlparse(self.url).netloc
            if domain == "":
                domain_regex = r'^(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)'
                match = re.match(domain_regex, self.url)
                if match:
                    domain = match.group(1)
            return domain
        except Exception as e:
            print(f"Function{self._get_domain.__name__} failed returning default" )
            raise e
        
    def _get_domain_external(self, url):
        try:
            domain = urlparse(url).netloc
            if domain == "":
                domain_regex = r'^(?:https?:\/\/)?(?:www\.)?([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)'
                match = re.match(domain_regex, url)
                if match:
                    domain = match.group(1)
            return domain
        except Exception as e:
            print(f"Function{self._get_domain.__name__} failed returning default" )
            raise e
        
    def _extract_links_from_strings(self,string_list):
        all_links = []

        for string in string_list:
            # Find all URLs in the string using regular expressions
            urls = re.findall(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', string)

            # If no URLs found, check for URLs without prefix and add the prefix
            if not urls:
                urls_without_prefix = re.findall(r'(?<!\w)([-\w.]+\.[a-zA-Z]{2,6}(?:\/\S*)?)', string)
                urls = ['http://' + url for url in urls_without_prefix]

            all_links.extend(urls)

        return all_links
    
    def _get_dissimilarity(self,parsed_links, domain):
        if len(parsed_links) > 0:
            domain_disimilarity = []
            for link in parsed_links:
                if self._get_domain_external(link) == domain:
                    domain_disimilarity.append(0)
                else: 
                    domain_disimilarity.append(1)
            similarity_perc = (sum(domain_disimilarity) * len(domain_disimilarity)) / 100
            return similarity_perc

        else:
            print('No parsed links found')
            print(f"Function{self._get_dissimilarity.__name__} failed returning default" )
            return 0
        
    def _check_form(self,url):
        try:
            response = requests.get(url)
            content_type = response.headers.get('content-type', '').lower()

            if 'text/html' in content_type and 'form' in response.text.lower():
                return True
            else:
                return False

        except requests.exceptions.RequestException:
            print(f"Function{self._check_form.__name__} failed returning default" )
            return False
        
    def _get_response_with_https(self, url):
        parsed_url = urlparse(url)
    
        if not parsed_url.scheme:
            url = "https://" + url
            
        response = requests.get(url, timeout= 4)
        return response
    
    def _extract_hostname(self, url):
        pattern = r"(?:(?:http|https|ftp):\/\/)?(?:www\.)?([^\/]+)"
        match = re.match(pattern, url)
        
        if match:
            return match.group(1)
        else:
            return self._get_domain(url)
        
    def _get_response(self,url):
        return requests.get(url, timeout=3)
    
    def _get_whois_data(self):
        domain = self._get_domain()
        # API endpoint and parameters
        endpoint = 'https://www.whoisxmlapi.com/whoisserver/WhoisService'
        params = {
            'apiKey': self.whois_api,
            'domainName': domain,
            'outputFormat': 'json'
        }

        # Make the API request
        response = requests.get(endpoint, params=params)
        data = response.json()

        return data

    def _http_request(self,url):
        try:
            parsed_url = urlparse(url)
            if not parsed_url.scheme:
                url = "https://" + self.url
                return url
            else:
                return url
        except:
            print(f"Function{self._http_request.__name__} failed returning default" )
            return url
                    
    
    ## --------------- Features ------------------

    ## 1 - having_IP_Address
    def having_IP_Address(self):
        try:
            # Regular expression to match an IP address
            ip_regex = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

            # Find all IP addresses in the URL
            ip_addresses = re.findall(ip_regex, self.url)

            # If at least one IP address is found, return True
            if len(ip_addresses) > 0:
                return -1
            else:
                return 1
        except:
            print(f"Function{self.having_IP_Address.__name__} failed returning default" )
            return 1
    
    ## 2 - URL_Length
    def URL_Length(self):
        if len(self.url) < 54:
            return 1
        if len(self.url) >= 54 and len(self.url) <= 75:
            return 0
        return -1
    
    ## 3 - Shortining_Service
    def Shortining_Service(self):
        match = re.search('bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|'
                    'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|'
                    'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|'
                    'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|'
                    'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|'
                    'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|'
                    'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|tr\.im|link\.zip\.net', self.url)
        if match:
            return -1
        return 1
    
    ## 4 - having_At_Symbol
    def having_At_Symbol(self):
        if re.findall("@",self.url):
            return -1
        return 1
    
    
    
    ## 5 - double_slash_redirecting
    def double_slash_redirecting(self):
        if self.url.rfind('//')>6:
            return -1
        return 1
    
    ## 6 - Prefix_Suffix
    def Prefix_Suffix(self):
        try:
            domain = self._get_domain()
            match = re.findall('\-', domain)
            if match:
                return -1
            return 1
        except:
            print(f"Function{self.Prefix_Suffix.__name__} failed returning default" )
            return 1
        
    ## 7 - having_Sub_Domain
    def having_Sub_Domain(self): 
        dot_count = len(re.findall("\.", self.url)) - 1
        if 'www.' in self.url:
             dot_count -=  1
        if dot_count == 1:
            return 1
        elif dot_count == 2:
            return 0
        return -1
    
    ## 8 - SSLfinal_State
    def SSLfinal_State(self):

        def using_https(url):
            if url.startswith('https'):
                return True
            else:
                return False
    
        def trust_check_googlesafebrowsing(url, api_key):
            api_url = 'https://safebrowsing.googleapis.com/v4/threatMatches:find'

            payload = {
                "client": {
                    "clientId": "795201079937-90cocmnhrjk9l2717tv4lcaip4rg83j2.apps.googleusercontent.com",
                    "clientVersion": "1.0"
                },
                "threatInfo": {
                    "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "POTENTIALLY_HARMFUL_APPLICATION"],
                    "platformTypes": ["ANY_PLATFORM"],
                    "threatEntryTypes": ["URL"],
                    "threatEntries": [{"url": url}]
                }
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            response = requests.post(api_url, json=payload, headers=headers)

            if response.ok:
                threat_matches = response.json().get("matches", [])
                if threat_matches:
                    return False  # URL found in threat database, considered untrusted

            return True
        
        def trust_check_virustotal(url, api_key):
            api_url = 'https://www.virustotal.com/api/v3/urls'

            headers = {
                'x-apikey': api_key
            }

            params = {
                'url': url
            }

            response = requests.get(api_url, headers=headers, params=params)

            if response.ok:
                data = response.json()
                if data['data']['attributes']['last_analysis_stats']['malicious'] > 0:
                    return False  # URL found to be malicious, considered untrusted

            return True  # URL not found to be malicious, considered trusted
        
        def trust_check_urlscan(url, api_key):
            api_url = 'https://urlscan.io/api/v1/scan/'

            headers = {
                'Content-Type': 'application/json',
                'API-Key': api_key
            }

            data = {
                'url': url
            }

            response = requests.post(api_url, headers=headers, json=data)

            if response.ok:
                result = response.json()
                if result.get('message') == 'Submission successful':
                    scan_id = result.get('uuid')
                    report_url = f'https://urlscan.io/result/{scan_id}/'

                    # Check the report for trustworthiness manually or process the response as needed

                    report_url  # Return the URLScan.io report URL

                if report_url!= None:
                    print(report_url)
                    return True
                else:
                    return False
            return False
        
        def get_certificate_age(url):
            try:
                hostname = self._extract_hostname(url)
                print(hostname)
                context = ssl.create_default_context()
                with socket.create_connection((hostname, 443), timeout=3) as sock:
                    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                        cert = ssock.getpeercert()
                        cert_expiry = cert['notAfter']
                        cert_creation =  cert['notBefore']
                        creation = datetime.strptime(cert_creation, "%b %d %H:%M:%S %Y %Z")
                        expiry_date = datetime.strptime(cert_expiry, "%b %d %H:%M:%S %Y %Z")
                        current_date = datetime.now()
                        age = expiry_date - creation
                        return age.days

            except Exception as e:
                print('Certificate Age not found returning default')
                return 0
            
        http_status = using_https(self.url)
        trust_status = trust_check_googlesafebrowsing(self.url, self.gsb_api) and trust_check_virustotal(self.url, self.vt_api) and trust_check_urlscan(self.url, self.us_api)
        cert_age =  get_certificate_age(self.url)

        if http_status and trust_status and (cert_age >= 30):
            return 1
        elif not http_status and trust_status and (cert_age >= 30):
            return 1
        elif http_status and not trust_status :
            return 0
        else:
            return -1
    
    ## 9 - get_domain_registration_length_status
    def get_domain_registration_length_status(self):
        try:
            data = self._get_whois_data()

            # Extract the registration date from the API response
            creation_date_str = data['WhoisRecord']['registryData']['createdDate']
            creation_date = datetime.strptime(creation_date_str, '%Y-%m-%dT%H:%M:%SZ')

            # Calculate the registration length
            today = datetime.now()
            registration_length = today - creation_date

            if registration_length.days < 365:
                return -1
            else:
                return 1

        except Exception as e:
            print(f"Function{self.get_domain_registration_length_status.__name__} failed returning default" )
            return -1
        
    ## 10 - get_favicon_links_status
    def get_favicon_links_status(self):
        try:
            domain = self._get_domain()
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
            response = requests.get(self.url, headers=headers, timeout=3.5)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            favicon_links = []

            # Find all <link> tags with rel="icon" or rel="shortcut icon"
            link_tags = soup.find_all('link', rel=['icon', 'shortcut icon'])

            for link_tag in link_tags:
                favicon_url = link_tag.get('href')

                # Convert relative URLs to absolute URLs
                favicon_url = urljoin(self.url, favicon_url)

                favicon_links.append(favicon_url)

            if len(favicon_links) > 0:
                for link in favicon_links:
                    if self._get_domain_external(link) == domain:
                        return 1
                    return -1
            return -1

        except Exception as e:
            print(f"Function{self.get_favicon_links_status.__name__} failed returning default" )
            return -1
        
    ##11 - Port
    def is_non_standard_port(self):
        parsed_url = urlparse(self.url)
        non_std_port_status = parsed_url.port is not None and parsed_url.port not in (80, 443)
        if non_std_port_status:
            return -1
        return 1
    
    ## 12 - Https token

    def https_in_domain_status(self):
        domain = self._get_domain()
        if 'https' in domain or 'http' in domain:
            return -1
        return 1
    
    ## 13 - Embedded objects link
    def get_embedded_object_links_status(self):
        try:
            domain = self._get_domain()
            response = self._get_response(self.url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            embedded_links = []

            # Find all image tags
            for img in soup.find_all('img'):
                img_src = img.get('src')
                if img_src:
                    embedded_links.append(urljoin(self.url, img_src))

            # Find all video tags
            for video in soup.find_all('video'):
                video_src = video.get('src')
                if video_src:
                    embedded_links.append(urljoin(self.url, video_src))

            # Find all audio tags
            for audio in soup.find_all('audio'):
                audio_src = audio.get('src')
                if audio_src:
                    embedded_links.append(urljoin(self.url, audio_src))

            # Find all object tags
            for obj in soup.find_all('object'):
                obj_data = obj.get('data')
                if obj_data:
                    embedded_links.append(urljoin(self.url, obj_data))

            print(f'Embedded obj parsed links - {embedded_links}')
        
            similarity_perc = self._get_dissimilarity(embedded_links, domain)

            if similarity_perc <= 22:
                return 1
            elif similarity_perc > 22 and similarity_perc <= 61:
                return 0
            else: 
                return -1

        except Exception as e:
            print(f"Function{self.get_embedded_object_links_status.__name__} failed returning default" )
            return 0
        
    ## 14 - Get Anchor link status
    def get_anchor_links_status(self):
        try:
            domain = self._get_domain()
            response = self._get_response(self.url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            anchor_links = []

            # Find all anchor tags
            for anchor in soup.find_all('a'):
                href = anchor.get('href')
                if href:
                    anchor_links.append(urljoin(self.url, href))

            print(f'anchor parsed links - {anchor_links}')
        
            similarity_perc = self._get_dissimilarity(anchor_links, domain)

            if similarity_perc < 36:
                return 1
            elif similarity_perc >= 36 and similarity_perc <= 71:
                return 0
            else: 
                return -1

        except Exception as e:
            print(f"Function{self.get_anchor_links_status.__name__} failed returning default" )
            return 0
        
    ## 15 - Links from tags
    def get_links_from_tags(self):

        domain = self._get_domain()

        try:
            response = self._get_response(self.url)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            links = []

            # Find links from meta tags
            for meta in soup.find_all('meta'):
                meta_content = meta.get('content')
                if meta_content:
                    links.append(meta_content)

            # Find links from link tags
            for link in soup.find_all('link'):
                link_href = link.get('href')
                if link_href:
                    links.append(urljoin(self.url, link_href))

            # Find links from script tags
            for script in soup.find_all('script'):
                script_src = script.get('src')
                if script_src:
                    links.append(urljoin(self.url, script_src))

            ## The metadata tags may contain strings with the url, parsing the url form the link text recieved from the url
            parsed_links = self._extract_links_from_strings(links)
            print(f'tags parsed links - {parsed_links}')

            similarity_perc =  self._get_dissimilarity(parsed_links, domain)

            if similarity_perc < 46:
                return 1
            elif similarity_perc >= 46 and similarity_perc <= 71:
                return 0
            else: 
                return -1
                
        except Exception as e:
            print(f"Function{self.get_links_from_tags.__name__} failed returning default" )
            return 0
        
    ## 16 - Server form Handeler
    def check_form_sfh(self):
        try:
            # Parse the URL to extract the domain
            parsed_url = urlparse(self.url)
            domain = self._get_domain()

            # Check if the URL is a form
            if self._check_form(self.url):
                # Check if the SFH is about:blank or empty
                if 'sfh' in parsed_url.query.lower() and ('about:blank' in parsed_url.query.lower() or parsed_url.query.lower() == 'sfh='):
                    return -1
                # Check if the SFH refers to a different domain
                elif 'sfh' in parsed_url.query.lower() and parsed_url.query.lower().startswith('sfh=') and domain.lower() != parsed_url.query[4:].lower():
                    return 0
                else:
                    return 1
            else:
                print("Given url is not a form")
                return 1  # Not a form
            
        except:
            print(f"Function{self.check_form_sfh.__name__} failed returning default" )
            return 1
        
    ## 17 - Submitting to mail
    def check_form_redirection_to_mail(self):
        try:
            response = self._get_response(self.url)
            soup = BeautifulSoup(response.content, 'html.parser')

            if self._check_form(self.url):
                form = soup.find('form')
                if form:
                    # Check for "mailto:" in the form action attribute
                    action = form.get('action', '').lower()
                    if action.startswith('mailto:'):
                        return -1

                    # Check for JavaScript-based redirection
                    script_tags = soup.find_all('script')
                    for script in script_tags:
                        if 'location.href' in script.text or 'window.open' in script.text:
                            return -1

                    # Check for server-side redirection
                    # Inspect the server-side code associated with the form submission

                    # Check for PHP mail() function
                    php_tags = soup.find_all('php')
                    for php in php_tags:
                        if 'mail(' in php.text:
                            return -1

        except requests.exceptions.RequestException:
            print(f"Function{self.check_form_redirection_to_mail.__name__} failed returning default" )
            return 1

        return 1
    
    ## 18 - Abnormal Url
    def is_abnormal_url(self):
        try:
            domain = self._get_domain()
            
            data = self._get_whois_data()

            if 'ErrorMessage' in data:
                # Error occurred while making the API request
                print(f"Error: {data['ErrorMessage']}")
                return False

            if 'WhoisRecord' in data:
                whois_record = data['WhoisRecord']
                if whois_record['domainName'] == domain:
                    return 1

            return -1
        
        except Exception as e:
            print(f"Function{self.is_abnormal_url.__name__} failed returning default" )
            return -1
    
    ## 19 - Redirects
    def get_redirects_status(self):
        try:
            parsed_url = urlparse(self.url)
        
            if not parsed_url.scheme:
                url = "https://" + url
            else:
                url = self.url
            
            response = requests.get(url, allow_redirects=True, timeout=3)
            if response.status_code == 200:
                num_redirects = len(response.history)
                
                if num_redirects <= 1:
                    return 1
                elif num_redirects >= 2 and num_redirects <4:
                    return 0
                else:
                    return -1
            return 0
        except Exception as e:
            print(f"Function{self.get_redirects_status.__name__} failed returning default" )
            return 0
        
    ## 20 - OnMouseOver
    def check_onmouseover_status_bar(self):
        try:    
            response = self._get_response(self.url)
            source_code = response.text
            
            if 'onMouseOver' in source_code:
                if 'window.status' in source_code or 'window.defaultStatus' in source_code:
                    return -1
                else:
                    return 1
            else:
                return 1
            
        except:
            print(f"Function{self.check_onmouseover_status_bar.__name__} failed returning default" )
            return 1
        
    ## 21 - Right Click Disabled

    def check_right_click_disabled(self):
        try:  
            response = self._get_response(self.url)
            source_code = response.text
            if re.findall(r"event.button ?== ?2", source_code):
                return -1
            else:
                return 1
        except:
             print(f"Function{self.check_right_click_disabled.__name__} failed returning default" )
             return 1
        
    ## 22 - Popup Window
    def check_popup_with_text_fields(self):
        try:
            response = self._get_response(self.url)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            # Find all <script> tags in the HTML
            script_tags = soup.find_all('script')

            for script_tag in script_tags:
                if 'window.open' in str(script_tag) or 'form-popup' in str(script_tag) or 'alert(' in str(script_tag):
                    # Check if the popup window has text fields
                    if 'input type="text"' in str(script_tag):
                        return -1  # Popup window with text fields found

            return 1  # No popup windows with text fields found
        except:
            print(f"Function{self.check_popup_with_text_fields.__name__} failed returning default" )
            return 1
        
    ## 23 - Using IFrame
    def using_iframe(self):
        try:
            response = self._get_response(self.url)

            if re.findall(r"[<iframe>|<frameBorder>]", response.text):
                return -1
            else:
                return 1
        except:
             print(f"Function{self.using_iframe.__name__} failed returning default" )
             return 1
        
    ## 24 - Age of domian
    def domain_age(self):
        try:
            data =self._get_whois_data()

            if 'ErrorMessage' in data:
                # Error occurred while making the API request
                print(f"Error: {data['ErrorMessage']}")
                return -1

            if 'WhoisRecord' in data:
                whois_record = data['WhoisRecord']
                if whois_record['estimatedDomainAge'] <= 183:
                    return -1
                else:
                    return 1

            return -1
        
        except Exception as e:
            print(f"Function{self.domain_age.__name__} failed returning default" )
            return -1
        
    ## 25 - DNS Record
    def check_dns_record(self):
        try:
            data =self._get_whois_data()

            if 'ErrorMessage' in data:
                # Error occurred while making the API request
                print(f"Error: {data['ErrorMessage']}")
                return -1

            if 'WhoisRecord' in data:
                whois = data['WhoisRecord']

                if "domainName" in whois and len(whois['domainName'])> 0 and whois['domainName'] == self._get_domain():
                    return 1
                else:
                    return -1
            
            return -1
        
        except Exception as e:
            print(f"Function{self.check_dns_record.__name__} failed returning default" )
            return -1
        
    ## 26 - Page Rank

    def get_page_rank_status(self):
        try:
            domain = self._get_domain()
            url = f"https://openpagerank.com/api/v1.0/getPageRank?domains%5B0%5D={domain}"
            headers = {
                "API-OPR": self.opr_api
            }

            response = requests.get(url, headers=headers, timeout = 3.5)
            data = response.json()
            page_rank = data['response'][0]['page_rank_decimal']
            if page_rank >2:
                return 1
            else:
                return -1
            
        except:
            print(f"Function{self.get_page_rank_status.__name__} failed returning default" )
            return -1
        
    ## 27 - Google Index
    def check_google_indexed(self):
        try:    
            google = "https://www.google.com/search?q=site:" + self.url + "&hl=en"
            response = requests.get(google, cookies={"CONSENT": "YES+1"})
            soup = BeautifulSoup(response.content, "html.parser")
            not_indexed = re.compile("did not match any documents")

            if soup(text=not_indexed):
                return -1
            else:
                return 1
        except:
            print(f"Function{self.check_google_indexed.__name__} failed returning default" )
            return -1
        

    def get_feature_list(self):
        feature_list = []
        
        feature_list.append(self.having_IP_Address())
        feature_list.append(self.URL_Length())
        feature_list.append(self.Shortining_Service())
        feature_list.append(self.having_At_Symbol())
        feature_list.append(self.Prefix_Suffix())
        feature_list.append(self.having_Sub_Domain())
        feature_list.append(self.SSLfinal_State())
        feature_list.append(self.get_domain_registration_length_status())
        feature_list.append(self.get_favicon_links_status())
        feature_list.append(self.https_in_domain_status())
        feature_list.append(self.get_embedded_object_links_status())
        feature_list.append(self.get_anchor_links_status())
        feature_list.append(self.get_links_from_tags())
        feature_list.append(self.check_form_sfh())
        feature_list.append(self.get_redirects_status())
        feature_list.append(self.domain_age())
        feature_list.append(self.check_dns_record())
        feature_list.append(self.get_page_rank_status())
        feature_list.append(self.check_google_indexed())

        return np.array(feature_list).reshape(1,19)

