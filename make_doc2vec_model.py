from gensim.corpora.wikicorpus import WikiCorpus
import multiprocessing
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

# PREFERENCES
full_wiki = True
full_wiki_path = r"C:\Users\jacob\Desktop/enwiki-20181101-pages-articles-multistream.xml.bz2"
simple_wiki_path = r"C:\Users\jacob\Desktop/simplewiki-20170820-pages-meta-current.xml.bz2"


class TaggedWikiDocument(object):
    def __init__(self, wikipedia):
        self.wikipedia = wikipedia
        self.wikipedia.metadata = True

    def __iter__(self):
        for texts, (id, title) in self.wikipedia.get_texts():
            yield TaggedDocument([texts for texts in texts], [title])


if __name__ == '__main__':

    if full_wiki:
        wiki_path = WikiCorpus(full_wiki_path)
        model_name = "doc2vec.model"
    else:
        wiki_path = WikiCorpus(simple_wiki_path)
        model_name = "simple.model"

    print("Model loaded successfully")
    documents = TaggedWikiDocument(wiki_path)
    cores = multiprocessing.cpu_count()
    model = Doc2Vec(dm=1, dm_mean=1, vector_size=100, window=8, min_count=19, epochs=10, workers=cores)
    model.build_vocab(documents)
    print("Training model")
    model.train(documents, epochs=model.iter, total_examples=model.corpus_count)
    model.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)
    print("Saving model")
    model.save(model_name)
    print("model saved")
