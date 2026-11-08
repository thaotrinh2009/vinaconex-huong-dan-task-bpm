#!/bin/bash
# usage: grab.sh key  -> copies newest tool-result image to img/key.jpg
f=$(ls -t /tmp/claude-tool-results/*/*.jpg /tmp/claude-tool-results/*/*.png 2>/dev/null | head -1)
cp "$f" /home/claude/guide/img/$1.${f##*.}
python3 -c "from PIL import Image;print('$1',Image.open('$f').size)"
