import re


def slugify(title):
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
    slug = slug[:40].rstrip('-')
    if not slug:
        raise ValueError(f'no letters a-z or digits in {title!r}')
    return slug
