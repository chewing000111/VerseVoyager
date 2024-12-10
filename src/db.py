import faiss
import pandas
import os
import torch
import numpy as np
from .bert import text2vec
from tqdm import tqdm
from collections import defaultdict
from RainbowPrint import RainbowPrint as rp

sentence_embeddings_pt_path = "./data/sentence_embeddings"

# def _make_sentence_embeddings(sentences, batch_size = 100):
#     for i in tqdm(range(len(sentences) // batch_size + 1)):
#         sentences_temp = sentences[batch_size * i:batch_size * i + batch_size]
#         try:
#             sentence_embeddings_temp = text2vec(sentences_temp)
#             yield sentence_embeddings_temp
#         except:
#             for s in sentences_temp:
#                 try:
#                     sentence_embeddings_temp = text2vec(s)
#                     yield sentence_embeddings_temp
#                 except Exception as e:
#                     rp.error(e, s)
#
# def make_sentence_embeddings():
#     # books = ["《黄鹤楼送孟浩然之广陵》","《送元二使安西》","《咏柳》"]
#     # authors = ["李白","王维","贺知章"]
#     # sentences = ["故人西辞黄鹤楼，烟花三月下扬州。孤帆远影碧空尽，唯见长江天际流。",
#     #              "渭城朝雨浥轻尘，客舍青青柳色新。劝君更尽一杯酒，西出阳关无故人。",
#     #              "碧玉妆成一树高，万条垂下绿丝绦。不知细叶谁裁出，二月春风似剪刀。"]
#
#     from .load_protry import load_tang
#     book_ids, sentences, book_dict = load_tang()
#
#     sentence_embeddings = None
#     for sentence_embeddings_temp in _make_sentence_embeddings(sentences):
#         if sentence_embeddings is None:
#             sentence_embeddings = sentence_embeddings_temp
#         else:
#             sentence_embeddings = np.concatenate((sentence_embeddings, sentence_embeddings_temp), axis=0)
#
#     # sentence_embeddings = text2vec(sentences)
#
#     save_data = {
#         "df": {"book_id": book_ids, 'sentence': sentences},
#         "book_dict": book_dict,
#         "sentence_embeddings": sentence_embeddings
#     }
#
#     torch.save(save_data, sentence_embeddings_pt_path)


# if not os.path.exists(sentence_embeddings_pt_path):
#     rp.info("编译向量数据库")
#     # make_sentence_embeddings()
#     raise Exception("现在不支持运行时编译向量数据库")

df_book_ids = []
df_sentences = []
sentence_embeddings = None
book_dict = {}
for pt_file in os.listdir(sentence_embeddings_pt_path):
    if not pt_file.endswith(".pt"):
        continue
    rp.info("加载数据集: {}".format(pt_file))
    state = pt_file.split("_")[0]
    data_0 = torch.load(os.path.join(sentence_embeddings_pt_path, pt_file))
    df0_book_ids = data_0["df"]["book_id"]
    df0_sentences = data_0["df"]["sentence"]
    book_dict0 = data_0["book_dict"]
    for _, d in book_dict0.items():
        d["state"] = state
    sentence_embeddings0 = data_0["sentence_embeddings"]
    df_book_ids += df0_book_ids
    df_sentences += df0_sentences
    if sentence_embeddings is None:
        sentence_embeddings = sentence_embeddings0
    else:
        sentence_embeddings = np.concatenate((sentence_embeddings, sentence_embeddings0), axis=0)
    book_dict = book_dict | book_dict0

dimension = sentence_embeddings.shape[1]
df = pandas.DataFrame({"book_id": df_book_ids, 'sentence': df_sentences})

index = faiss.IndexFlatL2(dimension)
index.add(sentence_embeddings)

rp.info("faiss 向量数据库 加载完成")

def search(search_text, topK = 100):
    search = text2vec(search_text)
    D, I = index.search(search, topK)
    rp.info(f"查询:{search_text}\n结果：")
    print(df.iloc[I[0]])

    books = defaultdict(list)
    for i, row in df.iloc[I[0]].iterrows():
        books[row['book_id']].append(row["sentence"])
    rtn = []
    for book_id, target_sentences in books.items():
        book = book_dict[book_id].copy()
        book["target_sentences"] = target_sentences
        rtn.append(book)
    return rtn
