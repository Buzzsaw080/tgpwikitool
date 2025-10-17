import os
from argparse import ArgumentParser
import pywikibot
from pywikibot.page import Page
from pywikibot.specialbots import UploadRobot

argument_parser = ArgumentParser(
    description="Upload articles from the generatedarticles folder into a"
                + "wikimedia family (specified in user-config.py)"
)

argument_parser.add_argument(
    "-f", "--force",
    action='store_true',
    help="overwrite articles and images that already exist instead of skipping them,"
        + " will remove any user made changes",
)

argument_parser.add_argument(
    "-i", "--images",
    action='store_true',
    help="upload images as well, these have been pulled from the game files"
        + " and so are probably not legal to upload (unless you're a T EAM member)",
)

argument_parser.add_argument(
    "--no-articles",
    action='store_true',
    help="do not upload articles, useful if you're only uploading images",
)

argument_parser.add_argument(
    "family",
    help="The family to upload articles to, available families are"
        + " specified in user-config.py"
)

cmd_args = argument_parser.parse_args()

site = pywikibot.Site('en',cmd_args.family)

articles = os.listdir('generatedarticles')

def upload_articles():
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

def upload_images():
    print("Uploading images...")
    img_bot = UploadRobot()

if not cmd_args.no_articles:
    upload_articles()

if cmd_args.images:
    upload_images(
        os.listdir("generatedimages")
    )

print("Finished")