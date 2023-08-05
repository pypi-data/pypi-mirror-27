from abc import ABC, abstractmethod


class Document:

    def __init__(self, proto_doc):
        self._doc = proto_doc

    def __str__(self):
        return self._doc.text

    def __len__(self):
        return self._doc.sentence[-1].token[-1].tokenEndIndex

    def __repr__(self):
        return '<{}: [sentences: {}, tokens: {}]>'.format(
            __class__.__name__,
            len(self._doc.sentence),
            self._doc.sentence[-1].token[-1].tokenEndIndex
        )

    def __getitem__(self, item):
        if isinstance(item, int) and item >= 0:
            return Sentence(self._doc, self._doc.sentence[item])

    def __eq__(self, other):
        return self._doc == other._doc

    @classmethod
    def from_bytes(cls, protobuf):
        raise NotImplementedError('Method under development') # todo

    def to_bytes(self):
        return NotImplementedError('Method under development') # todo

    @property
    def text(self):
        return self._doc.text

    @property
    def entities(self):
        for proto_mention in self._doc.mentions:
            yield NamedEntity(self._doc, proto_mention)

    @property
    def coref_chains(self):
        for proto_coref in self._doc.corefChain:
            yield CorefChain(self._doc, proto_coref)

    def coref_chain(self, chain_id):
        for proto_chain in self._doc.corefChain:
            if proto_chain.chainID == chain_id:
                return CorefChain(self._doc, proto_chain)
        raise IndexError('No CorefChain with id={} exits.'.format(chain_id))

    @property
    def quotes(self):
        for proto_quote in self._doc.quote:
            yield Quote(self._doc, proto_quote)


class Span(ABC):

    def __init__(self, proto_doc):
        self._doc = proto_doc

    @abstractmethod
    def __getitem__(self, item):
        pass


class Sentence(Span):

    def __init__(self, proto_doc, proto_sentence):
        super().__init__(proto_doc)
        self._sentence = proto_sentence

    def __str__(self):
        return ''.join([(t.originalText + t.after)
                        for t in self._sentence.token])

    def __len__(self):
        return len(self._sentence)

    def __repr__(self):
        return '<{} : [index: {}, tokens: {}]>'.format(
            __class__.__name__,
            self._sentence.sentenceIndex,
            self._sentence.token[-1].tokenEndIndex
        )

    def __eq__(self, other):
        return self._sentence == other._sentence and self._doc == other._doc

    def __getitem__(self, item):
        return Token(self._doc, self._sentence, self._sentence.token[item])

    @property
    def index(self):
        return self._sentence.sentenceIndex

    @property
    def tokens(self):
        for proto_token in self._sentence.token:
            yield Token(self._doc, self._sentence, proto_token)

    @property
    def entities(self):
        for proto_mention in self._sentence.mentions:
            yield NamedEntity(self._doc, proto_mention)

    @property
    def dependencies(self):
        basic_dep = self._sentence.basicDependencies
        return DependencyTree(self._doc, self._sentence, basic_dep)

    @property
    def e_dependencies(self):
        enhanced_dep = self._sentence.enhancedDependencies
        return DependencyTree(self._doc, self._sentence, enhanced_dep)

    @property
    def epp_dependencies(self):
        enhanced_dep_plusplus = self._sentence.enhancedPlusPlusDependencies
        return DependencyTree(self._doc, self._sentence, enhanced_dep_plusplus)

    @property
    def coref_mentions(self):
        # todo: implement this
        raise NotImplementedError('Method under development.')

    @property
    def sentiment(self):
        return self._sentence.sentiment

    @property
    def triples(self):
        for proto_triple in self._sentence.openieTriple:
            yield RelationTriple(self._doc, self._sentence, proto_triple)

    @property # parseTree, annotatedParseTree, binarizedParseTree
    def parse_tree(self):
        # todo: implement this (ParseTree class?)
        raise NotImplementedError('Method under development.')


