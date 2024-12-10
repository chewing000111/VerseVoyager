import torch
import numpy as np
from src.bert import text2vec
from tqdm import tqdm
from src.load_poetry import load_tang_single_file

def _make_sentence_embeddings(sentences, batch_size = 100):
    for i in tqdm(range(len(sentences) // batch_size + 1)):
        sentences_temp = sentences[batch_size * i:batch_size * i + batch_size]
        try:
            sentence_embeddings_temp = text2vec(sentences_temp)
            yield sentence_embeddings_temp
        except:
            for s in sentences_temp:
                try:
                    sentence_embeddings_temp = text2vec(s)
                    yield sentence_embeddings_temp
                except Exception as e:
                    print(e, s)

def make_sentence_embeddings(json_path, sentence_embeddings_pt_path):

    book_ids, sentences, book_dict = load_tang_single_file(json_path)

    sentence_embeddings = None
    for sentence_embeddings_temp in _make_sentence_embeddings(sentences):
        if sentence_embeddings is None:
            sentence_embeddings = sentence_embeddings_temp
        else:
            sentence_embeddings = np.concatenate((sentence_embeddings, sentence_embeddings_temp), axis=0)

    save_data = {
        "df": {"book_id": book_ids, 'sentence': sentences},
        "book_dict": book_dict,
        "sentence_embeddings": sentence_embeddings
    }

    torch.save(save_data, sentence_embeddings_pt_path)



make_sentence_embeddings("./data/poet.song.test.json", "./data/sentence_embeddings/new_0.pt")


