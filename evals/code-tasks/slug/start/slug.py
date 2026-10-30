import re


def slugify(title):
    return re.sub(r'\W+', '-', title.lower()).strip('-')