class Token:

    def __init__(self, proto_doc, proto_sentence, proto_token):
        self._doc = proto_doc
        self._sentence = proto_sentence
        self._token = proto_token

    def __str__(self):
        return self._token.originalText

    def __repr__(self):
        return '<{}: [sentence: {}, index: {}]>'.format(
            __class__.__name__,
            self._sentence.sentenceIndex,
            self._token.beginIndex
        )

    def __eq__(self, other):
        return self._token == other._token and \
               self._sentence == other._sentence and \
               self._doc == other._doc

    def __hash__(self):  # this is not foolproof!
        return hash((self._token.originalText,
                     self._token.beginChar,
                     self._token.endChar))

    @property
    def word(self):
        return self._token.word

    @property
    def word_ws(self):
        return self._token.word + self._token.after

    @property
    def pos(self):
        return self._token.pos

    @property
    def ner(self):
        return self._token.ner

    @property
    def lemma(self):
        return self._token.lemma

    @property
    def sentence(self):
        return Sentence(self._doc, self._sentence)


class Root(Token):

    def __init__(self, proto_doc, proto_sentence):
        super().__init__(proto_doc, proto_sentence, None)

    def __eq__(self, other):
        return self._sentence == other._sentence and self._doc == other._doc

    def __hash__(self):
        return hash('ROOT')

    def __str__(self):
        return 'ROOT'

    def __repr__(self):
        return '<Token: [sentence: {}, index: ROOT]>'.format(
            self._sentence.sentenceIndex
        )

    @property
    def word(self):
        return 'ROOT'

    @property
    def word_ws(self):
        return 'ROOT'

    @property
    def pos(self):
        return 'ROOT'

    @property
    def ner(self):
        return 'ROOT'

    @property
    def lemma(self):
        return 'ROOT'


class NamedEntity(Span):

    def __init__(self, proto_doc, proto_mention):
        super().__init__(proto_doc)
        self._mention = proto_mention
        self._sentence = proto_doc.sentence[proto_mention.sentenceIndex]
        self._tokens = [token for token in self._sentence.token
                        if token.tokenBeginIndex >= self._mention.tokenStartInSentenceInclusive
                        and token.tokenEndIndex <= self._mention.tokenEndInSentenceExclusive]

    def __str__(self):
        return ' '.join([token.originalText for token in self._tokens])

    def __repr__(self):
        return '<{}: [type: {}, sentence: {}]>'.format(
            __class__.__name__,
            self._mention.entityType,
            self._sentence.sentenceIndex
        )

    def __getitem__(self, item):
        return Token(self._doc, self._sentence, self._tokens[item])

    @property
    def type(self):
        return self._mention.entityType

    @property
    def ner(self):
        return self._mention.ner

    @property
    def normalized_ner(self):
        return self._mention.normalizedNER


class CorefChain:

    def __init__(self, proto_doc, proto_coref):
        self._doc = proto_doc
        self._coref = proto_coref
        self._index = 0

    def __repr__(self):
        return '<{}: [chain_id: {}, length: {}]>'.format(
            __class__.__name__,
            self._coref.chainID,
            len(self._coref.mention)
        )

    def __str__(self):
        referent = self._coref.mention[self._coref.representative]
        references = {}
        for reference in self._coref.mention:
            references.setdefault(reference.sentenceIndex, []).append(reference)
        string = ''
        for sentence_index in sorted(references):
            words = []
            whitespace = []
            for token in self._doc.sentence[sentence_index].token:
                words.append(token.originalText)
                whitespace.append(token.after)
            for ref in sorted(references[sentence_index], key=lambda r: r.beginIndex):
                left_tag = '('
                right_tag = ')-[id={}]'.format(ref.mentionID)
                if ref.mentionID == referent.mentionID:
                    left_tag = '(' + left_tag
                    right_tag = ')' + right_tag
                words[ref.beginIndex] = left_tag + words[ref.beginIndex]
                words[ref.endIndex - 1] += right_tag

            for index, word in enumerate(words):
                string += word + whitespace[index]

            string += '\n'

        return string

    def __iter__(self):
        return self

    def __next__(self):
        try :
            i = self._index
            self._index += 1
            return Coreference(self._doc, self._coref, self._coref.mention[self._index])
        except IndexError:
            self._index = 0
            raise StopIteration

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise KeyError('Index by coref_id for coreference.')
        for proto_mention in self._coref.mention:
            if proto_mention.mentionID == item:
                return Coreference(self._doc, self._coref, proto_mention)
        raise KeyError('No coreference with id={} exits.'.format(item))

    @property
    def chain_id(self):
        return self._coref.chainID

    @property
    def referent(self):
        proto_coref_mention = self._coref.mention[self._coref.representative]
        return Coreference(self._doc, self._coref, proto_coref_mention)


