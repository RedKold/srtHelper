'''
Author: RedKold redkold233@gmail.com
Date: 2024-08-26 10:30:23
LastEditors: RedKold redkold233@gmail.com
LastEditTime: 2024-08-26 15:38:22
FilePath: \SRT-learner\setVectorBase.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from sentence_transformers import SentenceTransformer, util
import torch
import os
import pysrt
# 切换到指定工作目录
os.chdir("E:\\Codinglife\\Python_project\\SRT-learner")

# 加载预训练的 Sentence-BERT 模型
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 读取 SRT 文件，提取台词和时间轴信息
def read_srt(file_path):
    subs = pysrt.open(file_path, encoding='utf-8')
    lines = []  # 用于存储台词
    timestamps = []  # 用于存储时间轴

    for sub in subs:
        # 处理台词和时间轴
        text = sub.text.replace('\n', ' ')  # 将台词合并成一行
        time_range = f"{sub.start.to_time()} --> {sub.end.to_time()}"
        
        lines.append(text)
        timestamps.append(time_range)
    
    return lines, timestamps

def setVector():#返回对应台词和时间轴
    # 读取台词和时间轴
    srt_file_path = 'srt\\Frozen_chs.srt'
    lines, timestamps = read_srt(srt_file_path)

    # 生成台词嵌入
    embeddings = model.encode(lines, convert_to_tensor=True)

    query = "我爱你"
    query_embedding = model.encode(query, convert_to_tensor=True)

    # 计算余弦相似度并获取前 5 条最相似的台词
    cosine_sim = util.cos_sim(query_embedding, embeddings)[0]
    top_5_indices = torch.topk(cosine_sim, 5).indices.tolist()
    top_5_similarities = [cosine_sim[i].item() for i in top_5_indices]

    # 获取对应的台词和时间轴
    top_5_lines = [lines[i] for i in top_5_indices]
    top_5_timestamps = [timestamps[i] for i in top_5_indices]
    return top_5_lines,top_5_timestamps,top_5_similarities

