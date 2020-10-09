import requests
import yaml
import os
import lxml.html
from markdownify import markdownify
from tqdm import tqdm
import re


ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) + "/"
print(ROOT_DIR)
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
    omitted_services = []
    re_2space = re.compile(r"\s{2,20}")
    re_1stspace = re.compile(r"^\s|\s{2,20}|\s$")
    re_colon = re.compile(r":")
    with open(file_name) as file:
        services = yaml.load(file, yaml.FullLoader)['services']
        for service in tqdm(services):
            url = f"https://aws.amazon.com/{str.lower(service)}"
            response = requests.get(url).text
            tree = lxml.html.fromstring(response)
            nodes = tree.xpath('//*[@id="aws-page-content"]/main/div[3]')

            if(len(nodes) > 0):
                node = nodes[0]
                mdown = markdownify(lxml.html.tostring(node))
                mdown = re_1stspace.sub("", mdown)
                mdown = re_2space.sub(" ", mdown)
                # mdown = re_colon.sub(";", mdown)
                out_services.append({f"{service}": {
                    "url": url,
                    "description": mdown
                } })
                # print(f"{bcolors.OKGREEN}{service}{bcolors.ENDC}", mdown)
            else:
                # print(f"{bcolors.WARNING}{service}{bcolors.ENDC}")
                omitted_services.append(service)

    f = open(f"{ROOT_DIR}aws_omitted_services.yaml", "w")
    f.write(yaml.dump(omitted_services, width=110))
    f.close()

    f = open(f"{ROOT_DIR}aws_services_descriptions.yaml", "w")
    f.write(yaml.dump(out_services, width=110))
    f.close()

loop_file('D:/T3/Git/cliqz/cliqz/quizzes/aws_service_names.yaml')
