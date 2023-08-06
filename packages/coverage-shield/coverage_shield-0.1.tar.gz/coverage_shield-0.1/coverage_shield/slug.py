import os
import re
import subprocess


def autodetect():
    """Returns a tuple (user, repo). Tries to parse git remote url and also
    Travis CI environment variable."""
    remote = subprocess.check_output("git remote get-url origin".split()).decode()
    match = re.match(r"git@github.com:(.+)\/(.+)\.git", remote)
    if match:
        user, repo = match.groups()
        return user, repo

    slug = os.environ.get('TRAVIS_REPO_SLUG')
    if slug:
        user, repo = slug.split('/')
        return user, repo

    # autodetect failed
    return None, None
