import re

text = "[('apple',), ('banana',)]"   
print(re.findall(r"\('(.*?)',\)", text))

