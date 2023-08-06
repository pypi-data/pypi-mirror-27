class Grammar(object):
    def __init__(self):
        self.symbol_id = 0
        self.symbol_cache_terminal = {}
        self.rules_nonterminals = {}
        self.rules_terminals = {}
        self.rules_unit = {}

    def sym(self):
        self.symbol_id += 1
        return self.symbol_id

    def insert_rule_terminal(self, lsym, char):
        if lsym not in self.rules_terminals:
            self.rules_terminals[lsym] = set()
        self.rules_terminals[lsym].add(char)

    def insert_rule_nonterminal(self, lsym, rsym1, rsym2):
        if lsym not in self.rules_nonterminals:
            self.rules_nonterminals[lsym] = set()
        self.rules_nonterminals[lsym].add((rsym1, rsym2))

    def insert_rule_unit(self, lsym, rsym):
        if lsym not in self.rules_unit:
            self.rules_unit[lsym] = set()
        self.rules_unit[lsym].add(rsym)

    def get_string_symbol(self, s):
        """s is a non-empty string"""
        if s in self.symbol_cache_terminal:
            return self.symbol_cache_terminal[s]

        lsym = self.sym()
        if len(s) == 1:
            self.insert_rule_terminal(lsym, s)
        else:
            rsym1 = self.get_string_symbol(s[:1])
            rsym2 = self.get_string_symbol(s[1:])
            self.insert_rule_nonterminal(lsym, rsym1, rsym2)
        self.symbol_cache_terminal[s] = lsym
        return lsym

    def get_symbol(self, rhs):
        if type(rhs) == int:
            return rhs
        elif type(rhs) == str:
            return self.get_string_symbol(rhs)
        elif type(rhs) == tuple:
            lsym = self.sym()
            rsym1 = self.get_symbol(rhs[0])
            rsym2 = self.get_symbol(rhs[1])
            self.insert_rule_nonterminal(lsym, rsym1, rsym2)
            return lsym

    def get_wildcard_character_symbol(self, alphabet):
        lsym = self.sym()
        for char in alphabet:
            self.insert_rule_terminal(lsym, char)
        return lsym

    def insert_rule(self, lsym, rhs):
        rsym = self.get_symbol(rhs)
        self.insert_rule_unit(lsym, rsym)


