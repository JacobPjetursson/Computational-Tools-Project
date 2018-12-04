from gensim.models.doc2vec import Doc2Vec


def load_model(path):
    model = Doc2Vec.load(path)
    print("Model loaded")
    return model

def get_model_vectors(path):
    model = load_model(path)
    vectors = model.docvecs
    print("Amount of vectors: %s" % len(vectors))
    return vectors
