#!/usr/bin/env python3

import collections
import functools
import unittest

from corpconv import corpus_readers
from corpconv import corpus_writers


Sentence = collections.namedtuple("Sentence", ["id", "tokens"])

sentences = [Sentence(id='s1',
                      tokens=[
                          ['They', 'they', 'PRON', 'PRP', 'Case=Nom|Number=Plur', '2', 'nsubj', '2:nsubj|4:nsubj', ''],
                          ['buy', 'buy', 'VERB', 'VBP', 'Number=Plur|Person=3|Tense=Pres', '0', 'root', '0:root', ''],
                          ['and', 'and', 'CONJ', 'CC', '', '4', 'cc', '4:cc', ''],
                          ['sell', 'sell', 'VERB', 'VBP', 'Number=Plur|Person=3|Tense=Pres', '2', 'conj', '0:root|2:conj', ''],
                          ['books', 'book', 'NOUN', 'NNS', 'Number=Plur', '2', 'obj', '2:obj|4:obj', 'SpaceAfter=No'],
                          ['.', '.', 'PUNCT', '.', '', '2', 'punct', '2:punct', '']]),
             Sentence(id='s2',
                      tokens=[
                          ['I', 'I', 'PRON', 'PRP', 'Case=Nom|Number=Sing|Person=1', '2', 'nsubj', '', ''],
                          ['have', 'have', 'VERB', 'VBP', 'Number=Sing|Person=1|Tense=Pres', '0', 'root', '', ''],
                          ['no', 'no', 'DET', 'DT', 'PronType=Neg', '4', 'det', '', ''],
                          ['clue', 'clue', 'NOUN', 'NN', 'Number=Sing', '2', 'obj', '', 'SpaceAfter=No'],
                          ['.', '.', 'PUNCT', '.', '', '2', 'punct', '', '']])]


class TestConllReader(unittest.TestCase):
    def test_conll_reader_01(self):
        corpus_conll = """# sent_id = s1
# text = They buy and sell books.
1\tThey\tthey\tPRON\tPRP\tCase=Nom|Number=Plur\t2\tnsubj\t2:nsubj|4:nsubj\t_
2\tbuy\tbuy\tVERB\tVBP\tNumber=Plur|Person=3|Tense=Pres\t0\troot\t0:root\t_
3\tand\tand\tCONJ\tCC\t_\t4\tcc\t4:cc\t_
4\tsell\tsell\tVERB\tVBP\tNumber=Plur|Person=3|Tense=Pres\t2\tconj\t0:root|2:conj\t_
5\tbooks\tbook\tNOUN\tNNS\tNumber=Plur\t2\tobj\t2:obj|4:obj\tSpaceAfter=No
6\t.\t.\tPUNCT\t.\t_\t2\tpunct\t2:punct\t_

# sent_id = s2
# text = I have no clue.
1\tI\tI\tPRON\tPRP\tCase=Nom|Number=Sing|Person=1\t2\tnsubj\t_\t_
2\thave\thave\tVERB\tVBP\tNumber=Sing|Person=1|Tense=Pres\t0\troot\t_\t_
3\tno\tno\tDET\tDT\tPronType=Neg\t4\tdet\t_\t_
4\tclue\tclue\tNOUN\tNN\tNumber=Sing\t2\tobj\t_\tSpaceAfter=No
5\t.\t.\tPUNCT\t.\t_\t2\tpunct\t_\t_

""".splitlines()
        self.assertEqual(list(corpus_readers.read_conll(corpus_conll)), sentences)


class TestOslReader(unittest.TestCase):
    def test_osl_reader_01(self):
        corpus_osl = """They_they_PRON_PRP_Case=Nom|Number=Plur_2_nsubj_2:nsubj|4:nsubj_ buy_buy_VERB_VBP_Number=Plur|Person=3|Tense=Pres_0_root_0:root_ and_and_CONJ_CC__4_cc_4:cc_ sell_sell_VERB_VBP_Number=Plur|Person=3|Tense=Pres_2_conj_0:root|2:conj_ books_book_NOUN_NNS_Number=Plur_2_obj_2:obj|4:obj_SpaceAfter=No ._._PUNCT_.__2_punct_2:punct_
I_I_PRON_PRP_Case=Nom|Number=Sing|Person=1_2_nsubj__ have_have_VERB_VBP_Number=Sing|Person=1|Tense=Pres_0_root__ no_no_DET_DT_PronType=Neg_4_det__ clue_clue_NOUN_NN_Number=Sing_2_obj__SpaceAfter=No ._._PUNCT_.__2_punct__""".splitlines()
        self.assertEqual(list(corpus_readers.read_osl(corpus_osl, delimiter="_", nr_of_fields=10)), sentences)


