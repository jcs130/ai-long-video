#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
短视频完整工作流脚本 - Project 003 V2 模板
包含：配音生成 → SRT 自动生成 → 视频裁剪 → 合并 → 字幕
"""

import os
import sys
import json
import base64
import requests
import subprocess
from pathlib import Path

sys.path.insert(0, '/home/jcs130/.copaw/active_skills')

# ========== 配置 ==========
API_KEY = "8d27bf88-53b0-4656-9946-f21934f4f24b"
VIDEO_MODEL = "ep-20260227022253-b67vh"
IMAGE_MODEL = "ep-20260227121917-j9vll"

# TTS 配置
TTS_APP_ID = "3019120872"
TTS_ACCESS_KEY = "qcdGrSiKz8_8qTkHo1whQREW48QPWT6I"
TTS_RESOURCE_ID = "seed-tts-2.0"
TTS_URL = "https://openspeech.bytedance.com/api/v3/tts/unidirectional/sse"

# 工作目录
WORK_DIR = Path("/home/jcs130/.copaw/workspaces/64cKss/media/project_003")

# ========== 角色声音设定（必须一致） ==========
ROLES = {
    "旁白": {"speaker": "zh_male_m191_uranus_bigtts", "speed": 0.95, "pitch": -2},
    "老张": {"speaker": "zh_male_m191_uranus_bigtts", "speed": 1.0, "pitch": 0},
    "老李": {"speaker": "zh_male_m191_uranus_bigtts", "speed": 1.15, "pitch": 4},
}

# ========== 脚本（台词 + 视频片段对应） ==========
SCRIPT = [
    {"role": "旁白", "text": "成年人的世界，只有深夜才能卸下防备", "video": "01_opening.mp4"},
    {"role": "旁白", "text": "和兄弟撸串喝酒，才是真正的生活", "video": "02_approach.mp4"},
    {"role": "老张", "text": "敬第十年", "video": "03_zhang_toast.mp4"},
    {"role": "老李", "text": "十年啊，还记得第一次来这吗", "video": "04_li_respond.mp4"},
    {"role": "老张", "text": "兜里不到 100 块，你请的我", "video": "05_zhang_memory.mp4"},
    {"role": "老李", "text": "来吃肉，那时候你比现在瘦", "video": "06_li_laugh.mp4"},
    {"role": "老张", "text": "啥叫日子", "video": "07_zhang_thought.mp4"},
    {"role": "老李", "text": "有人陪你喝酒，有人陪你聊天", "video": "08_li_answer.mp4"},
    {"role": "老张", "text": "敬兄弟", "video": "09_cheers.mp4"},
    {"role": "旁白", "text": "木屋烧烤，十年烟火，敬每一个不眠的夜晚", "video": "10_ending.mp4"},
]

def generate_tts(text, role, output_path):
    """生成单个 TTS 音轨"""
    config = ROLES[role]
    
    headers = {
        "X-Api-App-Id": TTS_APP_ID,
        "X-Api-Access-Key": TTS_ACCESS_KEY,
        "X-Api-Resource-Id": TTS_RESOURCE_ID,
        "Content-Type": "application/json"
    }
    
    payload = {
        "user": {"uid": "user_001"},
        "req_params": {
            "speaker": config["speaker"],
            "text": text,
            "audio_params": {"format": "mp3", "sample_rate": 24000},
            "speed_ratio": config["speed"],
            "pitch": config["pitch"],
        }
    }
    
    response = requests.post(TTS_URL, headers=headers, json=payload, stream=True)
    
    audio_data = b""
    for line in response.iter_lines():
        if line.startswith(b'data:'):
            try:
                event = json.loads(line[5:])
                if 'data' in event and event['data']:
                    audio_data += base64.b64decode(event['data'])
            except:
                continue
    
    if not audio_data:
        return None
    
    with open(output_path, 'wb') as f:
        f.write(audio_data)
    
    return output_path

def get_audio_duration(audio_path):
    """获取音频时长（秒）"""
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
           '-of', 'default=noprint_wrappers=1:nokey=1', audio_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def format_time(seconds):
    """秒转 SRT 时间格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:06.3f}".replace('.', ',')

def generate_srt(tracks, output_path):
    """根据配音生成对齐 SRT"""
    current_time = 0.0
    srt_content = ""
    
    for i, track in enumerate(tracks, 1):
        duration = get_audio_duration(track["audio"])
        start_time = current_time
        end_time = start_time + duration
        
        speaker = track["role"]
        text = track["text"]
        full_text = f"{speaker}：{text}" if speaker != "旁白" else text
        
        srt_content += f"{i}\n"
        srt_content += f"{format_time(start_time)} --> {format_time(end_time)}\n"
        srt_content += f"{full_text}\n\n"
        
        current_time = end_time
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(srt_content)
    
    return current_time

