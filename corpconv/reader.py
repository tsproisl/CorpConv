#!/usr/bin/env python3

import collections
import logging
import re

Sentence = collections.namedtuple("Sentence", ["id", "tokens"])
Token = collections.namedtuple("Token", ["id", "fields"])
RawSentence = collections.namedtuple("RawSentence", ["id", "lines"])
Line = collections.namedtuple("Line", ["number", "text"])


def read_sentences(corpus, format_string, args):
    sent_del, tok_del, field_del, sent_id, tok_id, missing = format_string
    if sent_del == "e":
        raw_sentences = _read_empty_line(corpus, sent_id)
    elif sent_del == "n":
        raw_sentences = _read_newline(corpus, sent_id)
    elif sent_del == "x":
        raw_sentences = _read_xml(corpus, sent_id, args)
    raw_tokens = _read_raw_tokens(raw_sentences, tok_del)
    sentences = _read_fields(raw_tokens, field_del, tok_id, missing)
    return sentences


def _read_empty_line(corpus, sent_id):
    pattern = re.compile(r'^# sent_id = (.+)$')
    sentence_counter = 0
    sentence_id = None
    lines = []
    for line_counter, line in enumerate(corpus, start=1):
        line = line.rstrip("\n")
        if line == "":
            # Ignore consecutive empty lines
            if len(lines) == 0:
                if line_counter == 1:
                    logging.warning("Empty line at beginning of file (line %d)", line_counter)
                else:
                    logging.warning("Consecutive empty lines (line %d)", line_counter)
                continue
            sentence_counter += 1
            if sentence_id is None:
                if sent_id != "n":
                    logging.warning("Missing ID for sentence %d (line %d)", (sentence_counter, line_counter))
                sentence_id = "s%d" % sentence_counter
            yield RawSentence(sentence_id, lines)
            lines = []
            sentence_id = None
            continue
        if sent_id == "c" and len(lines) == 0:
            m = re.search(pattern, line)
            if m:
                sentence_id = m.group(1)
                continue
            else:
                logging.warning("Badly formatted file (expected sentence ID in line %d)", line_counter)
        if sent_id == "s":
            sentence_id, line = line.split(" ", maxsplit=1)
        elif sent_id == "t":
            sentence_id, line = line.split("\t", maxsplit=1)
        lines.append(Line(line_counter, line))
    if line != "":
        logging.warning("Badly formatted file (missing empty line at end of file)!")
        sentence_counter += 1
        if sentence_id is None:
            if sent_id != "n":
                logging.warning("Missing ID for sentence %d (line %d)", (sentence_counter, line_counter))
            sentence_id = "s%d" % sentence_counter
        yield RawSentence(sentence_id, lines)


def _read_newline(corpus, sent_id):
    pattern = re.compile(r'^# sent_id = (.+)$')
    expect_id = True
    sentence_counter = 0
    line_counter = 0
    sentence_counter = 0
    sentence_id = None
    for line_counter, line in enumerate(corpus, start=1):
        line = line.rstrip("\n")
        if line == "":
            logging.warning("Ignore empty line (%d)" % line_counter)
            continue
        if sent_id == "c":
            if expect_id:
                m = re.search(pattern, line)
                if m:
                    sentence_id = m.group(1)
                    expect_id = False
                    continue
                else:
                    logging.warning("Badly formatted file (expected sentence ID in line %d)", line_counter)
        elif sent_id == "s":
            sentence_id, line = line.split(" ", maxsplit=1)
        elif sent_id == "t":
            sentence_id, line = line.split("\t", maxsplit=1)
        sentence_counter += 1
        if sentence_id is None:
            if sent_id != "n":
                logging.warning("Missing ID for sentence %d (line %d)", (sentence_counter, line_counter))
            sentence_id = "s%d" % sentence_counter
        yield RawSentence(sentence_id, [Line(line_counter, line)])
        expect_id = True
        sentence_id = None


def _read_xml(corpus, sent_id, args):
    tagname = args.xml_tag
    id_attribute = args.xml_id
    # regex taken from Goyvaerts and Levithan's Regular Expressions
    # Cookbook, 2nd ed., section 9.7
    pattern = re.compile(r"""<%s\s(?:[^>"']|"[^"]*"|'[^']*')*?\b%s\s*=\s*("[^"]*"|'[^']*')(?:[^>"']|"[^"]*"|'[^']*')*>""" % (tagname, id_attribute))
    sentence_counter = 0
    line_counter = 0
    sentence_id = None
    lines = []
    for line_counter, line in enumerate(corpus, start=1):
        line = line.rstrip("\n")
        if line == "</%s>" % args.xml_tag:
            sentence_counter += 1
            if sentence_id is None:
                if sent_id != "n":
                    logging.warning("Missing ID for sentence %d (line %d)", (sentence_counter, line_counter))
                sentence_id = "s%d" % sentence_counter
            yield RawSentence(sentence_id, lines)
            lines = []
            sentence_id = None
        elif sent_id == "x" and (line == "<%s>" % tagname or line.startswith("<%s " % tagname)):
            m = re.search(pattern, line)
            if m:
                sentence_id = m.group(1)
            else:
                logging.warning("Badly formatted file (expected sentence ID in line %d)", line_counter)
        elif line.startswith("<"):
            pass
        elif line == "":
            logging.warning("Ignore empty line (%d)" % line_counter)
        else:
            if sent_id == "s":
                sentence_id, line = line.split(" ", maxsplit=1)
            elif sent_id == "t":
                sentence_id, line = line.split("\t", maxsplit=1)
            lines.append(Line(line_counter, line))


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
