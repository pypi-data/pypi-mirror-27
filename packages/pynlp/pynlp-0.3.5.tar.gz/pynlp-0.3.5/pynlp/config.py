DEFAULT_PORT = 9000
DEFAULT_HOST = 'localhost'
ENV_NAME = 'CORE_NLP'
SERIALIZER_CLASS = 'edu.stanford.nlp.pipeline.ProtobufAnnotationSerializer'
SERVER_CLASS = 'edu.stanford.nlp.pipeline.StanfordCoreNLPServer'
DEFAULT_ANNOTATORS = 'tokenize, ssplit, pos, lemma, ner'