class TestTsvReader(unittest.TestCase):
    def test_tsv_reader_01(self):
        corpus_tsv = """They\tthey\tPRON\tPRP\tCase=Nom|Number=Plur\t2\tnsubj\t2:nsubj|4:nsubj\t
buy\tbuy\tVERB\tVBP\tNumber=Plur|Person=3|Tense=Pres\t0\troot\t0:root\t
and\tand\tCONJ\tCC\t\t4\tcc\t4:cc\t
sell\tsell\tVERB\tVBP\tNumber=Plur|Person=3|Tense=Pres\t2\tconj\t0:root|2:conj\t
books\tbook\tNOUN\tNNS\tNumber=Plur\t2\tobj\t2:obj|4:obj\tSpaceAfter=No
.\t.\tPUNCT\t.\t\t2\tpunct\t2:punct\t

I\tI\tPRON\tPRP\tCase=Nom|Number=Sing|Person=1\t2\tnsubj\t\t
have\thave\tVERB\tVBP\tNumber=Sing|Person=1|Tense=Pres\t0\troot\t\t
no\tno\tDET\tDT\tPronType=Neg\t4\tdet\t\t
clue\tclue\tNOUN\tNN\tNumber=Sing\t2\tobj\t\tSpaceAfter=No
.\t.\tPUNCT\t.\t\t2\tpunct\t\t

""".splitlines()
        self.assertEqual(list(corpus_readers.read_tsv(corpus_tsv)), sentences)


class TestVrtReader(unittest.TestCase):
    def test_vrt_reader_01(self):
        corpus_vrt = """<s id="s1">
They\tthey\tPRON\tPRP\tCase=Nom|Number=Plur\t2\tnsubj\t2:nsubj|4:nsubj\t
buy\tbuy\tVERB\tVBP\tNumber=Plur|Person=3|Tense=Pres\t0\troot\t0:root\t
and\tand\tCONJ\tCC\t\t4\tcc\t4:cc\t
sell\tsell\tVERB\tVBP\tNumber=Plur|Person=3|Tense=Pres\t2\tconj\t0:root|2:conj\t
books\tbook\tNOUN\tNNS\tNumber=Plur\t2\tobj\t2:obj|4:obj\tSpaceAfter=No
.\t.\tPUNCT\t.\t\t2\tpunct\t2:punct\t
</s>
<s id="s2">
I\tI\tPRON\tPRP\tCase=Nom|Number=Sing|Person=1\t2\tnsubj\t\t
have\thave\tVERB\tVBP\tNumber=Sing|Person=1|Tense=Pres\t0\troot\t\t
no\tno\tDET\tDT\tPronType=Neg\t4\tdet\t\t
clue\tclue\tNOUN\tNN\tNumber=Sing\t2\tobj\t\tSpaceAfter=No
.\t.\tPUNCT\t.\t\t2\tpunct\t\t
</s>
""".splitlines()
        self.assertEqual(list(corpus_readers.read_vrt(corpus_vrt)), sentences)


class TestAll(unittest.TestCase):
    def test_all_01(self):
        readers = {"conll": corpus_readers.read_conll,
                   "osl": functools.partial(corpus_readers.read_osl, delimiter="_", nr_of_fields=10),
                   "tsv": corpus_readers.read_tsv,
                   "vrt": corpus_readers.read_vrt}
        writers = {"conll": corpus_writers.write_conll,
                   "osl": functools.partial(corpus_writers.write_osl, delimiter="_"),
                   "tsv": corpus_writers.write_tsv,
                   "vrt": corpus_writers.write_vrt}
        for fmt in readers.keys():
            self.assertEqual(list(readers[fmt](writers[fmt](sentences))), sentences)
