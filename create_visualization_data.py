import os, codecs, tarfile, json, csv
import xml.etree.ElementTree as ET

from collections import defaultdict

import numpy as np

def load_topics(file):
    topics = []
    with open(file) as csvfile:
        lreader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in lreader:
            topics.append(row[0])
    return topics

topics = set(load_topics('data/topics_clean.csv'))
print(topics)

# DATA FOR VISUALIZATION 1

with open('data/acl_papers_with_language.json') as json_file:
    acl_papers = json.load(json_file)

    all_languages = defaultdict(int)
    for id, info in acl_papers.items():
        if info["languages"]:
            for l in info["languages"].split(","):
                all_languages[l] += 1
    print(all_languages)
    sorted_langs_counts = sorted(all_languages.items(), key=lambda x: x[1], reverse=True)[:10]
    print(sorted_langs_counts)
    sorted_langs = [l for l, count in sorted_langs_counts]
    print(sorted_langs)

year_to_languages = {}
for paper in acl_papers:
    year = acl_papers[paper]["year"]
    if acl_papers[paper]["languages"]:
        languages = acl_papers[paper]["languages"].split(",")
        for lang in languages:
            if lang in sorted_langs:
                if year in year_to_languages:
                    year_to_languages[year][lang] += 1
                else:
                    year_to_languages[year] = {l: 0 for l in sorted_langs}
                    year_to_languages[year][lang] += 1

with open('project_page/data/stacked_area.csv', 'w') as outfile:
    langs = ",".join(sorted_langs)
    outfile.write("year" + "," + langs + "\n")
    for year in sorted(year_to_languages):
        lang_counts = [str(count) for lang, count in year_to_languages[year].items()]
        outfile.write(str(year) + "," + ",".join(lang_counts) + "\n")

# DATA FOR VISUALIZATION 2

lang_to_topics = defaultdict(int)
topic_total_counts = defaultdict(int)
for paper in acl_papers:
    if acl_papers[paper]["topic"]:
        topic_total_counts[acl_papers[paper]["topic"]] +=  1
        if acl_papers[paper]["languages"]:
            languages = acl_papers[paper]["languages"].split(",")
            for l in languages:
                lang_to_topics[(l, acl_papers[paper]["topic"])] += 1
print(lang_to_topics)
print(topic_total_counts)

topics_by_count = [k for k, v in sorted([(k, v) for k, v in topic_total_counts.items()], key=lambda x: x[1], reverse=True)][:25]

with open('project_page/data/matrix_data.csv', 'w') as outfile:
    langs = '"","' + '","'.join(sorted_langs)
    outfile.write(langs + '"' + "\n")
    for t in topics_by_count:
        topics = []
        new_line = ['"' + t + '"']
        for l in sorted_langs:
            topics.append(lang_to_topics[(l, t)])
            new_line.append(str(lang_to_topics[(l, t)]))
        if sum(topics) > 0:
            outfile.write(",".join(new_line) + "\n")
