#!/usr/bin/env python3

import collections
import logging
import re


Sentence = collections.namedtuple("Sentence", ["id", "tokens"])
Token = collections.namedtuple("Sentence", ["id", "fields"])


def read_tokens(raw_sentences, format_string):
    sent_del, tok_del, field_del, sent_id, tok_id, missing = format_string
    raw_tokens = _read_raw_tokens(raw_sentences, tok_del)
    sentences = _read_fields(raw_tokens, field_del, tok_id, missing)
    return sentences


def _read_raw_tokens(raw_sentences, tok_del):
    for sentence_id, lines in raw_sentences:
        if tok_del == "s" or tok_del == "t":
            if len(lines) > 1:
                logging.warning("Sentence %s spans multiple lines (%d–%d). Skipping sentence.", (sentence_id, lines[0].number, lines[-1].number))
                continue
            if tok_del == "s":
                toks = lines[0].split(" ")
            elif tok_del == "t":
                toks = lines[0].split("\t")
            tok_lines = [lines[0].number for t in toks]
        elif tok_del == "l":
            toks = [l.text for l in lines]
            tok_lines = [l.number for l in lines]
        yield sentence_id, toks, tok_lines


def _read_fields(raw_tokens, field_del, tok_id, missing):
    n_fields = None
    for sentence_id, toks, tok_lines in raw_tokens:
        tokens = []
        for token_number, tok, tok_line in enumerate(zip(toks, tok_lines), start=1):
            if field_del == "n":
                fields = [tok]
            elif field_del == "s":
                fields = tok.split(" ")
            elif field_del == "t":
                fields = tok.split("\t")
            else:
                fields = tok.split(field_del)
            if n_fields is None:
                n_fields = len(fields)
            if len(fields) != n_fields:
                logging.warning("Line %d has %d fields instead of %d!", (tok_line, len(fields), n_fields))
            if tok_id == "n":
                token_id = "t%d" % token_number
            else:
                token_id = fields[tok_id]
                fields = fields[:tok_id] + fields[tok_id + 1:]
            if missing == "n":
                if any(f == "" for f in fields):
                    logging.warning("There is an empty field in line %d!", tok_line)
            elif missing != "e":
                fields = ["" if f == missing else f for f in fields]
            tokens.append(Token(token_id, fields))
        yield Sentence(sentence_id, tokens)
