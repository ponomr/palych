import re

PATTERN = re.compile(r'(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?')


def parse_duration(text):
    match = PATTERN.fullmatch(text)
    if not text or not match:
        raise ValueError(f'bad duration: {text!r}')
    hours, minutes, seconds = (int(part or 0) for part in match.groups())
    return hours * 3600 + minutes * 60 + seconds
