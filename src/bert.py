from transformers import BertModel, BertTokenizer
import torch
from RainbowPrint import RainbowPrint as rp

tokenizer = BertTokenizer.from_pretrained('./BERT_CCPoem_v1')
model = BertModel.from_pretrained('./BERT_CCPoem_v1')

rp.info("bert 加载完成")

def text2vec(text):
    if isinstance(text,list):
        input_ids = torch.tensor(tokenizer.batch_encode_plus(text)['input_ids'])
    else:
        input_ids = torch.tensor(tokenizer.encode(text)).unsqueeze(0)
    outputs = model(input_ids).last_hidden_state
    sen_emb = torch.mean(outputs, 1)
    return sen_emb.detach().numpy()

# def text_l2vec(text_l):
#     input_ids = torch.tensor(tokenizer.batch_encode_plus(text_l)['input_ids'])
#     outputs = model(input_ids).last_hidden_state
#     sen_emb = torch.mean(outputs, 1)
#     return sen_emb.detach().numpy()