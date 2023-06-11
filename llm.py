from chromadb.config import Settings
from chromadb import Client
from sentence_transformers import SentenceTransformer, CrossEncoder
from transformers import AutoTokenizer, T5ForConditionalGeneration, pipeline
# from transformers import T5Tokenizer, T5ForConditionalGeneration
import torch
import numpy as np

# models
semb_model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')
xenc_model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-large")
# model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-large",
#                                                    device_map="auto",
#                                                    torch_dtype=torch.float32
#                                                    )

model_name = "MaRiOrOsSi/t5-base-finetuned-question-answering"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)
model.to(device)

# data

client = Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory=".chromadb/"
))
collection = client.get_collection("hoff5")


def rerank(query, docs, n_responses=1):
    reranked_indices = np.argsort(-xenc_model.predict(
        [[query, d] for d in docs]))
    reranked = [docs[r] for r in reranked_indices[0:n_responses]]

    return reranked


def answer_bot_skeleton(query, contexts, qa_tokenizer=tokenizer, qa_model=model, device=device):
    # def prompt_eng(x, y): return f'Answer the below question with the context provided.\n\nQuestion: {x}\n\nContext: {y}'
    def prompt_eng(x, y): return f"question: {x} context: {y}"

    input_texts = [prompt_eng(query, context) for context in contexts]
    input_ids = qa_tokenizer(input_texts, return_tensors="pt",
                             max_length=512, truncation=True).input_ids.to(device)

    output_ids = qa_model.generate(input_ids, max_new_tokens=128)
    output_texts = [qa_tokenizer.decode(
        o, skip_special_tokens=True) for o in output_ids]

    return output_texts


def qa_pipeline(query, n_responses=1):
    embs = semb_model.encode(query).tolist()

    # preliminary ranking
    docs = collection.query(query_embeddings=embs, n_results=32)[
        'documents'][0]

    # rerank
    docs = rerank(query, docs, n_responses=n_responses)

    # answer
    ans = answer_bot_skeleton(query, docs)[0]

    return ans