def main():
    print("=" * 70)
    print("短视频完整工作流 - Project 003 V2")
    print("=" * 70)
    
    # 创建目录
    tracks_dir = WORK_DIR / "tracks_auto"
    videos_sync_dir = WORK_DIR / "videos_sync_auto"
    tracks_dir.mkdir(exist_ok=True)
    videos_sync_dir.mkdir(exist_ok=True)
    
    # 步骤 1: 生成所有配音音轨
    print("\n🎙️  步骤 1: 生成配音")
    tracks = []
    for i, item in enumerate(SCRIPT, 1):
        audio_file = tracks_dir / f"track_{i:02d}.mp3"
        print(f"  生成 {i}/{len(SCRIPT)}: {item['role']} - {item['text'][:20]}...")
        
        generate_tts(item["text"], item["role"], audio_file)
        
        tracks.append({
            "index": i,
            "role": item["role"],
            "text": item["text"],
            "audio": str(audio_file),
            "video": item["video"]
        })
        print(f"    ✅ {audio_file.name}")
    
    # 步骤 2: 生成 SRT 字幕
    print("\n📝 步骤 2: 生成 SRT 字幕")
    srt_path = WORK_DIR / "subtitles_auto.srt"
    total_duration = generate_srt(tracks, srt_path)
    print(f"  ✅ 总时长：{total_duration:.2f}秒")
    
    # 步骤 3: 裁剪视频匹配配音
    print("\n✂️  步骤 3: 裁剪视频")
    for track in tracks:
        video_path = WORK_DIR / "videos_v2" / track["video"]
        if not video_path.exists():
            print(f"  ⚠️  跳过：{video_path} 不存在")
            continue
        
        duration = get_audio_duration(track["audio"])
        output = videos_sync_dir / f"{track['index']:02d}_trimmed.mp4"
        
        cmd = ['ffmpeg', '-y', '-i', str(video_path), '-t', str(duration),
               '-c', 'copy', str(output)]
        subprocess.run(cmd, capture_output=True)
        print(f"  ✅ {track['video']} → {duration:.2f}s")
    
    # 步骤 4: 合并视频
    print("\n🎬 步骤 4: 合并视频")
    concat_file = videos_sync_dir / "concat.txt"
    with open(concat_file, 'w') as f:
        for i in range(1, len(tracks) + 1):
            f.write(f"file '{videos_sync_dir}/{i:02d}_trimmed.mp4'\n")
    
    merged_video = WORK_DIR / "video_merged_auto.mp4"
    cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(concat_file),
           '-c', 'copy', str(merged_video)]
    subprocess.run(cmd, capture_output=True)
    print(f"  ✅ {merged_video.name}")
    
    # 步骤 5: 合并配音
    print("\n🔊 步骤 5: 合并配音")
    audio_concat = tracks_dir / "concat.txt"
    with open(audio_concat, 'w') as f:
        for track in tracks:
            f.write(f"file '{track['audio']}'\n")
    
    merged_audio = WORK_DIR / "narration_auto.mp3"
    cmd = ['ffmpeg', '-y', '-f', 'concat', '-safe', '0', '-i', str(audio_concat),
           '-c', 'copy', str(merged_audio)]
    subprocess.run(cmd, capture_output=True)
    print(f"  ✅ {merged_audio.name}")
    
    # 步骤 6: 视频 + 配音 + 字幕
    print("\n✨ 步骤 6: 合成最终视频")
    final_video = WORK_DIR / "video_final_auto.mp4"
    
    cmd = [
        'ffmpeg', '-y',
        '-i', str(merged_video),
        '-i', str(merged_audio),
        '-c:v', 'copy', '-c:a', 'aac', '-b:a', '128k',
        '-map', '0:v:0', '-map', '1:a:0', '-shortest',
        str(WORK_DIR / "video_with_audio_temp.mp4")
    ]
    subprocess.run(cmd, capture_output=True)
    
    cmd = [
        'ffmpeg', '-y',
        '-i', str(WORK_DIR / "video_with_audio_temp.mp4"),
        '-vf', f"subtitles={srt_path}:force_style='FontName=Source Han Sans CN,FontSize=36,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,ShadowColour=&H80000000,Outline=2,Alignment=2,MarginV=40'",
        '-c:a', 'copy',
        str(final_video)
    ]
    subprocess.run(cmd, capture_output=True)
    
    # 清理临时文件
    (WORK_DIR / "video_with_audio_temp.mp4").unlink()
    
    print(f"  ✅ {final_video.name}")
    
    # 输出信息
    print("\n" + "=" * 70)
    print("✅ 完成！")
    print("=" * 70)
    
    duration = get_audio_duration(merged_audio)
    size = final_video.stat().st_size / 1024 / 1024
    
    print(f"📊 总时长：{duration:.2f}秒")
    print(f"📊 文件大小：{size:.1f}MB")
    print(f"📁 输出文件：{final_video}")
    print("=" * 70)

if __name__ == "__main__":
    main()
