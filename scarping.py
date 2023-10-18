from requests_html import HTML
import sys
import requests
import re
user = {"User-Agent":"Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_2; en-us) AppleWebKit/525.7 (KHTML, like Gecko) Version/3.1 Safari/525.7"}
list = []

def extract_domains(text):
    domain_pattern = r'\b[\w.-]+\.[a-z]{2,6}\b'
    return re.findall(domain_pattern, text)

def main ():
    if len(sys.argv) > 1:
        domain = sys.argv[1]  # Use the command-line argument as the domain
    else:
        domain = sys.stdin.read().strip()  # Read the domain from stdin if no argument is provided
    with requests.session() as s:
        req = s.get(url=f"https://crt.sh/?q={domain}",headers=user)
        source = req.content
        html = HTML(html=source)
        subdomains = html.text
        domain_names = extract_domains(subdomains)
        for dom in domain_names:
            if domain in dom and ("*." not in dom) and (dom not in list) and ("Type: Identity    Match: ILIKE    Search:" not in dom) and ("crt.sh |" not in dom):
                print(dom)
                list.append(dom)

if __name__ == "__main__":
    main()