<img width="497" height="286" alt="tgpwikitool4" src="https://github.com/user-attachments/assets/f04511ac-ae83-4899-9cbf-8fa0c7d5a340" />

The Genesis Project wiki tool (TGPWikiTool) is a tool that can automatically generate and upload mediawiki articles for every item in the game, including recipes, descriptions, stats and categories
(Not affiliated with the genesis project, but the hope is that this will be used for the official wiki)

[Skip to the instructions](#usage)

## Examples
Note: all of these examples are from a generic mediawiki instance, and so will not have the wiki.gg theming, also, this tool doesn't generate any images (which is probably the most annoying thing that should have been the one automated, but whatever)

Main recipe page  
<img width="938" height="764" alt="Screenshot_20251017_011401" src="https://github.com/user-attachments/assets/dfb378cf-9a07-40df-a444-3d915d0eecc5" />

Smart Hammer  
<img width="637" height="419" alt="image" src="https://github.com/user-attachments/assets/ce745c33-ebc9-4fef-8b7c-c5009c7bee01" />

Sorting by tag  
<img width="1200" height="384" alt="image" src="https://github.com/user-attachments/assets/b2ff0a5e-33af-4d29-b304-8f4bb8f09ba4" />

Sorting by strifekind  
<img width="1350" height="560" alt="image" src="https://github.com/user-attachments/assets/40e78b0e-cb70-4b86-940d-36fb808386be" />


## Category meanings
|Category|Meaning|
|-------|------|
|Item|An item, applied to all articles|
|Burning, Bouncy, etc|An item tag, as defined by the game|
|Strife|An item with any strifekind|
|___kind|An item in the named strifekind|
|Armor|An item with Hatkind, Facekind, Shirtkind, Pantskind, or Shoeskind|
|Weapon|An item with any strifekind that Armor doesn't cover|
|Craftable|An item which can be alchemized|
|Spawnable|An item which can be found naturally in the world|


## Usage
Note: Only tested on linux using a generic mediawiki server created using [this guide](https://www.mediawiki.org/wiki/Manual:Running_MediaWiki_on_Arch_Linux), this may not work for you, but if it doesn't let me know and i will try and fix it!

### Setup
First download TGPWikiTool either using `git clone https://github.com/Buzzsaw080/tgpwikitool` if you have git or click the green code button at the top of the page and press download zip  
TGPWikiTool requires you to have [python](https://www.python.org/downloads/) and pywikibot, so
download and run the python installer, and with a terminal in the folder of tgpwikitool run
```bash
python -m venv .venv
source .venv/bin/activate
pip install pywikibot
```

### Uploading articles
You can use [my premade articles](https://github.com/Buzzsaw080/tgpwikitool/releases/latest) to make the process easier, or you can [make your own](#getting-the-article-data-yourself)  
If using premade articles, extract generatedarticles.zip into the tgpwikitool folder  
You will also need to create a user-config.py file with a family for your mediawiki server, which can be achieved using [this guide](https://www.mediawiki.org/wiki/Manual:Pywikibot/Use_on_third-party_wikis), user-config.example.py only has a local family set which just uploads to a local mediawiki server  
Once you have your user-config file you can run articleuploader.py, it takes two arguments, a mediawiki family and an optional force flag which overwrites already generated articles  
`python articleuploader.py -f local` (to upload to a local mediawiki server, overwriting articles)


### Getting the item data yourself
Although i do provide premade articles and item files, if you want to get the data yourself, you can (like if a later version of TGP comes out and i haven't updated)
[LiteDB studio](https://github.com/litedb-org/LiteDB.Studio) is used to get item and recipe data, so download and run it and then click connect
<img width="431" height="277" alt="An arrow pointing to the connect button" src="https://github.com/user-attachments/assets/8363e8dd-4f80-422d-bf41-7d2243e7853a" />  
Then in the popup that appears,
1. Open the items.ldb file located in `The Genesis Project_Data/StreamingAssets/items.ldb` in the genesis project files (click browse local files in steam)
2. Turn it on read only
3. Click connect  
<img width="608" height="472" alt="image" src="https://github.com/user-attachments/assets/c3b7634b-3e0f-486f-ae4d-16ec05df39ea" />  
Once connected,  
1. Type `SELECT $ FROM LDBItem LIMIT 90000;` into the query field  
2. Click run and wait for it to finish (unfreeze)  
3. Click text  
4. Copy all the text that shows up (ctrl+a ctrl+c)  
5. Paste the text into a new file called `items.txt` in the same folder as tgpwikitool
6. Repeat steps 1-5 but replace `LDBItem` with `LDBRecipe` and `items.txt` with `recipes.txt`
<img width="877" height="572" alt="image" src="https://github.com/user-attachments/assets/0acdbfe7-416f-47c7-af93-d168840ab0b2" />
Then run `python articlegenerator.py` which should only take a second or two and generate all the articles, you are now free to [upload the articles](#uploading-articles)  

## Contributing
Pull requests are welcome, but please open an issue first, issues can be made about anything that you think should be changed, not just bugs!
AI use is not allowed when contributing in any form
