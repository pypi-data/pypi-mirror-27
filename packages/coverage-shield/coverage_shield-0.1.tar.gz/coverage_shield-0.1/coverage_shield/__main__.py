import argparse
import os

import coverage

import coverage_shield.slug as slug
from coverage_shield.badges import upload


def total(cov: coverage.Coverage) -> float:
    with open(os.devnull, "w") as f:
        return cov.report(file=f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--url", help="Where to post badge data", default='http://badges.volumental.com')
    parser.add_argument("--user", help="User part of slug. Defaults to autodetect")
    parser.add_argument("--repo", help="Repo part of slug. Defaults to autodetect")
    args = parser.parse_args()

    cov = coverage.Coverage()
    cov.load()
    c = total(cov)

    auto_user, auto_repo = slug.autodetect()
    user, repo = args.user or auto_user, args.repo or auto_repo
    svg = upload(args.url, user, repo, "coverage", "{0:.0f}%".format(c), "green")
    print(svg)


if __name__ == "__main__":
    main()
