#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成视频片段 - 一拳超人 vs 鸣人
10 个场景，每个 12 秒
"""

import sys
sys.path.insert(0, '/home/jcs130/.copaw/active_skills')

from volc_multimedia_sdk import VolcVideo
import os
import time

# 配置
API_KEY = "8d27bf88-53b0-4656-9946-f21934f4f24b"
MODEL = "ep-20260227022253-b67vh"  # seedance1.5pro

KEYFRAMES_DIR = "/home/jcs130/.copaw/workspaces/64cKss/media/project_002/keyframes"
OUTPUT_DIR = "/home/jcs130/.copaw/workspaces/64cKss/media/project_002/videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 10 个场景的视频提示词
SCENES = [
    {
        "name": "00_opening",
        "prompt": "Anime title screen with dramatic text appearing, energy waves spreading, two silhouettes emerging from darkness on opposite sides, camera zooming out slowly, cinematic opening sequence",
        "first_frame": "00_start.png",
        "last_frame": "00_end.png",
        "duration": 12
    },
    {
        "name": "01_power",
        "prompt": "Close-up of fist gathering energy, power building up, then massive collision explosion with shockwave, camera shaking from impact, slow motion on impact moment",
        "first_frame": "01_power_start.png",
        "last_frame": "01_power_end.png",
        "duration": 12
    },
    {
        "name": "02_speed",
        "prompt": "Silhouette sprinting forward creating multiple afterimages, speed lines rushing past, motion blur effects, camera tracking alongside the running figure",
        "first_frame": "02_speed_start.png",
        "last_frame": "02_speed_end.png",
        "duration": 12
    },
    {
        "name": "03_defense",
        "prompt": "Energy barrier shield activating with hexagonal patterns, powerful beam attack hitting the shield, impact creating bright flash and sparks, shield holding firm",
        "first_frame": "03_defense_start.png",
        "last_frame": "03_defense_end.png",
        "duration": 12
    },
    {
        "name": "04_ability",
        "prompt": "Blue energy ball forming and spiraling in hand, then cut to yellow energy punch launching forward, camera following the energy beam trajectory",
        "first_frame": "04_ability_start.png",
        "last_frame": "04_ability_end.png",
        "duration": 12
    },
    {
        "name": "05_experience",
        "prompt": "Young silhouette training at sunset, time-lapse transition showing growth, camera panning from young to mature warrior, warm to cool lighting transition",
        "first_frame": "05_exp_start.png",
        "last_frame": "05_exp_end.png",
        "duration": 12
    },
    {
        "name": "06_stamina",
        "prompt": "Two fighters facing each other at sunset, time passing shown by sky changing to night with moon rising, both still standing determined, camera circling around",
        "first_frame": "06_stamina_start.png",
        "last_frame": "06_stamina_end.png",
        "duration": 12
    },
    {
        "name": "07_growth",
        "prompt": "Timeline graphic showing progression from left to right, silhouette growing and powering up, golden aura expanding, camera panning along the timeline",
        "first_frame": "07_growth_start.png",
        "last_frame": "07_growth_end.png",
        "duration": 12
    },
    {
        "name": "08_analysis",
        "prompt": "Radar chart appearing with animated lines drawing, two colored areas filling in, comparison data showing, camera zooming into the chart details",
        "first_frame": "08_analysis_start.png",
        "last_frame": "08_analysis_end.png",
        "duration": 12
    },
    {
        "name": "09_ending",
        "prompt": "Two fighters showing mutual respect with fist bump, sunset background with warm glow, transition to end screen with text appearing, call to action elements",
        "first_frame": "09_end_start.png",
        "last_frame": "09_end_end.png",
        "duration": 12
    },
]

def generate_video(scene):
    """生成单个视频片段"""
    name = scene["name"]
    prompt = scene["prompt"]
    duration = scene["duration"]
    
    first_frame_path = f"{KEYFRAMES_DIR}/{scene['first_frame']}"
    last_frame_path = f"{KEYFRAMES_DIR}/{scene['last_frame']}"
    output_path = f"{OUTPUT_DIR}/{name}.mp4"
    
    video = VolcVideo(api_key=API_KEY)
    
    result = video.generate_from_first_last_frames(
        first_frame_path=first_frame_path,
        last_frame_path=last_frame_path,
        prompt=prompt,
        model=MODEL,
        duration=duration,
        watermark=False,
        timeout=900
    )
    
    if result and 'video_url' in result:
        # 下载视频
        import requests
        video_url = result['video_url']
        video_data = requests.get(video_url, timeout=300).content
        
        with open(output_path, "wb") as f:
            f.write(video_data)
        
        return True, output_path
    else:
        return False, result

def main():
    print("=" * 60)
    print("生成视频片段 - 一拳超人 vs 鸣人")
    print("=" * 60)
    
    total = len(SCENES)
    success = 0
    
    for i, scene in enumerate(SCENES):
        print(f"\n[{i+1}/{total}] 生成场景：{scene['name']}")
        print(f"  时长：{scene['duration']}秒")
        print(f"  提示词：{scene['prompt'][:60]}...")
        
        try:
            ok, result = generate_video(scene)
            
            if ok:
                print(f"  ✅ 成功：{result}")
                success += 1
            else:
                print(f"  ❌ 失败：{result}")
            
        except Exception as e:
            print(f"  ❌ 错误：{e}")
        
        # 避免限流
        if i < total - 1:
            print(f"  ⏳ 等待 3 秒...")
            time.sleep(3)
    
    print("\n" + "=" * 60)
    print(f"完成！成功：{success}/{total}")
    print("=" * 60)

if __name__ == "__main__":
    main()
