from warnings import filters
import math
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.parsing.preprocessing import preprocess_string
from gensim.parsing import (
    strip_tags, strip_punctuation, strip_multiple_whitespaces, strip_numeric,
    remove_stopwords, strip_short
)

def preprocess_routine(texts):
    texts =  ["\n".join(x.split("\n", maxsplit=1)[1:]) for x in texts]
    CUSTOM_FILTERS = [lambda x: x.lower(),
                      strip_tags,
                      strip_punctuation,
                      strip_multiple_whitespaces,
                      strip_numeric,
                      remove_stopwords,
                      strip_short]
    texts =  [preprocess_string(x, filters=CUSTOM_FILTERS) for x in texts]
    return texts

def get_topic_words(result_model, num_topics, num_words):
    topic_data = []
    content_topics = []
    content_topics.append(result_model.print_topics(num_topics=num_topics, num_words=num_words))
    for cont in content_topics:
        for top in cont:
            itens = top[1].split("+")
            words = []
            for i in itens:
                it = i.split("*")
                pal = it[1].split("\"")
                words.append(pal[1])
            topic_data.append({
                "words" : words,
                "name" : "_".join(words[:3])
            })
    return topic_data

def run_inference(model, titles, lyrics):
    dictionary = model.id2word
    json_inferece_topics = []
    for i, t in enumerate(lyrics):    
        other_corpus = [dictionary.doc2bow(t)] 
        doc_topics = model.get_document_topics(other_corpus, minimum_probability=-math.inf)
        percent_order_topics = sorted(doc_topics[0], key=lambda x: x[1], reverse=True)
        float_formatted_topics = []
        for id, val in percent_order_topics:
            v = float(val)
            float_formatted_topics.append((id,v))
        item = {titles[i]:float_formatted_topics}
        json_inferece_topics.append(item)
    return json_inferece_topics

def run_lda(titles, lyrics, n_topics):
    lyrics = preprocess_routine(lyrics)
    dictionary = Dictionary(lyrics)
    corpus = [dictionary.doc2bow(text) for text in lyrics]
    lda = LdaModel(corpus, num_topics=n_topics, id2word=dictionary, eta='auto', alpha='auto')
    topic_data = get_topic_words(lda, n_topics, 5)
    topic_inference = run_inference(lda, titles, lyrics)
    return (topic_data, topic_inference)