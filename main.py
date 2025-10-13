# can't be bothered to mess with making my own extractor
# even though it would probably be faster than extracting
# everything and sorting through that
from UnityPy.tools import extractor

extractor.extract_assets(
    "/home/noel/.local/share/Steam/steamapps/common/The Genesis Project/The Genesis Project_Data/sharedassets0.resource",
    "extractedassets",
)