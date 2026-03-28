#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project 003: 木屋烧烤宣传视频 - 生成视频片段
使用首尾帧控制生成 10 个视频片段
"""

import sys
sys.path.insert(0, '/home/jcs130/.copaw/active_skills')

from volc_video_sdk import VolcVideo
import os
import time

# 配置
API_KEY = "8d27bf88-53b0-4656-9946-f21934f4f24b"
MODEL = "ep-20260227022253-b67vh"  # 视频端点

KEYFRAMES_DIR = "/home/jcs130/.copaw/workspaces/64cKss/media/project_003/keyframes"
VIDEOS_DIR = "/home/jcs130/.copaw/workspaces/64cKss/media/project_003/videos"
os.makedirs(VIDEOS_DIR, exist_ok=True)

# 10 个场景的视频生成提示词
SCENES = [
    {"name": "00_opening", "prompt": "Camera slowly zooming in on wooden BBQ sign glowing in rainy night, warm yellow light creating atmospheric mood, cinematic opening shot", "duration": 5},
    {"name": "01_approach", "prompt": "Camera moving closer to BBQ stall, charcoal fire sparks flying, steam rising from grill, warm inviting atmosphere", "duration": 3},
    {"name": "02_characters", "prompt": "Two middle-aged men sitting at table, rain drops falling from eaves, warm light on faces, natural conversation pose", "duration": 4},
    {"name": "03_grilling", "prompt": "Close-up of meat skewers on grill, oil dripping, smoke rising, hand sprinkling seasoning, food photography style", "duration": 4},
    {"name": "04_memory", "prompt": "Man's face showing nostalgic smile, eyes full of memories, warm lighting, emotional moment, subtle head shake", "duration": 4},
    {"name": "05_eating", "prompt": "Man taking big bite of meat skewer, satisfied expression, enjoying food, authentic eating motion", "duration": 4},
    {"name": "06_pouring", "prompt": "Beer being poured into glass, golden liquid flowing, white foam rising, slow motion liquid movement", "duration": 4},
    {"name": "07_contemplation", "prompt": "Man looking at dark ocean thoughtfully, contemplative mood, rain in background, emotional depth", "duration": 6},
    {"name": "08_toast", "prompt": "Two men clinking beer glasses together, genuine smiles, foam splashing, warm brotherhood moment", "duration": 6},
    {"name": "09_ending", "prompt": "Camera pulling back to reveal full restaurant scene, warm lights in rainy night, peaceful ending, cinematic fade", "duration": 10}
]

def generate_videos():
    print("=" * 60)
    print("Project 003: 木屋烧烤 - 生成视频片段")
    print("=" * 60)
    
    video = VolcVideo(api_key=API_KEY)
    
    for i, scene in enumerate(SCENES):
        name = scene["name"]
        prompt = scene["prompt"]
        duration = scene["duration"]
        
        first_frame = f"{KEYFRAMES_DIR}/{i:02d}_start.png"
        last_frame = f"{KEYFRAMES_DIR}/{i:02d}_end.png"
        output_path = f"{VIDEOS_DIR}/{name}.mp4"
        
        print(f"\n[{i+1}/{len(SCENES)}] 生成：{name} ({duration}s)")
        print(f"  首帧：{first_frame}")
        print(f"  尾帧：{last_frame}")
        print(f"  提示词：{prompt[:60]}...")
        
        if not os.path.exists(first_frame):
            print(f"  ❌ 首帧不存在")
            continue
        if not os.path.exists(last_frame):
            print(f"  ❌ 尾帧不存在")
            continue
        
        try:
            result = video.generate_from_first_last_frames(
                first_frame_path=first_frame,
                last_frame_path=last_frame,
                prompt=prompt,
                model=MODEL,
                duration=duration,
                watermark=False,
                timeout=300
            )
            
            if result and result.get('video_url'):
                # 下载视频
                import requests
                video_url = result['video_url']
                print(f"  下载视频：{video_url[:80]}...")
                
                video_data = requests.get(video_url, timeout=300).content
                with open(output_path, 'wb') as f:
                    f.write(video_data)
                
                print(f"  ✅ 成功：{output_path}")
            else:
                print(f"  ❌ 失败：{result}")
        except Exception as e:
            print(f"  ❌ 错误：{e}")
        
        # 避免限流
        if i < len(SCENES) - 1:
            print(f"  等待 3 秒...")
            time.sleep(3)
    
    print("\n" + "=" * 60)
    print("✅ 视频生成完成！")
    print(f"📁 输出目录：{VIDEOS_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    generate_videos()
