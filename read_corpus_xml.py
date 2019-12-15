import re, os, codecs, tarfile, json, csv, string
import xml.etree.ElementTree as ET

from collections import defaultdict

def load_languages(file):
    languages = []
    with open(file) as csvfile:
        lreader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in lreader:
            languages.append(row[0])
    return languages

def load_topics(file):
    topics = []
    with open(file) as csvfile:
        lreader = csv.reader(csvfile, delimiter=",", quotechar='"')
        for row in lreader:
            topics.append(row[0])
    return topics

def load_papers(file):
    with open(file) as json_file:
        papers = json.load(json_file)
    return papers

languages = set(load_languages('data/languages.csv'))
print(languages)

topics = set(load_topics('data/topics_clean.csv'))
print(topics)

papers = load_papers('data/acl_papers.json')
print(papers)

# Corpus is not uploaded with the project, but can be downloaded online.
corpus_path = "corpus/acl-arc.comp.nus.edu.sg/archives/acl-arc-160301-omnipage/"
dirs = os.listdir(corpus_path)

# Only get directories that start with P; which are ACL Proceedings.
ACL_dirs = [dir for dir in dirs if re.match("^P.", dir)]
print(ACL_dirs)

for dir in ACL_dirs:
    try:
        tar = tarfile.open(corpus_path + dir,encoding='utf-8')
    except:
        print('Not a tarfile', dir)
        continue

    utf8reader = codecs.getreader('utf-8')
    count = 0
    for name in tar.getmembers():
        print(name.name)
        paper_id = name.name.split("/")[2].split("-")
        paper_id = paper_id[0] + "-" + paper_id[1]

        # Make sure we only get paper XMLs.
        if name.name.split("/")[-1][0] == "P" and not "1000" in paper_id:
            fp = utf8reader(tar.extractfile(name))
            xmlstring = fp.read()
            try:
                tree = ET.ElementTree(ET.fromstring(xmlstring))
            except:
                continue
            root = tree.getroot()

            text = []

            for elem in list(root.iter()):
                if elem.tag == "{http://www.scansoft.com/omnipage/xml/ssdoc-schema3.xsd}wd":
                    if elem.text: # and elem.text != "References":
                        text.append(elem.text.translate(str.maketrans('', '', string.punctuation)))
                    else:
                        continue
            count += 1

            # Get language information for paper
            language_in_paper_count = defaultdict(int)
            for word in text:
                if word in languages:
                    language_in_paper_count[word] += 1
            print(language_in_paper_count)

            # Get topic information for paper
            full_text = " ".join(text)

            topic_in_paper_count = defaultdict(int)
            for topic in topics:
                if topic in full_text:
                    topic_in_paper_count[topic] = full_text.count(topic)
            # print(topic_in_paper_count)

            # Pick the most common topic as the main topic
            if len(topic_in_paper_count) > 0:
                main_topic = sorted(topic_in_paper_count, key = lambda x: x[1])[0]
            else:
                main_topic = None
            # print(main_topic)

            try:
                if len(language_in_paper_count) == 0:
                    papers[paper_id]["languages"] = "No language"
                else:
                    papers[paper_id]["languages"] = ",".join(list(language_in_paper_count))
                papers[paper_id]["topic"] = main_topic
                print(papers[paper_id])
            except:
                continue

with open('data/acl_papers_with_language.json', 'w') as outfile:
    json.dump(papers, outfile, indent=4)
