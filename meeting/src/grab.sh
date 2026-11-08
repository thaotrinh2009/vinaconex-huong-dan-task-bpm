#!/bin/bash
f=$(ls -t /tmp/claude-tool-results/*/*.jpg /tmp/claude-tool-results/*/*.png 2>/dev/null | head -1)
cp "$f" /home/claude/vinaconex-huong-dan-task-bpm/meeting/src/img/$1.${f##*.}
python3 -c "from PIL import Image;print('$1',Image.open('$f').size)"
