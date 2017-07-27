#!/usr/bin/env python3
import sys
for line in sys.stdin:
    if line.strip()=="</s>":
        sys.stdout.write("0\tdummy\tEOS\tdummy-x\t-1\t_\n</s>\n")
    else:
       sys.stdout.write(line)
