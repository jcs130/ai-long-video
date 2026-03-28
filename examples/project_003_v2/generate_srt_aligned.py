#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project 003 V2: 生成对齐字幕 SRT
根据实际配音时长自动生成字幕时间轴
"""

import os
import subprocess

def get_audio_duration(audio_path):
    """获取音频文件时长（秒）"""
    cmd = [
        'ffprobe', '-v', 'error',
        '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        audio_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def format_time(seconds):
    """秒转 SRT 时间格式 (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}".replace('.', ',')

def generate_srt(tracks_dir, script, output_path):
    """
    根据配音音轨生成对齐的 SRT 字幕
    
    Args:
        tracks_dir: 音轨文件目录
        script: 台词列表 [{"file": "track_旁白_01.mp3", "text": "台词", "speaker": "旁白"}]
        output_path: 输出 SRT 路径
    """
    current_time = 0.0
    srt_content = ""
    
    for i, item in enumerate(script, 1):
        audio_file = os.path.join(tracks_dir, item["file"])
        text = item["text"]
        speaker = item.get("speaker", "")
        
        # 获取实际时长
        duration = get_audio_duration(audio_file)
        start_time = current_time
        end_time = start_time + duration
        
        # 添加说话人前缀
        if speaker and speaker != "旁白":
            full_text = f"{speaker}：{text}"
        else:
            full_text = text
        
        # 生成 SRT 条目
        srt_content += f"{i}\n"
        srt_content += f"{format_time(start_time)} --> {format_time(end_time)}\n"
        srt_content += f"{full_text}\n\n"
        
        print(f"#{i}: {start_time:.2f}s - {end_time:.2f}s ({duration:.2f}s) - {speaker}")
        
        current_time = end_time
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    
    print(f"\n✅ SRT 生成完成：{output_path}")
    print(f"📊 总时长：{current_time:.2f}秒")
    return output_path

def main():
    print("=" * 70)
    print("Project 003 V2: 生成对齐字幕")
    print("=" * 70)
    
    tracks_dir = "tracks_v2"
    output_path = "subtitles_v2_aligned.srt"
    
    # 台词列表（按顺序）
    script = [
        {"file": "track_旁白_01.mp3", "text": "成年人的世界，只有深夜才能卸下防备", "speaker": "旁白"},
        {"file": "track_旁白_02.mp3", "text": "和兄弟撸串喝酒，才是真正的生活", "speaker": "旁白"},
        {"file": "track_老张_03.mp3", "text": "敬第十年", "speaker": "老张"},
        {"file": "track_老李_04.mp3", "text": "十年啊，还记得第一次来这吗", "speaker": "老李"},
        {"file": "track_老张_05.mp3", "text": "兜里不到 100 块，你请的我", "speaker": "老张"},
        {"file": "track_老李_06.mp3", "text": "来吃肉，那时候你比现在瘦", "speaker": "老李"},
        {"file": "track_老张_07.mp3", "text": "啥叫日子", "speaker": "老张"},
        {"file": "track_老李_08.mp3", "text": "有人陪你喝酒，有人陪你聊天", "speaker": "老李"},
        {"file": "track_老张_09.mp3", "text": "敬兄弟", "speaker": "老张"},
        {"file": "track_旁白_10.mp3", "text": "木屋烧烤，十年烟火，敬每一个不眠的夜晚", "speaker": "旁白"},
    ]
    
    generate_srt(tracks_dir, script, output_path)
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
