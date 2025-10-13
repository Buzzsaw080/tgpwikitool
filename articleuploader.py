import os
import pywikibot
from pywikibot.page import Page

site = pywikibot.Site('en','local')

articles = os.listdir('generatedarticles')

print("Uploading articles...")
print("This is gonna take a while")

index = 0
for article in articles:
    index += 1
    print(f"{index}/{len(articles)}: {article}")
    page = Page(site,article)
    
    with open(os.path.join('generatedarticles',article)) as f:
        page.text = f.read()

    page.save(
        "Auto generated article using TGPWikiTool", # Change title
        'nochange', # Watch this article?
        False, # Is this a minor change? (it most likely isn't)
    )