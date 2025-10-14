import os
from argparse import ArgumentParser
import pywikibot
from pywikibot.page import Page

argument_parser = ArgumentParser(
    description="Upload articles from the generatedarticles folder into a"
                + "wikimedia family (specified in user-config.py)"
)

argument_parser.add_argument(
    "-f", "--force",
    action='store_true',
    help="overwrite articles that already exist instead of skipping them,"
        + " will remove any user made changes",
)

argument_parser.add_argument(
    "family",
    help="The family to upload articles to, available families are"
        + " specified in user-config.py"
)

cmd_args = argument_parser.parse_args()

site = pywikibot.Site('en',cmd_args.family)

articles = os.listdir('generatedarticles')

print("Uploading articles...")
print("This is gonna take a while")

index = 0
for article in articles:
    index += 1
    print(f"{index}/{len(articles)}: {article}")
    page = Page(site,article)

    if page.exists() and not cmd_args.force:
        print("Skipping because the article already exists")
        print("Use --force to overwrite the article anyways")
        continue
    
    old_page_text = page.text
    with open(os.path.join('generatedarticles',article)) as f:
        page.text = f.read()
    
    if old_page_text == page.text:
        print("Skipping because the existing article is the same as the new one")
        continue

    page.save(
        "Auto generated article using TGPWikiTool", # Change title
        'nochange', # Watch this article?
        False, # Is this a minor change? (it most likely isn't)
    )