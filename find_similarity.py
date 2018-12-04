import load_model

# PREFERENCES
full_wiki = False


def find_similarity(article_title):
    elements = model[article_title]
    print("5 first elements of the article vector: %s" % elements[:5])
    print("Printing the top 20 articles most similar to %s" % article_title)
    sim = model.most_similar([article_title], topn=20)
    print(sim)


if full_wiki:
    model_path = "doc2vec.model"
else:
    model_path = "simple.model"

model = load_model.get_model_vectors(model_path)
while True:
    article = input("Enter an article title: ")
    try:
        model.most_similar([article])
    except:
        print("Article does not exist, please try again")
    else:
        find_similarity(article)
