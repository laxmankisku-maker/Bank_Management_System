import os

for root, dirs, files in os.walk('templates'):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if '|first' in content:
                        print(f'FOUND in: {filepath}')
                        for i, line in enumerate(content.split('\n'), 1):
                            if '|first' in line:
                                print(f'  Line {i}: {line.strip()[:80]}')
            except:
                pass