class EsperantoGrammar(Grammar):
    def __init__(self, dwords=None, dstubs=None):
        super(EsperantoGrammar, self).__init__()

        self.WORD = self.sym()  # Start symbol

        # Terminals
        self.PREFIX = self.sym()
        self.SUFFIX = self.sym()

        self.WILDCARD_1 = self.sym()
        self.WILDCARD_N = self.sym()

        self.DSTUB = self.sym()
        self.DWORD = self.sym()

        self.STUB = self.sym()  # A part of the word without ending

        self.NOUN_SING = self.sym()  # -o
        self.NOUN_SING_ACC = self.sym()  # -on
        self.NOUN_PLUR = self.sym()  # -oj
        self.NOUN_PLUR_ACC = self.sym()  # -ojn

        self.ADJ_SING = self.sym()  # -a
        self.ADJ_SING_ACC = self.sym()  # -an
        self.ADJ_PLUR = self.sym()  # -aj
        self.ADJ_PLUR_ACC = self.sym()  # -ajn
        self.ADVERB = self.sym()  # -e
        self.VERB_INF = self.sym()  # -i
        self.VERB_PAST = self.sym()  # -is
        self.VERB_PRES = self.sym()  # -as
        self.VERB_FUT = self.sym()  # -os
        self.VERB_JUS = self.sym()  # -u
        self.VERB_COND = self.sym()  # -us

        rules = []

        if dwords is None and dstubs is None:
            for char in 'abcĉdefgĝhĥijĵklmnoprsŝtuŭvz':
                rules.append((self.WILDCARD_1, char))

            rules.extend([
                (self.WILDCARD_N, self.WILDCARD_1),
                (self.WILDCARD_N, (self.WILDCARD_1, self.WILDCARD_N)),
                # 2 character minimum
                (self.DSTUB, (self.WILDCARD_1, self.WILDCARD_N)),
                (self.DWORD, (self.WILDCARD_1, self.WILDCARD_N)),
            ])
        else:
            for dstub in dstubs:
                rules.append((self.DSTUB, dstub))
            for dword in dwords:
                rules.append((self.DWORD, dword))

        for p in PREFIXES.keys():
            rules.append((self.PREFIX, p))

        for s in SUFFIXES.keys():
            rules.append((self.SUFFIX, s))

        rules.extend([
            (self.STUB, self.DSTUB),
            (self.STUB, (self.STUB, self.SUFFIX)),
            (self.STUB, (self.PREFIX, self.STUB)),
            # Compound words
            (self.STUB, (self.STUB, self.STUB)),
            (self.STUB, (self.NOUN_SING, self.STUB)),
            (self.STUB, (self.NOUN_SING_ACC, self.STUB)),
            (self.STUB, (self.VERB_INF, self.STUB)),

            (self.NOUN_SING, (self.STUB, 'o')),
            (self.NOUN_SING_ACC, (self.NOUN_SING, 'n')),
            (self.NOUN_PLUR, (self.NOUN_SING, 'j')),
            (self.NOUN_PLUR_ACC, (self.NOUN_PLUR, 'n')),
            (self.ADJ_SING, (self.STUB, 'a')),
            (self.ADJ_SING_ACC, (self.ADJ_SING, 'n')),
            (self.ADJ_PLUR, (self.ADJ_SING, 'j')),
            (self.ADJ_PLUR_ACC, (self.ADJ_PLUR, 'n')),
            (self.ADVERB, (self.STUB, 'e')),
            (self.VERB_INF, (self.STUB, 'i')),
            (self.VERB_PAST, (self.STUB, 'is')),
            (self.VERB_PRES, (self.STUB, 'as')),
            (self.VERB_FUT, (self.STUB, 'os')),
            (self.VERB_JUS, (self.STUB, 'u')),
            (self.VERB_COND, (self.STUB, 'us')),

            (self.WORD, self.DWORD),
            (self.WORD, (self.STUB, self.DWORD)),
            (self.WORD, self.NOUN_SING),
            (self.WORD, self.NOUN_SING_ACC),
            (self.WORD, self.NOUN_PLUR),
            (self.WORD, self.NOUN_PLUR_ACC),
            (self.WORD, self.ADJ_SING),
            (self.WORD, self.ADJ_SING_ACC),
            (self.WORD, self.ADJ_PLUR),
            (self.WORD, self.ADJ_PLUR_ACC),
            (self.WORD, self.ADVERB),
            (self.WORD, self.VERB_INF),
            (self.WORD, self.VERB_PAST),
            (self.WORD, self.VERB_PRES),
            (self.WORD, self.VERB_FUT),
            (self.WORD, self.VERB_JUS),
            (self.WORD, self.VERB_COND)
        ])

        for l, r in rules:
            self.insert_rule(l, r)


class Parser(object):
    def __init__(self, grammar):
        self.cache = {}
        self.grammar = grammar

    def get_parse_forest(self, sym, text):
        k = (sym, text)
        if k in self.cache:
            return self.cache[k]

        ret = []
        if len(text) == 1:
            if sym in self.grammar.rules_terminals:
                if text in self.grammar.rules_terminals[sym]:
                    ret.append((sym, text))

        if sym in self.grammar.rules_unit:
            for rhs in self.grammar.rules_unit[sym]:
                subforest = self.get_parse_forest(rhs, text)
                if subforest is not None:
                    ret.append((sym, subforest))

        if len(text) > 1:
            if sym in self.grammar.rules_nonterminals:
                for rhs in self.grammar.rules_nonterminals[sym]:
                    for i in range(1, len(text)):
                        subforest1 = self.get_parse_forest(rhs[0], text[:i])
                        if subforest1 is not None:
                            subforest2 = self.get_parse_forest(rhs[1], text[i:])
                            if subforest2 is not None:
                                ret.append((sym, subforest1, subforest2))

        if len(ret) == 0:
            ret = None

        self.cache[k] = ret
        return ret


