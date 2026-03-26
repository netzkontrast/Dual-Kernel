import re

content = ""
with open("tools/common.py", "r", encoding="utf-8") as f:
    content = f.read()

# Extract KNOWN_ENTITIES
match = re.search(r'KNOWN_ENTITIES\s*=\s*\[(.*?)\]', content, re.DOTALL)
if match:
    entities_str = match.group(1)
    # Extract strings from the list
    entities = re.findall(r'"([^"]+)"', entities_str)

    with open("known_entities.txt", "w", encoding="utf-8") as f:
        for ent in entities:
            f.write(f"{ent}\n")
    print(f"Extracted {len(entities)} entities to known_entities.txt")
else:
    print("Could not find KNOWN_ENTITIES")
