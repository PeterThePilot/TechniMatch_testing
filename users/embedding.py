from transformers import BertModel, BertTokenizer
from sklearn.metrics.pairwise import cosine_similarity

model_name = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

def embedding(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).detach().numpy()



def sim(embedding1, embedding2):
    return cosine_similarity(embedding1, embedding2)[0][0]
