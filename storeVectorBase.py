'''
Author: RedKold redkold233@gmail.com
Date: 2024-08-26 16:10:22
LastEditors: RedKold redkold233@gmail.com
LastEditTime: 2024-08-26 16:10:28
FilePath: \SRT-learner\storeVectorBase.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pickle
import os
from sentence_transformers import SentenceTransformer

def generate_and_save_embeddings(srt_file, model_name='paraphrase-multilingual-MiniLM-L12-v2', db_file='subtitle_db.pkl'):
    # 初始化模型
    model = SentenceTransformer(model_name)

    # 读取 SRT 文件并处理
    import pysrt
    subs = pysrt.open(srt_file, encoding='utf-8')
    lines = [sub.text.replace('\n', ' ') for sub in subs]
    timestamps = [f"{sub.start} --> {sub.end}" for sub in subs]

    # 生成嵌入向量
    embeddings = model.encode(lines, convert_to_tensor=True)

    # 存储数据到本地文件
    with open(db_file, 'wb') as db:
        pickle.dump({
            'lines': lines,
            'timestamps': timestamps,
            'embeddings': embeddings
        }, db)
    print(f"数据已保存到 {db_file}")

if __name__ == "__main__":
    # 生成并保存字幕数据库
    srt_file = 'srt/Frozen_chs.srt'  # 替换为你的 SRT 文件路径
    generate_and_save_embeddings(srt_file,db_file=f'{srt_file}_db.pkl')
