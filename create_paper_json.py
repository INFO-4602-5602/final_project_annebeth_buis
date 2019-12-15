import os, codecs, tarfile, json
import xml.etree.ElementTree as ET

from collections import defaultdict

import numpy as np

# The corpus is not included with this project, but can be downloaded at:
# https://acl-arc.comp.nus.edu.sg/archives/acl-arc-160301-aclxml/
# Set your corpus path accordingly!
corpus_path = "corpus/aclxml/P/"
dirs = os.listdir(corpus_path)
print(dirs)

examples = {}
for dir in dirs:
    if dir[0] == "P":
        files = os.listdir(corpus_path + dir)
        for file in files:
            try:
                tree = ET.parse(corpus_path + dir + "/" + file, parser=ET.XMLParser(encoding="utf8"))
            except:
                continue
            root = tree.getroot()
            papers = root.findall("./paper")
            for paper in papers:
                id = paper.get("id")
                if id != "1000":
                    title = paper.find("./title").text.title()
                    author_list = []
                    authors = paper.findall("./author")
                    for author in authors:
                        if author.text:
                            author_list.append(author.text)
                        else:
                            try:
                                first = author.find("./first").text
                                last = author.find("./last").text
                                author_list.append(first + " " + last)
                            except:
                                continue
                    year = paper.find("./year")
                    if not year:
                        incomplete_year = int(dir[-2:])
                        if incomplete_year < 20:
                            year = incomplete_year + 2000
                        else:
                            year = incomplete_year + 1900
                    else:
                        year = year.text
                    examples[dir + "-" + id] = {
                        "id": dir + "-" + id,
                        "title": title,
                        "authors": ", ".join(author_list),
                        "year": year,
                        "languages": None,
                        "topic": None
                    }

with open('data/acl_papers.json', 'w') as outfile:
    json.dump(examples, outfile, indent=4)
