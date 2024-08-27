'''
Author: RedKold redkold233@gmail.com
Date: 2024-08-26 10:30:23
LastEditors: RedKold redkold233@gmail.com
LastEditTime: 2024-08-27 11:42:13
FilePath: \SRT-learner\setVectorBase.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pickle
import torch
from sentence_transformers import SentenceTransformer, util

def load_embeddings(db_file='subtitle_db.pkl'):
    with open(db_file, 'rb') as db:
        data = pickle.load(db)
    return data['lines'], data['timestamps'], data['embeddings']

def find_most_similar(query,k,model_name='paraphrase-multilingual-MiniLM-L12-v2', db_file='subtitle_db.pkl'):
    # 加载本地保存的嵌入数据
    lines, timestamps, embeddings = load_embeddings(db_file)

    # 加载模型进行查询
    model = SentenceTransformer(model_name)
    query_embedding = model.encode(query, convert_to_tensor=True)

    # 计算余弦相似度
    cosine_sim = util.cos_sim(query_embedding, embeddings)

    # 找到前 k 条最相似的台词
    top_k_indices = torch.topk(cosine_sim, k).indices
    top_k_indices=torch.squeeze(top_k_indices)
    print(top_k_indices)
    top_k_indices=top_k_indices.tolist()

    # 返回相应的台词、时间轴和相似度
    top_k_lines = [lines[i] for i in top_k_indices]
    top_k_timestamps = [timestamps[i] for i in top_k_indices]
    top_k_similarities = [cosine_sim[0][i].item() for i in top_k_indices]

    return top_k_lines, top_k_timestamps, top_k_similarities

if __name__ == "__main__":
    k=6
    query = "我爱你"
    top_k_lines, top_k_timestamps, top_k_similarities = find_most_similar(query,k)
    # 打印查询结果
    for i in range(k):
        print(f"相似度: {top_k_similarities[i]:.4f}\n时间轴: {top_k_timestamps[i]}\n台词: {top_k_lines[i]}\n")