# Prefixes and suffixes taken from Fundamento de Esperanto


PREFIXES = {
    "kun": "with",
    "ge": "of both sexes; e. g. patr' father ― ge'patr'o'j parents",
    "dis": "has the same force as the English prefix dis; e. g. sem' sow ― dis'sem' disseminate; ŝir' tear ― dis'ŝir' tear to pieces",
    "ek": "denotes sudden or momentary action; e. g. kri' cry ― ek'kri' cry out",
    "bo": "relation by marriage; e. g. patr'in' mother ― bo'patr'in' mother-in-law",
    "\u0109ef": "chief",
    "mal": "denotes opposites; e. g. alt' high ― mal'alt' low",
    "eks": "ex-, late",
    "re": "again, back",
    "pra": "primordial, great-"
}

SUFFIXES = {
    "ar": "a collection of objects; e. g. vort' word ― vort'ar' dictionary",
    "ad": "denotes duration of action; e. g. danc' dance ― danc'ad' dancing",
    "estr": "chief, boss; e.g. ŝip' ship ― ŝip'estr' captain",
    "nj": "diminutive of female names; e. g. Henriet' Henrietta ― Henri'nj', He'nj' Hetty",
    "ind": "worth",
    "\u0109j": "affectionate diminutive of masculine names; e.g. Johan' John ― Jo'ĉj' Johnnie",
    "ec": "denotes qualites; e. g. bon' good ― bon'ec' goodness",
    "il": "instrument; e. g. tond' shear ― tond'il' scissors",
    "ig": "to cause to be; e. g. pur' pure ― pur'ig' purify",
    "i\u011d": "to become; e. g. ruĝ' red ― ruĝ'iĝ' blush",
    "er": "one of many objects of the same kind; e. g. sabl' sand ― sabl'er' grain of sand",
    "on": "marks fractions; e. g. kvar four ― kvar'on' a fourth, quarter",
    "em": "inclined to; e. g. babil' chatter ― babil'em' talkative",
    "obl": "...fold; e. g. du two ― du'obl' twofold, duplex",
    "ebl": "able, possible",
    "an": "inhabitant, member; e. g. Nov-Jork New York ― Nov-Jork'an' New Yorker",
    "ist": "person occupied with; e. g. mar' sea ― mar'ist' sailor",
    "um": "this syllable has no fixed meaning",
    "op": "marks collective numerals; e. g. tri three ― tri'op' three together",
    "et": "denotes diminution of degree; e. g. rid' laugh ― rid'et' smile",
    "in": "ending of feminine words; e. g. bov' ox ― bov'in' cow",
    "a\u0135": "made from or possessing the quality of; e. g. sek' dry ― sek'aĵ' dry goods",
    "ing": "holder for; e. g. kandel' candle ― kandel'ing' candlestick",
    "eg": "denotes increase of degree; e. g, varm' warm ― varm'eg' hot",
    "uj": "filled with; e. g. ink' ink ― ink'uj' ink-pot; pom' apple ― pom'uj' apple-tree; Turk'uj' Turkey",
    "ej": "place where an action occurs; e. g. kuir' cook ― kuir'ej' kitchen",
    "id": "descendant, young one; e. g. bov' ox ― bov'id' calf"
}

# Not found in Fundamento
PREFIXES['sen'] = 'without'


def list_parse_trees(forest):
    if type(forest) is list:
        for subtree in forest:
            yield from list_parse_trees(subtree)
    elif type(forest) is tuple:
        sym = forest[0]
        if len(forest) == 2:
            if type(forest[1]) is str:
                yield forest
            else:
                for t in list_parse_trees(forest[1]):
                    yield (sym, t)
        else:
            for t1 in list_parse_trees(forest[1]):
                for t2 in list_parse_trees(forest[2]):
                    yield (sym, t1, t2)


def collapse_parse_tree(tree):
    if len(tree) == 2:
        if type(tree[1]) is str:
            return tree[1]
        else:
            return collapse_parse_tree(tree[1])
    else:
        text = ''
        text += collapse_parse_tree(tree[1])
        text += collapse_parse_tree(tree[2])
        return text


