# CorpConv #

## Introduction ##

CorpConv is a tool for converting between some common corpus formats.


## Installation ##

CorpConv can be easily installed using pip:

    pip install CorpConv

Alternatively, you can download and decompress the [latest
release](https://github.com/tsproisl/CorpConv/releases/latest) or clone
the git repository:

    git clone https://github.com/tsproisl/CorpConv.git

In the new directory, run the following command:

    python3 setup.py install


## Usage ##

### Using the corpconv executable

You can use the converter as a standalone program from the command
line. General usage information is available via the -h option:

    corpconv -h

To convert a corpus from one format to another, call the converter like this:

    corpconv -i <input_format> -o <output_format> <file>

Supported formats are:
  * conll: Tab-separated, one token per line with token IDs, empty
    line after sentences, empty fields marked with an underscore
    (`_`), sentence IDs as leading comments (`# sent_id 5`)
	
	    # sent_id = 1
        1   They     they    PRON    PRP
        2   buy      buy     VERB    VBP
        3   and      and     CONJ    CC
        4   sell     sell    VERB    VBP
        5   books    book    NOUN    NNS
        6   .        .       PUNCT   .
	
  * osl: One sentence per line, custom delimiter for annotation, tokens separated by space
	
	    They/they/PRON/PRP buy/buy/VERB/VBP and/and/CONJ/CC sell/sell/VERB/VBP books/book/NOUN/NNS ././PUNCT/.
	
  * tsv: Tab-separated, one token per line, empty line after sentences
	
        They     they    PRON    PRP
        buy      buy     VERB    VBP
        and      and     CONJ    CC
        sell     sell    VERB    VBP
        books    book    NOUN    NNS
        .        .       PUNCT   .
	
  * vrt: Tab-separated, one token per line, sentences as s-tags
	
	    <s id="s1">
        They     they    PRON    PRP
        buy      buy     VERB    VBP
        and      and     CONJ    CC
        sell     sell    VERB    VBP
        books    book    NOUN    NNS
        .        .       PUNCT   .
		</s>


### Using the module ###

You can also use the readers and writers in your own Python projects.
Here is a small example for converting from osl to vrt:

    from corpconv import corpus_readers
	from corpconv import corpus_writers
	
	sentences = corpus_readers.read_osl(file_object)
	for line in corpus_writers.write_vrt(sentences):
	    print(line)

