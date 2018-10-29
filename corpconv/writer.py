#!/usr/bin/env python3

import collections
import logging
import re


def write_sentences(sentences, format_string, args):
    sent_del, tok_del, field_del, sent_id, tok_id, missing = format_string
    if field_del == "s":
        f_del = " "
    elif field_del == "t":
        f_del = "\t"
    elif field_del != "n":
        f_del = field_del
    if tok_del == "l":
        t_del = "\n"
    elif tok_del == "s":
        t_del = " "
    elif tok_del == "t":
        t_del = "\t"
    for sentence in sentences:
        toks = []
        for token in sentence.tokens:
            if tok_id != "n":
                token.fields.insert(tok_id, token.id)
            if field_del == "n" and len(token.fields) != 1:
                logging.warning("You specified output field delimiter 'n' but there are %d fields in sentence %d, token %d. Skipping token.", (len(token.fields), sentence.id, token.id))
                continue
            toks.append(f_del.join(token.fields))

