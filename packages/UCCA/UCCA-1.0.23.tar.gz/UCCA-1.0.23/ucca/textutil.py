"""Utility functions for UCCA package."""
import os
from itertools import groupby
from operator import attrgetter

import numpy as np
from tqdm import tqdm

from ucca import layer0, layer1


def nlp(*args, lang="en", **kwargs):
    return get_nlp(lang)(*args, **kwargs)


MODEL_ENV_VAR = "SPACY_MODEL"
DEFAULT_MODEL = {"en": "en_core_web_md", "fr": "fr_core_news_md", "de": "de_core_news_sm"}


def get_nlp(lang="en"):
    instance = nlp.instance.get(lang)
    if instance is None:
        import spacy
        model_name = os.environ.get(MODEL_ENV_VAR + "_" + lang.upper(), os.environ.get(MODEL_ENV_VAR,
                                                                                       DEFAULT_MODEL.get(lang, "xx")))
        try:
            nlp.instance[lang] = instance = spacy.load(model_name)
        except OSError:
            spacy.cli.download(None, model_name)
            try:
                nlp.instance[lang] = instance = spacy.load(model_name)
            except OSError as e:
                raise OSError("Failed to get spaCy model. Download it manually using "
                              "`python -m spacy download %s`." % model_name) from e
        nlp.tokenizer[lang] = instance.tokenizer
        instance.tokenizer = lambda words: spacy.tokens.Doc(instance.vocab, words=words)
    return instance


nlp.instance = {}
nlp.tokenizer = {}


def get_tokenizer(tokenized=False, lang="en"):
    instance = get_nlp(lang)
    return instance.tokenizer if tokenized else nlp.tokenizer[lang]


def get_word_vectors(dim=None, size=None, filename=None, lang="en"):
    vocab = get_nlp(lang).vocab
    if filename is not None:
        print("Loading word vectors from '%s'..." % filename)
        it = read_word_vectors(dim, size, filename)
        nr_row, nr_dim = next(it)
        i = 0
        if nr_row is None:
            vocab.reset_vectors(width=nr_dim)
        else:
            vocab.reset_vectors(shape=(nr_row, nr_dim))
        for word, vector in tqdm(it, total=nr_row, unit=" vectors", leave=False, mininterval=3):
            vocab_word = vocab[word]
            if not vocab_word.has_vector:
                vocab.set_vector(vocab_word.orth, np.asarray(vector[:nr_dim], dtype="f"))
                if vocab_word.has_vector:
                    i += 1
                    if nr_row and i >= nr_row:
                        break
    # elif dim is not None:  # Disabled due to explosion/spaCy#1518
    #     nr_row, nr_dim = vocab.vectors.shape
    #     if dim < nr_dim:
    #         vocab.vectors.resize(shape=(int(size or nr_row), int(dim)))
    lexemes = sorted([l for l in vocab if l.has_vector], key=attrgetter("prob"), reverse=True)[:size]
    return {l.orth_: l.vector for l in lexemes}, vocab.vectors_length


def read_word_vectors(dim, size, filename):
    try:
        first_line = True
        nr_row = nr_dim = None
        with open(filename, encoding="utf-8") as f:
            for line in f:
                fields = line.split()
                if first_line:
                    first_line = False
                    try:
                        nr_row, nr_dim = map(int, fields)
                        is_header = True
                    except ValueError:
                        nr_dim = len(fields) - 1  # No header, just get vector length from first one
                        is_header = False
                    if dim and dim < nr_dim:
                        nr_dim = dim
                    yield size or nr_row, nr_dim
                    if is_header:
                        continue  # Read next line
                word, *vector = fields
                if len(vector) >= nr_dim:  # May not be equal if word is whitespace
                    yield word, np.asarray(vector[-nr_dim:], dtype="f")
    except OSError as e:
        raise IOError("Failed loading word vectors from '%s'" % filename) from e


TAG_KEY = "tag"  # fine-grained POS tag
POS_KEY = "pos"  # coarse-grained POS tag
NER_KEY = "ner"  # named entity type
IOB_KEY = "iob"  # integer named entity IOB tag (0: unknown, 1: I, 2: O, 3: B)
DEP_KEY = "dep"  # dependency relation to syntactic head
HEAD_KEY = "head"  # integer position of syntactic head within paragraph (para_pos)
LEMMA_KEY = "lemma"
ANNOTATION_KEYS = (TAG_KEY, POS_KEY, NER_KEY, IOB_KEY, DEP_KEY, HEAD_KEY, LEMMA_KEY)


