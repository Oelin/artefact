from elasticsearch_dsl import Document, Text, DenseVector


class Artefact(Document):

	sentence = Text()
	sentence_embedding = DenseVector(dims=300)

	class Index:
		name = 'artefacts'


models = (
	Artefact,
)