def list_matching_subtrees(tree, match_symbols):
    if tree[0] in match_symbols:
        yield tree
    elif len(tree) == 2 and type(tree[1]) is not str:
        yield from list_matching_subtrees(tree[1], match_symbols)
    elif len(tree) == 3:
        yield from list_matching_subtrees(tree[1], match_symbols)
        yield from list_matching_subtrees(tree[2], match_symbols)


def extract_wildcards(word):
    grammar = EsperantoGrammar()
    parser = Parser(grammar)
    forest = parser.get_parse_forest(grammar.WORD, word)
    dstubs = set()
    dwords = set()
    for tree in list_parse_trees(forest):
        for subtree in list_matching_subtrees(tree, {grammar.DSTUB}):
            dstubs.add(collapse_parse_tree(subtree))
        for subtree in list_matching_subtrees(tree, {grammar.DWORD}):
            dwords.add(collapse_parse_tree(subtree))
    return dwords, dstubs


def list_chains(forest, symbols):
    for tree in list_parse_trees(forest):
        chain = []
        for subtree in list_matching_subtrees(tree, symbols):
            chain.append((subtree[0], collapse_parse_tree(subtree)))
        yield chain


def normalize_word(word):
    # Poetic omission of the ending
    if word.endswith("'"):
        word = word[:-1] + 'o'

    word = word.lower()
    return word


class Lookup(object):
    def __init__(self, content):
        self.content = content

    def lookup(self, word):
        ordered_definitions = []
        word = normalize_word(word)
        dwords, dstubs = extract_wildcards(word)

        if dwords or dstubs:

            dword_queries = set(dwords)
            dstub_queries = set()

            for dstub in dstubs:
                for e in ['a', 'o', 'e', 'i']:
                    q = dstub + e
                    dstub_queries.add(q)

            queries = dword_queries | dstub_queries

            resolved_dwords = {}
            resolved_dstubs = {}

            definitions = {}
            dstubs_to_dwords = {}

            for eo in queries:
                if eo not in self.content:
                    continue

                definition = self.content[eo]
                definitions[eo] = definition

                if eo in dword_queries:
                    resolved_dwords[eo] = definition
                if eo in dstub_queries:
                    dstubs_to_dwords[eo[:-1]] = eo
                    resolved_dstubs[eo[:-1]] = definition

            grammar_step2 = EsperantoGrammar(
                dstubs=set(resolved_dstubs.keys()),
                dwords=set(resolved_dwords.keys()))

            parser = Parser(grammar_step2)
            forest = parser.get_parse_forest(grammar_step2.WORD, word)

            chains = list(list_chains(forest,
                                      {grammar_step2.PREFIX,
                                       grammar_step2.SUFFIX,
                                       grammar_step2.DWORD,
                                       grammar_step2.DSTUB}))

            if chains:
                chains_lengths = list(map(len, chains))
                shortest_len = min(chains_lengths)
                shortest_chain = []
                for i in range(len(chains)):
                    if chains_lengths[i] == shortest_len:
                        shortest_chain.append(chains[i])

                chain = sorted(shortest_chain)[0]

                for symbol, text in chain:
                    if symbol is grammar_step2.PREFIX:
                        ordered_definitions.append((text + '-', PREFIXES[text].strip().split('|')))
                    elif symbol is grammar_step2.SUFFIX:
                        ordered_definitions.append(('-' + text, SUFFIXES[text].strip().split('|')))
                    elif symbol is grammar_step2.DWORD:
                        ordered_definitions.append((text, definitions[text]))
                    elif symbol is grammar_step2.DSTUB:
                        dword = dstubs_to_dwords[text]
                        ordered_definitions.append((dword, definitions[dword]))

        return ordered_definitions

    def lookup_html(self, word):
        ordered_definitions = self.lookup(word)
        text = ''
        if ordered_definitions:
            for eo, ens in ordered_definitions:
                definition = ', '.join(ens).strip()
                text += '<strong>%s</strong>: %s, ' % (eo, definition)
            text = text[:-2]
        else:
            text = 'Sorry, not found.'

        return text
