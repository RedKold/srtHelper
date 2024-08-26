'''
Author: RedKold redkold233@gmail.com
Date: 2024-08-26 09:21:24
LastEditors: RedKold redkold233@gmail.com
LastEditTime: 2024-08-26 11:09:09
FilePath: \SRT-learner\readSrt.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pysrt
import os

# 切换到指定工作目录
current_dir = os.getcwd()
print(f"Current working directory: {current_dir}")
os.chdir("E:\\Codinglife\\Python_project\\SRT-learner")

# 读取 SRT 文件并建立台词与时间轴的对照表
def read_srt(file_path):
    subs = pysrt.open(file_path)
    # 存储台词和时间轴信息的字典
    subtitle_dict = {}
    
    for sub in subs:
        start_time = sub.start.to_time()  # 获取开始时间
        end_time = sub.end.to_time()      # 获取结束时间
        text = sub.text.replace('\n', ' ')  # 将多行台词合并为一行
        time_range = f"{start_time} --> {end_time}"
        subtitle_dict[time_range] = text

    return subtitle_dict

# 保存对照表到文本文件
def save_to_file(subtitle_dict, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for time_range, text in subtitle_dict.items():
            file.write(f"{time_range}:\n{text}\n")

# 示例：读取并保存
if __name__ == "__main__":
    file_path = 'srt\\Frozen_chs.srt'  # 替换为你的 SRT 文件路径
    output_file = 'output_str.txt'     # 替换为输出文件路径
    subtitle_dict = read_srt(file_path)
    save_to_file(subtitle_dict, output_file)

    print(f"台词和时间轴对照表已保存到 {output_file}")
