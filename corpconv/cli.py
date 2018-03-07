#!/usr/bin/env python3

import argparse
import functools
import logging


from corpconv import corpus_readers
from corpconv import corpus_writers


# format, --only-tokens, delimiter, number of fields

"""foo

This converter can convert between corpus formats that can be expressed using the following model:
- A corpus consists of sentences that are separated by a sentence delimiter.
- A sentence consists of tokens that are separated by a token delimiter.
- A token consists of fields (e.g. word form, part of speech, lemma, …) that are separated by a field delimiter.
Sentences and tokens may have IDs and fields may have missing values.


Sentence delimiter:
  - e: empty line
  - n: newline (only if not used as token delimiter)
  - x: XML tag on a separate line (s-tag by default; can be customized via the --xml-tag option)
Token delimiter:
  - n: newline
  - s: space
  - t: tab
Field delimiter:
  - s: space (only if not used as token delimiter)
  - t: tab (only if not used as token delimiter)
  - character used as delimiter, e.g. /
Sentence IDs:
  - c: comment on preceding line (default pattern: '^# sent_id = (.+)')
  - n: no sentence IDs
  - s: at the beginning of the line, separated by a space (only if token delimiter is space or tab)
  - t: at the beginning of the line, separated by a tab (only if token delimiter is space or tab)
  - x: XML attribute (only if sentence delimiter is XML; id-attribute by default; can be customized via the --xml-id option)
Token IDs:
  - n: no token IDs
  - zero-based field index containing the ID
Missing values:
  - e: empty string
  - n: no missing values (checks that there a no missing values)
  - character used for empty fields, e.g. _

"""



def arguments():
    parser = argparse.ArgumentParser(description="Convert a corpus from a given input format to the desired output format.")
    parser.add_argument("-i", "--input-format", choices=["conll", "osl", "tsv", "vrt"], required=True, help="Input format. conll: Tab-separated, one token per line with token id, empty line after sentences, empty fields marked with \"_\"; osl: One sentence per line, custom delimiter for annotation, tokens separated by space; tsv: Tab-separated, one token per line, empty line after sentences; vrt: Tab-separated, one token per line, sentences as s-tags")
    parser.add_argument("-o", "--output-format", choices=["conll", "osl", "tsv", "vrt"], required=True, help="Output format. See --input-format.")
    parser.add_argument("-d", "--delimiter", type=str, default="\t", help="Delimiter in osl format (default: \"\\t\".")
    parser.add_argument("-n", "--nfields", type=int, help="Number of fields in osl format (only for reading from osl).")
    parser.add_argument("FILE", type=argparse.FileType("r"), help="The input file")
    args = parser.parse_args()
    return args


def main():
    args = arguments()
    readers = {"conll": corpus_readers.read_conll,
               "osl": functools.partial(corpus_readers.read_osl, delimiter=args.delimiter, nr_of_fields=args.nfields),
               "tsv": corpus_readers.read_tsv,
               "vrt": corpus_readers.read_vrt}
    writers = {"conll": corpus_writers.write_conll,
               "osl": functools.partial(corpus_writers.write_osl, delimiter=args.delimiter),
               "tsv": corpus_writers.write_tsv,
               "vrt": corpus_writers.write_vrt}
    reader = readers[args.input_format]
    writer = writers[args.output_format]
    for line in writer(reader(args.FILE)):
        print(line)


if __name__ == "__main__":
    main()
