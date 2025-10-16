from dataclasses import dataclass, field
from typing import Union
import json
import os
import re


@dataclass
class StrifeKind():
    id:str = field(default="",init=False)
    kind:str = "Other"

    def __post_init__(self,*args,**kwargs):
        self.id = f"kind:{self.kind}"

    def as_wiki_link(self):
        return f"[[:Category:{self.kind}kind]]"


@dataclass
class ItemTag():
    id:str = field(default="",init=False)
    tag:str = "Other"

    def __post_init__(self,*args,**kwargs):
        self.id = f"tag:{self.tag}"

    def as_wiki_link(self):
        return f"[[:Category:{self.tag}]]"


@dataclass
class Item():
    id:str = "???"
    name:str = "???"
    description:str = "???"
    grist:int = 0
    spawnable:bool = False
    tags:list[ItemTag] = field(default_factory=list)
    aliases:list[str] = field(default_factory=list)
    strifekind:StrifeKind = None

    def __init__(self,item_dict:dict[str]):
        self.id = item_dict.get('_id',"???")
        self.name = item_dict.get('Name',"???")
        self.description = item_dict.get('Description',"???")
        self.grist = item_dict.get('Grist',0)
        self.spawnable = item_dict.get('Spawn',False)
        self.tags = item_dict.get('Tags',[])
        self.aliases = item_dict.get('Aliases',[])
        
        # prevents Nonekind from showing up
        strifekind = item_dict.get('Strifekind')
        if strifekind:
            self.strifekind = StrifeKind(kind=strifekind)
    
    def as_wiki_link(self):
        return f"[[{self.name}]]"


@dataclass
class ItemAlias(Item):
    aliasName:str = ""

    def as_wiki_link(self):
        return f"[[{self.name}]]"

    def __init__(self,base:Item,aliasID:str):
        self.__dict__.update(base.__dict__)
        self.aliasName = aliasID


@dataclass
class Recipe():
    itemA:Union[Item, StrifeKind, ItemTag] = None
    method:str = "&&"
    itemB:Union[Item, StrifeKind, ItemTag] = None
    result:Item = None


def safe_append_to_sublist(dictionary:dict[str,list],key:str,value):
    """
        Takes in a dict of lists, and appends to the list at the key specified,
        creating it if it does not exist

        Args:
            dictionary (dict): The dict to operate on
            key (str): The key of the list to append to
            value (any): The value to append to the list
    """
    list = dictionary.get(key)
    if list:
        list.append(value)
    else:
        dictionary[key] = [value]


def parse_litedb_dump(filename:str) -> list[dict[str]]:
    """
        Parse the text output of LiteDB Studio, splitting into separate entries
        and then parsing those as JSON

        Args:
            filename (str): The name of the file to parse
        
        Returns:
            list[dict[str]]: The parsed JSON data
    """
    print(f"Loading data from {filename}...")
    with open(filename) as f:
        raw_dump:str = f.read()

    print("Converting to list...")
    # match item separators like /* 5 */, inbetween which is just
    # normal JSON that we can parse
    separated_dump:list[str] = re.split('/\\* \\d+ \\*/',raw_dump)
    print(f"Got {len(separated_dump)} items")

    print("Parsing...")
    parsed_dump:list[dict[str]] = []
    for item_string in separated_dump:
        try:
            if item_string == "":
                # Empty strings are probably just the beginning and end
                # can be ignored
                continue

            item = json.loads(item_string)
            parsed_dump.append(item)
        except json.JSONDecodeError:
            print("ERROR: Failed to decode an item")
    
    return parsed_dump


def get_recipe_ingredient(item:str) -> Union[Item, StrifeKind]:
    if item.startswith('kind:'):
        return StrifeKind(kind=item[5:])
    elif item.startswith('tag:'):
        return ItemTag(tag=item[4:])

    return items[item]


def create_recipe_table(recipes:list[Recipe]) -> str:
    table = '''{| class="wikitable"
!Item A
!Method
!Item B
!Result
'''
    for recipe in recipes:
        table += '|-\n'
        table += f'|{recipe.itemA.as_wiki_link()}\n'
        table += f'|{recipe.method}\n'
        table += f'|{recipe.itemB.as_wiki_link()}\n'
        table += f'|{recipe.result.as_wiki_link()}\n'
    table += "|}\n"
    
    return table


if __name__ == "__main__":
    # i am so sorry to any potential future maintainer for
    # this variable naming but to be fair, the actual TGP codebase is worse
    # (if the decompilation is to be trusted)
    items_list:list[dict] = parse_litedb_dump('items.txt')
    recipes_list:list[dict] = parse_litedb_dump('recipes.txt')

    print("Indexing...")
    # Key is the item's ID and the value is the item
    items:dict[str,Item] = {}
    # Key is the recipe result and the value is a list of all recipes
    # which make that result
    recipes:dict[str,list[Recipe]] = {}
    # Key is the recipe ingredient and the value is a list of all recipes
    # which use that ingredient
    reverse_recipes:dict[str,list[Recipe]] = {}

    for item in items_list:
        good_item = Item(item)
        items[item['_id']] = good_item
        for alias in good_item.aliases:
            items[alias] = ItemAlias(good_item,alias)

    for recipe in recipes_list:
        try:
            good_recipe = Recipe(
                result=items[recipe['Result']['_id']],
                itemA=get_recipe_ingredient(recipe['ItemA']),
                itemB=get_recipe_ingredient(recipe['ItemB']),
                # Convert methods/operators to how they appear in game
                # AND -> && OR -> ||
                method="&&" if recipe['Method'] == "AND" else "||",
            )

            safe_append_to_sublist(recipes, good_recipe.result.id, good_recipe)
            safe_append_to_sublist(reverse_recipes, good_recipe.itemA.id, good_recipe)
            safe_append_to_sublist(reverse_recipes, good_recipe.itemB.id, good_recipe)
        except KeyError as e:
            print(f"Recipe for {recipe['Result']['_id']} failed because of an invalid item {e.args[0]}")
 
    print("Writing articles...")
    for item in items.values():
        if isinstance(item,Item):
            # Image at top of page
            article = f"[[File:{item.name}.png|300x300px]]\n\n"
            # Item description
            article += f"''\"{item.description}\"''\n"

            # Recipes
            if recipes.get(item.id):
                article += "=== Crafted with ===\n"
                article += create_recipe_table(recipes[item.id])

            # Reverse recipes (what this can be used to craft)
            if reverse_recipes.get(item.id):
                article += "=== Used to craft ===\n"
                article += create_recipe_table(reverse_recipes[item.id])

            # Categories
            article += "[[Category:Items]] "
            for tag in item.tags:
                article += f"[[Category:{tag}]] "
            if item.strifekind:
                article += "[[Category:Strife]] "
                article += f"[[Category:{item.strifekind.kind}kind]] "
            if recipes.get(item.id):
                article += "[[Category:Craftable]] "
            
            articletitle = item.name
        
        elif isinstance(item,ItemAlias):
            article = f"#REDIRECT {item.as_wiki_link()}"
            articletitle = item.aliasID


        try:
            with open(os.path.join("generatedarticles",item.name),"w") as f:
                f.write(article)
        except Exception as e:
            if isinstance(e,KeyboardInterrupt):
                # The user should be able to exit
                raise e
            print("ERROR: Failed to make an article")

    print("""Completed!
You may preview the generated articles in the folder named "generatedarticles"
If you want to upload the results you can run "articleuploader.py" """)
