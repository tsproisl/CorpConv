#!/usr/bin/env python3

import argparse
import functools
import logging

import reader
import writer

# format, --only-tokens, delimiter, number of fields


def arguments():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, description="Convert a corpus from a given input format to the desired output format.", epilog="""This converter can convert between corpus formats that can be expressed using the following model:
- A corpus consists of sentences that are separated by a sentence delimiter.
- A sentence consists of tokens that are separated by a token delimiter.
- A token consists of fields (e.g. word form, part of speech, lemma, …) that are separated by a field delimiter.
Sentences and tokens may have IDs and fields may have missing values.

When converting from a format that does not have IDs to one that has, IDs of the form '[st]\d+' will be generated.

The input and output formats are specified via a six-character string. The six characters represent the choices for sentence delimiter, token delimiter, field delimiter, sentence ID, token ID, and missing values.

Sentence delimiter:
  - e: empty line
  - l: newline (only if not used as token delimiter)
  - x: XML tag on a separate line (s-tag by default; can be customized via the --xml-tag option)
Token delimiter:
  - l: newline
  - s: space
  - t: tab
Field delimiter:
  - n: no additional fields, i.e. there is no token-level annotation
  - s: space (only if not used as token delimiter)
  - t: tab (only if not used as token delimiter)
  - character used as delimiter, e.g. /
Sentence IDs:
  - c: comment on preceding line (default pattern: '^# sent_id = (.+)$'; can be customized; cannot be used if sentence delimiter is XML)
  - n: no sentence IDs
  - s: at the beginning of the line, separated by a space (only if token delimiter is space or tab)
  - t: at the beginning of the line, separated by a tab (only if token delimiter is space or tab)
  - x: XML attribute (only if sentence delimiter is XML; id-attribute by default; can be customized via the --xml-id option)
Token IDs:
  - n: no token IDs
  - zero-based field index containing the ID
Missing values:
  - e: empty string
  - n: no missing values (checks that there are no missing values)
  - character used for empty fields, e.g. _

""")
    parser.add_argument("-i", "--input-format", type=parse_format_string, required=True, help="Input format.")
    parser.add_argument("-o", "--output-format", type=parse_format_string, required=True, help="Output format.")
    parser.add_argument("--xml-tag", default="s", help="XML tag that encloses sentences. Default: s")
    parser.add_argument("--xml-id", default="id", help="XML attribute that contains the sentence ID. Default: id")
    parser.add_argument("FILE", type=argparse.FileType("r"), help="The input file")
    args = parser.parse_args()
    return args


def parse_format_string(format_string):
    """"""
    valid_sentence_delimiters = set("e l x".split())
    valid_token_delimiters = set("l s t".split())
    special_field_delimiters = set("n s t".split())
    valid_sentence_ids = set("c n s t x".split())
    special_token_ids = set(["n"])
    special_missing_values = set("e n".split())
    if len(format_string) != 6:
        raise argparse.ArgumentTypeError("Format string must consist of six letters: '%s'" % format_string)
    sent_del, tok_del, field_del, sent_id, tok_id, missing = format_string
    if sent_del not in valid_sentence_delimiters:
        raise argparse.ArgumentTypeError("Not a valid sentence delimiter: '%s'" % sent_del)
    if tok_del not in valid_token_delimiters:
        raise argparse.ArgumentTypeError("Not a valid token delimiter: '%s'" % tok_del)
    if tok_del == sent_del:
        raise argparse.ArgumentTypeError("Cannot use the same delimiter for sentences and for tokens: '%s'" % tok_del)
    if field_del == tok_del:
        raise argparse.ArgumentTypeError("Cannot use the same delimiter for tokens and for fields: '%s'" % tok_del)
    if field_del == "n" and tok_id != "n":
        raise argparse.ArgumentTypeError("Not a valid choice for token ID when field delimiter is 'n': '%s'" % tok_id)
    if sent_id not in valid_sentence_ids:
        raise argparse.ArgumentTypeError("Not a valid choice for sentence ID: '%s'" % sent_id)
    if sent_id == "s" or sent_id == "t":
        if not (tok_del == "s" or tok_del == "t"):
            raise argparse.ArgumentTypeError("If choice for sentence ID is '%s', then token delimiter must be 's' or 't', not '%s'" % (sent_id, tok_del))
    if sent_id == "c" and sent_del == "x":
        raise argparse.ArgumentTypeError("If sentence delimiter is 'x', then choice for sentence ID must not be 'c'")
    if sent_id == "x":
        if sent_del != "x":
            raise argparse.ArgumentTypeError("If choice for sentence ID is 'x', then sentence delimiter must be 'x', not '%s'" % sent_del)
    if not (tok_id in special_token_ids or tok_id.isdigit()):
        raise argparse.ArgumentTypeError("Not a valid choice for token ID: '%s'" % tok_id)
    return format_string


def read_sentences(corpus, format_string, args):
    sent_del, tok_del, field_del, sent_id, tok_id, missing = format_string
    Sentence = collections.namedtuple("Sentence", ["counter", "tokens"])
    sentence_counter = 0
    if sent_del == "e":
        lines = []
        for line in corpus:
            line = line.rstrip()
            if line == "":
                sentence_counter += 1
                yield Sentence(sentence_counter, lines)
                lines = []
            else:
                lines.append(line)
        if line != "":
            logging.warning("Badly formatted file (missing empty line at end of file)!")
            sentence_counter += 1
            yield Sentence(sentence_counter, lines)
    elif sent_del == "n":
        pass
    elif sent_del == "x":
        pass


def main():
    args = arguments()
    sentences = reader.read_sentences(args.FILE, args.input_format, args)
    writer.write_sentences(sentences, args.output_format, args)


if __name__ == "__main__":
    main()
