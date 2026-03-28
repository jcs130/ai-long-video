#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project 003: 木屋烧烤 - 生成 SRT 字幕
"""

# 场景数据：(开始时间秒，结束时间秒，台词，角色)
scenes = [
    (0, 5, "有人说，成年人的世界，没有容易二字。", "画外音"),
    (5, 8, "但总有个地方，能让你卸下防备。", "画外音"),
    (8, 12, "老张，这杯酒，敬咱们认识的第十年。", "男人 A"),
    (12, 16, "十年啊...还记得咱俩第一次来这儿吗？", "男人 B"),
    (16, 20, "怎么不记得，那时候咱俩兜里加起来不到 100 块。", "男人 A"),
    (20, 24, "哈哈，现在不也过来了？来，吃肉！", "男人 B"),
    (24, 28, "你说，啥叫日子？", "男人 A"),
    (28, 34, "日子啊，就是有人陪你吃肉，有人陪你扛事。", "男人 B"),
    (34, 40, "说得好！敬木屋，敬兄弟，敬这该死的生活！", "男人 A"),
    (40, 50, "木屋烧烤——有些话，有些肉，只和懂你的人分享。", "画外音"),
]

def format_time(seconds):
    """将秒数转换为 SRT 时间格式：HH:MM:SS,mmm"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def generate_srt(output_path="subtitles.srt"):
    """生成 SRT 文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, (start, end, text, role) in enumerate(scenes, 1):
            # 写入序号
            f.write(f"{i}\n")
            # 写入时间轴
            f.write(f"{format_time(start)} --> {format_time(end)}\n")
            # 写入字幕文本（带角色）
            if role != "画外音":
                f.write(f"{text}\n")
            else:
                f.write(f"{text}\n")
            # 空行
            f.write("\n")
    
    print(f"✅ SRT 文件已生成：{output_path}")
    print(f"📊 共 {len(scenes)} 条字幕，总时长 {scenes[-1][1]} 秒")

if __name__ == "__main__":
    generate_srt()
