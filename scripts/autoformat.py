#!/usr/bin/python3

import sys
import re
import codecs
import textwrap

import autolink

for post in sys.argv[1:]:
    print ("Autoformatting %s..." % post)

    with codecs.open(post, 'r', 'utf-8') as f:
        content = f.read()

    # content = re.sub(
    #     "<.*?>(.*?)</.*?>",
    #     "\\1",
    #     content,
    #     flags=re.M
    # )

    wrapped = ''

    # ignore top header
    is_header = False

    for line in content.splitlines():
        if re.match('^---', line) is not None:
            is_header = not is_header
            #print("Found header token")
            wrapped += line + '\n'

            continue
        elif is_header:
            wrapped += line + '\n'

            #print(f"In header: {line}")
            continue

        # if already html, ignore and just add
        if re.match('^\s*<', line) is not None:
            #print(f"Line has HTML: {line}")
            wrapped += line + '\n'
        
        else:

            if re.search('a\s+href', line, re.UNICODE) is not None:
                print(f"Found links in {line}")
            else:
                line = autolink.linkify(line)
                # Because autolink is buggy
                line = line.replace("http://(http://", "http://")
                line = line.replace(")\">", "\">")

            wrapped_line = textwrap.fill(line, width=80, initial_indent='', subsequent_indent='', expand_tabs=True,
                        replace_whitespace=True, fix_sentence_endings=False, 
                        break_long_words=False, drop_whitespace=True, 
                        break_on_hyphens=False, tabsize=4, 
                        max_lines=None, placeholder='')

            wrapped += f'{wrapped_line}<br/>\n'

    content = wrapped
    
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

    content = re.sub("====(.*?)====", "<b>====\\1====</b>", content)

    with codecs.open(post, 'w', 'utf-8') as f:
        f.write(content)
