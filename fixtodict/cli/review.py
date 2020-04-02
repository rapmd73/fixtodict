import click

from ..utils import read_json
from . import cli


@cli.command()
@click.argument("repo", nargs=1, type=click.Path(exists=True))
def review(repo):
    """
    Print a short summary of a FIXtodict-produced JSON document.
    """
    repo = read_json(repo)
    print("FIXtodict-flavoured FIX Repository data.")
    print("- Abbreviations: {:>4}".format(len(repo["abbreviations"])))
    print("- Datatypes:     {:>4}".format(len(repo["datatypes"])))
    print("- Components:    {:>4}".format(len(repo["components"])))
    print("- Fields:        {:>4}".format(len(repo["fields"])))
    print("- Messages:      {:>4}".format(len(repo["messages"])))
    print("  By section and category:")
    for s in repo["sections"]:
        print("  - Section \"{}\": ".format(s), end="")
        by_category = {}
        for (c, c_val) in repo["categories"].items():
            if c_val["section"] == s:
                by_category[c] = 0
                for m_val in repo["messages"].values():
                    if m_val["section"] == s and m_val["category"] == c:
                        by_category[c] += 1
        print(sum([v for v in by_category.values()]))
        for (category, count) in by_category.items():
            print("    - Category \"{}\": {}".format(category, count))
