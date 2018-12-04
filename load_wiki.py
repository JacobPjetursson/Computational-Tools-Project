import glob
import re
import io


def load_wiki_files(path):
    article_dict = {}
    files = glob.glob(path)
    for file in files:
        f = io.open(file, 'r', encoding="utf-8")
        title = ""
        article = ""
        for line in f.readlines():
            if not line or line == "\n":
                continue
            if line[:8] == "<doc id=":
                # Start of article
                regexp = 'title="(.*)"'
                title = re.findall(regexp, line)[0]
            elif line[:7] == "</doc>\n":
                article_dict[title] = article
                article = ""
            else:
                article += line
    return article_dict