class Coreference(Span):

    def __init__(self, proto_doc, proto_coref_chain, proto_coref_mention):
        super().__init__(proto_doc)
        self._coref_chain = proto_coref_chain
        self._coref_mention = proto_coref_mention
        sentence_index = proto_coref_mention.sentenceIndex
        self._tokens = [token for token in proto_doc.sentence[sentence_index].token
                        if token.beginIndex >= self._coref_mention.beginIndex
                        and token.endIndex <= self._coref_mention.endIndex]

    def __repr__(self):
        ref_id = self._coref_chain.mention[self._coref_chain.representative].mentionID
        return '<{}: [coref_id: {}, chain_id: {}, referent: {}]>'.format(
            self.__class__.__name__,
            self._coref_mention.mentionID,
            self._coref_chain.chainID,
            ref_id)

    def __str__(self):
        return ' '.join([token.originalText for token in self._tokens])

    def __getitem__(self, item):
        return Token(self._doc, self._doc.sentence[self._coref_mention.sentenceIndex],
                     self._tokens[item])

    def chain(self):
        return CorefChain(self._doc, self._coref_chain)

    @property
    def is_referent(self):
        referent_id = self._coref_chain.mention[self._coref_chain.representative].mentionID
        return self._coref_mention.mentionID == referent_id

    @property
    def coref_id(self):
        return self._coref_mention.mentionID

    @property
    def type(self):
        return self._coref_mention.mentionType

    @property
    def number(self):
        return self._coref_mention.number

    @property
    def gender(self):
        return self._coref_mention.gender

    @property
    def animacy(self):
        return self._coref_mention.animacy

    @property
    def head(self):
        return self._coref_mention.head


class Quote(Span):

    def __init__(self, proto_doc, proto_quote):
        super().__init__(proto_doc)
        self._quote = proto_quote

    def __repr__(self):
        return '<{}: {}>'.format(__class__.__name__, self._quote.text)

    def __str__(self):
        return self._quote.text

    def __getitem__(self, item):
        if 0 <= item <= self._quote.sentenceEnd - self._quote.sentenceBegin:
            return Sentence(self._doc,
                            self._doc.sentence[
                                self._quote.sentenceBegin + item
                            ])
        else:
            raise IndexError('Quote contains {} sentences.'.format(
                self._quote.sentenceEnd - self._quote.sentenceBegin + 1
            ))

    @property
    def text(self):
        return self._quote.text[1:-1]


