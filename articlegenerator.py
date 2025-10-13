import json
import os
import re


def parse_litedb_dump(filename:str):
    print(f"Loading data from {filename}...")
    with open('items.txt') as f:
        raw_dump:str = f.read()

    print("Converting to list...")
    # match item separators like /* 5 */, inbetween which is just
    # normal JSON that we can parse
    separated_dump:list[str] = re.split('/\\* \d+ \\*/',raw_dump)
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


if __name__ == "__main__":
    items_list:list[dict] = parse_litedb_dump('items.txt')
    recipes_list:list[dict] = parse_litedb_dump('recipes.txt')

    print("Indexing...")

    print("Writing articles...")
    for item in items_list:
        try:
            with open(os.path.join("generatedarticles",item['Name']),"w") as f:
                f.write(f"""=={item.get('Name',"Unknown")}==
''"{item.get('Description',"???")}"''
{{| class="wikitable"
|+Item info
|-
|ID
|{item.get('_id',"None")}
|-
|Grist
|{item.get('grist',"None")}
|-
|Tags
|{item.get('tags',"None")}
|}}
[[Category:Items]]""")
        except Exception as e:
            if isinstance(e,KeyboardInterrupt):
                # The user should be able to exit
                raise e
            print("ERROR: Failed to make an articles")

    print("""Completed!
You may preview the generated articles in the folder named "generatedarticles"
If you want to upload the results you can run "articleuploader.py"
NOTE: This may overwrite previous work if the pages already exist, currently there is no support for retaining user changes""")
