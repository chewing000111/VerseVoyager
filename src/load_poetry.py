import os
from src.utils import load_json
from tqdm import tqdm
def load_tang():

    book_ids = []
    sentences = []
    book_dict = {}  # 方便查询完整诗词

    for f in os.listdir("./data/全唐诗-简体/唐"):
        if f.startswith("poet."):
            data = load_json(f"./data/全唐诗-简体/唐/{f}")
            for i, p in enumerate(data):
                book_id = p["title"]+"|"+p["author"]
                if book_id in book_dict:
                    continue
                for s in p["paragraphs"]:
                    book_ids.append(book_id)
                    sentences.append(s)
                book_data = {k:d for k,d in p.items() if k in ["author", "paragraphs", "title"]}

                book_data["paragraphs_tr"] = []
                book_dict[book_id] = book_data


            break


    return book_ids, sentences, book_dict


def load_tang_single_file(json_path):

    book_ids = []
    sentences = []
    book_dict = {}  # 方便查询完整诗词

    data = load_json(json_path)
    for p in tqdm(data):
        book_id = p["title"]+"|"+p["author"]
        for s in p["paragraphs"]:
            book_ids.append(book_id)
            sentences.append(s)
        book_data = {k:d for k,d in p.items() if k in ["author", "paragraphs", "title", "paragraphs_tr"]}
        book_dict[book_id] = book_data

    return book_ids, sentences, book_dict

if __name__ == '__main__':
    os.chdir("../")

    book_ids, sentences, book_dict =load_tang()
    for sentence in book_dict.items():
        print(sentence)