class RelationTriple:

    def __init__(self, proto_doc, proto_sentence, proto_triple):
        self._doc = proto_doc
        self._sentence = proto_sentence
        self._triple = proto_triple

    def __str__(self):
        return '({})-[{}]->({})'.format(
            self._triple.subject,
            self._triple.relation,
            self._triple.object
        )

    def __len__(self):
        return len(self._triple.tree.node)

    def __repr__(self):
        return '<{}: [confidence: {}]>'.format(
            __class__.__name__,
            self._triple.confidence
        )

    @property
    def confidence(self):
        return self._triple.confidence

    @property
    def tree(self):
        raise NotImplementedError('Method under development.')
        assert self._triple.tree.root # todo: why are these sometimes missing?
        return DependencyTree(self._doc, self._sentence, self._triple.tree)

    @property
    def subject(self):
        for subj in self._triple.subjectTokens:
            yield Token(self._doc, self._sentence, self._sentence.token[subj.tokenIndex])

    @property
    def relation(self):
        for rel in self._triple.relationTokens:
            yield Token(self._doc, self._sentence, self._sentence.token[rel.tokenIndex])

    @property
    def object(self):
        for rel in self._triple.objectTokens:
            yield Token(self._doc, self._sentence, self._sentence.token[rel.tokenIndex])


class DependencyEdge:

    def __init__(self, dependency, gov_vertex, dep_vertex):
        self._dependency = dependency
        self._governor = gov_vertex
        self._dependent = dep_vertex

    def __str__(self):
        return '({})-[{}]->({})'.format(str(self._governor),
                                        self._dependency,
                                        str(self._dependent))

    @property
    def dependency(self):
        return self._dependency

    @property
    def governor(self):
        return self._governor

    @property
    def dependent(self):
        return self._dependent


class DependencyTree:

    def __init__(self, proto_doc, proto_sentence, proto_dependency):
        self._doc = proto_doc
        self._sentence = proto_sentence
        self._dependency = proto_dependency
        root = Root(self._doc, self._sentence)
        root_gov = proto_sentence.token[proto_dependency.root[0] - 1]
        root_dep = Token(self._doc, self._sentence, root_gov)
        self._governors = {root_dep: root}
        self._dependents = {}
        self._dependencies = {root_dep: '-ROOT-'}
        tokens = proto_sentence.token
        for proto_edge in proto_dependency.edge:
            source = Token(proto_doc, proto_sentence, tokens[proto_edge.source - 1])
            target = Token(proto_doc, proto_sentence, tokens[proto_edge.target - 1])
            self._governors[target] = source
            self._dependencies[target] = proto_edge.dep
            self._dependents.setdefault(source, []).append(target)
        for key in self._dependents:
            self._dependents[key] = frozenset(self._dependents[key])
        self._dependents[root] = [root_dep]
        self._root = root_dep

    def __repr__(self):
        return '<{}: [sentence: {}]>'.format(
            self.__class__.__name__,
            self._sentence.sentenceIndex
        )

    @property
    def root(self):
        return self._root

    def governor_of(self, token_vertex):
        return self._governors[token_vertex]

    def dependents_of(self, token_vertex):
        return self._dependents[token_vertex]

    def dependency(self, token_verex):
        return self._dependencies[token_verex]

    def dependencies(self, dependency):
        for target, dependency_ in self._dependencies.items():
            if dependency_ == dependency:
                yield DependencyEdge(dependency, self._governors[target], target)

    def siblings_of(self, token_vertex):
        return {vertex for vertex in self._dependents[self._governors[token_vertex]]
                if vertex != token_vertex}

    def is_ancestor(self, descendant, ancestor): # todo: TEST meh
        raise NotImplementedError('Method under development. ')
        parent = descendant
        while parent in self._governors:
            parent = self._governors[parent]
            if parent == ancestor:
                return True
        return False

    def common_ancestor(self, vertex1, vertex2): # todo: TEST meh
        raise NotImplementedError('Method under development. ')
        parent1 = vertex1
        parent2 = vertex2
        while parent2 in self._governors:
            while parent1 in self._governors:
                parent1 = self._governors[parent1]
                if parent1 == parent2:
                    return parent2
            parent2 = self._governors[parent2]
        return None

    @property
    def vertices(self):
        return [vertex for vertex in self._governors.keys()]

    @property
    def edges(self):
        return [DependencyEdge(self._dependencies[target], self._governors[target], target)
                for target in self._governors.keys()]