def annotate(passage, verbose=False, replace=False, lang="en"):
    """
    POS tag the tokens in the given passage and parse with a dependency parser
    :param passage: Passage whose layer 0 nodes will be added these entries in the extra dict: tag, pos, dep, head
    :param verbose: whether to print annotated text
    :param replace: even if given passage is already annotated, replace with new annotation
    :param lang: optional two-letter language code
    :return: list of annotated terminal nodes
    """
    l0 = passage.layer(layer0.LAYER_ID)
    paragraphs = [sorted(p, key=attrgetter("position")) for _, p in groupby(l0.all, key=attrgetter("paragraph"))]
    if replace or any(k not in t.extra for p in paragraphs for t in p for k in ANNOTATION_KEYS):
        for p in paragraphs:
            annotated = nlp([t.text for t in p], lang=lang)
            for terminal, lex in zip(p, annotated):
                terminal.extra[TAG_KEY] = lex.tag_
                terminal.extra[POS_KEY] = lex.pos_
                terminal.extra[NER_KEY] = lex.ent_type_
                terminal.extra[IOB_KEY] = str(lex.ent_iob)
                terminal.extra[DEP_KEY] = lex.dep_
                terminal.extra[HEAD_KEY] = str(lex.head.i + 1)
                terminal.extra[LEMMA_KEY] = lex.lemma_
    if verbose:
        for p in paragraphs:
            extra = [["text"] + list(ANNOTATION_KEYS)] + [[t.text] + [t.extra[k] for k in ANNOTATION_KEYS] for t in p]
            width = [max(len(f) for f in t) for t in extra]
            for i in range(1 + len(ANNOTATION_KEYS)):
                print(" ".join("%-*s" % (w, f[i]) for f, w in zip(extra, width)))
            print()


SENTENCE_END_MARKS = ('.', '?', '!')


def break2sentences(passage, lang="en"):
    """
    Breaks paragraphs into sentences according to the annotation.

    A sentence is a list of terminals which ends with a mark from
    SENTENCE_END_MARKS, and is also the end of a paragraph or parallel scene.
    :param passage: the Passage object to operate on
    :param lang: optional two-letter language code
    :return: a list of positions in the Passage, each denotes a closing Terminal of a sentence.
    """
    l1 = passage.layer(layer1.LAYER_ID)
    terminals = extract_terminals(passage)
    if any(n.outgoing for n in l1.all):  # Passage is labeled
        ps_ends = [ps.end_position for ps in l1.top_scenes]
        ps_starts = [ps.start_position for ps in l1.top_scenes]
        marks = [t.position for t in terminals if t.text in SENTENCE_END_MARKS]
        # Annotations doesn't always include the ending period (or other mark)
        # with the parallel scene it closes. Hence, if the terminal before the
        # mark closed the parallel scene, and this mark doesn't open a scene
        # in any way (hence it probably just "hangs" there), it's a sentence end
        marks = [x for x in marks if x in ps_ends or ((x - 1) in ps_ends and x not in ps_starts)]
    else:  # Not labeled, split using spaCy
        annotated = nlp([t.text for t in terminals], lang=lang)
        marks = [span.end for span in annotated.sents]
    marks = sorted(set(marks + break2paragraphs(passage)))
    # Avoid punctuation-only sentences
    if len(marks) > 1:
        marks = [x for x, y in zip(marks[:-1], marks[1:])
                 if not all(layer0.is_punct(t) for t in terminals[x:y])] +\
                [marks[-1]]
    return marks


def extract_terminals(p):
    """returns an iterator of the terminals of the passage p"""
    return p.layer(layer0.LAYER_ID).all


def break2paragraphs(passage):
    """
    Breaks into paragraphs according to the annotation.

    Uses the `paragraph' attribute of layer 0 to find paragraphs.
    :param passage: the Passage object to operate on
    :return: a list of positions in the Passage, each denotes a closing Terminal
        of a paragraph.
    """
    terminals = list(extract_terminals(passage))
    paragraph_ends = [(t.position - 1) for t in terminals
                      if t.position != 1 and t.para_pos == 1]
    paragraph_ends.append(terminals[-1].position)
    return paragraph_ends


def indent_xml(xml_as_string):
    """
    Indents a string of XML-like objects.

    This works only for units with no text or tail members, and only for
    strings whose leaves are written as <tag /> and not <tag></tag>.
    :param xml_as_string: XML string to indent
    :return: indented XML string
    """
    tabs = 0
    lines = str(xml_as_string).replace('><', '>\n<').splitlines()
    s = ''
    for line in lines:
        if line.startswith('</'):
            tabs -= 1
        s += ("  " * tabs) + line + '\n'
        if not (line.endswith('/>') or line.startswith('</')):
            tabs += 1
    return s
