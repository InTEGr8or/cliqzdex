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

def write_yaml(out_file, yaml_obj):
    f = open(f"{ROOT_DIR}{out_file}.yaml", "w")
    f.write(yaml.dump(yaml_obj, width=110))
    f.close()
    pass

def prod_url(service_name): return f"https://aws.amazon.com/{str.lower(service_name)}"
def cli_url(service_name): return f"https://awscli.amazonaws.com/v2/documentation/api/latest/reference/{str.lower(service_name)}/index.html"
def docs_url(service_name): return f""

CLI_XPATH = '//*[@id="description"]/p'
PROD_XPATH = '//*[@id="aws-page-content"]/main/div[3]'

re_2space = re.compile(r"\s{2,20}")
re_1stspace = re.compile(r"^\s|\s{2,20}|\s$")

def extract_from_nodes(nodes):
    if(len(nodes) == 0): return ""
    node = nodes[0]
    mdown = markdownify(lxml.html.tostring(node))
    mdown = re_1stspace.sub("", mdown)
    mdown = re_2space.sub(" ", mdown)
    return mdown

def get_cli_desc_nodes(service_name):
    url = cli_url(service_name)
    response = requests.get(url)
    nodes = lxml.html.fromstring(response.text).xpath(CLI_XPATH)
    return nodes, url

def loop_file(file_name):
    """Open service list and fetch descriptions from reliable sources"""
    out_services = []
    omitted_services = []
    with open(file_name) as file:
        services = yaml.load(file, yaml.FullLoader)['services']
        for service in tqdm(services):
            nodes, url = get_cli_desc_nodes(service)
            desc = extract_from_nodes(nodes)
            if(len(desc)):
                out_services.append({f"{service}": {
                    "url": url,
                    "description": desc
                } })
            else:
                omitted_services.append(service)

    # output service descriptions and any missed items.
    write_yaml("aws_omitted_services", omitted_services)
    write_yaml("aws_services_descriptions", out_services)

name_file = "D:/T3/Git/cliqzdex/quizzes/aws_exams/aws_service_names.yaml"
loop_file(name_file)
