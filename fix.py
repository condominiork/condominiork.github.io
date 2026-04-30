import sys

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(r'\`', '`')
content = content.replace(r'\${', '${')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed index.html")
