#!/usr/bin/python
import sys
import re
import codecs
from textwrap import TextWrapper

import autolink

for post in sys.argv[1:]:
    print "Autoformatting %s..." % post

    with codecs.open(post, 'r', 'utf-8') as f:
        content = f.read()

    content = re.sub(
        "<.*?>(.*?)</.*?>",
        "\\1",
        content,
        flags=re.M
    )

    wrapper = TextWrapper(
        break_long_words=False,
        break_on_hyphens=False,
        width=80
    )

    wrapped = ''
    for line in content.splitlines():
        prefix = ''
        matches = re.match('^\s+', line)
        if matches:
            prefix = matches.group(0)

        wrapped += ('\n' + prefix).join(wrapper.wrap(line)) + '\n'

    content = autolink.linkify(wrapped)

    # Because autolink is buggy
    content = content.replace("http://(http://", "http://")
    content = content.replace(")\">", "\">")

    # This looks weird, because it is. This is to deal with overlapping patterns.
    oldcontent = False
    while oldcontent != content:
        oldcontent = content
        content = re.sub(
            "(^|[ (])@([a-zA-Z0-9_]+)([. )]|$)", 
            "\\1<a href='https://twitter.com/\\2'>@\\2</a>\\3", 
            content,
            flags=re.M
        )

    with codecs.open(post, 'w', 'utf-8') as f:
        f.write(content)
