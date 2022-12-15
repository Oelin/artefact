from os import environ
from dotenv import load_dotenv
from flask import Flask
from elasticsearch import Elasticsearch
from elasticsearch_dsl import connections, Search
from diffusers import StableDiffusionPipeline
from sentence_transformers import SentenceTransformer
from . models import models, Artefact


# Import environment variables...

load_dotenv()


# Initialize Flask app...

app = Flask(__name__)


# Initialize ElasticSearch client...

es = Elasticsearch(
        cloud_id = environ['ELASTIC_CLOUD_ID'],
        basic_auth=(
		environ['ELASTIC_USERNAME'], 
		environ['ELASTIC_PASSWORD'],
	),
)

connections.add_connection('default', es)
search = Search(using=es)


# Initialize ElasticSearch models...

for model in models: model.init()


# Initialize ML pipelines...

import torch

sentence_to_embedding = SentenceTransformer('all-MiniLM-L6-v2')
sentence_to_image = StableDiffusionPipeline.from_pretrained('runwayml/stable-diffusion-v1-5', torch_type=torch.float16)
sentence_to_image = sentence_to_image.to('cuda') if torch.cuda_is_available() else sentence_to_image


# Define app routes...

@app.route('/generate')
def generate():
	return 'hello generate'

	sentence = request.args.get('sentence')
	sentence_embedding = sentence_to_embedding.encode(sentence, convert_to_tensor=True)
	#image = sentence_to_image(sentence).images[0]

	return str(sentence_embedding)
	#artefact = Artefact(sentence, sentence_embedding)
	#artefact.save()

	# get ID of artefact
	#return id

	# plan:
	# generate image using stable diffusion
	# get description embedding
	# create Artefact(sentence, sentence_embedding)
	# save to cluster
	# get ID of artefact
	# upload image to static directory with filename determined entirely by ID.
	# return URL or ID.


@app.route('/search')
def search():
	return 'hello search'

	# create embedding of sentence
	# sort items in cluster by cosine similarity. Use pagination.
	# return results (artefact IDs + sentences)



print(es.info())
