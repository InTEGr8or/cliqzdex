import requests
import yaml
import os
import json
import lxml.html
import lxml.etree as etree
from lxml.cssselect import CSSSelector
from markdownify import markdownify

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def loop_file(file_name):
    out_services = []
    with open(file_name) as file:
        services = yaml.load(file, yaml.FullLoader)['services']
        for service in services:
            url = f"https://aws.amazon.com/{str.lower(service)}"
            response = requests.get(url).text
            tree = lxml.html.fromstring(response)
            nodes = tree.xpath('//*[@id="aws-page-content"]/main/div[3]')

            if(len(nodes) > 0):
                node = nodes[0]
                mdown = markdownify(lxml.html.tostring(node))
                out_services.append({f"{service}": {
                    "url": url,
                    "description": mdown
                } })
                # print(f"{bcolors.OKGREEN}{service}{bcolors.ENDC}", mdown)
            else:
                print(f"{bcolors.WARNING}{service}{bcolors.ENDC}")

    f = open(f"{ROOT_DIR}aws_services_descriptions.yaml", "w")
    f.write(yaml.dump(out_services))
    f.close()

loop_file('D:/T3/Git/cliqz/cliqz/quizzes/aws_service_names.yaml')
