#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成关键帧 - 一拳超人 vs 鸣人
使用剪影风格，避免版权问题
"""

import requests
import base64
import json
import os

# 配置
API_KEY = "8d27bf88-53b0-4656-9946-f21934f4f24b"
ENDPOINT = "ep-20260227022253-b67vh"

OUTPUT_DIR = "/home/jcs130/.copaw/workspaces/64cKss/media/project_002/keyframes"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 10 个场景的关键帧提示词
PROMPTS = [
    # 场景 0: 开场
    {
        "name": "00_start",
        "prompt": "Anime style title screen, dramatic text '一拳超人 VS 火影忍者', dark background with orange and yellow energy effects, cinematic lighting, 960x960"
    },
    {
        "name": "00_end",
        "prompt": "Two silhouettes facing each other, one in yellow cape, one in orange outfit, dramatic confrontation stance, energy aura around them, dark background, anime style, 960x960"
    },
    
    # 场景 1: 力量对比
    {
        "name": "01_power_start",
        "prompt": "Anime fist glowing with power, energy gathering around clenched fist, dramatic lighting, orange and yellow sparks, 960x960"
    },
    {
        "name": "01_power_end",
        "prompt": "Massive energy explosion from fist impact, shockwave spreading, ground cracking, dramatic anime action scene, 960x960"
    },
    
    # 场景 2: 速度对比
    {
        "name": "02_speed_start",
        "prompt": "Silhouette in running stance, motion blur effects, speed lines, wind swirling around, anime action style, 960x960"
    },
    {
        "name": "02_speed_end",
        "prompt": "Multiple afterimages of running figure, showing extreme speed, motion trails across the screen, dynamic anime scene, 960x960"
    },
    
    # 场景 3: 防御能力
    {
        "name": "03_defense_start",
        "prompt": "Energy shield barrier glowing, protective aura surrounding silhouette, orange and yellow light, anime defensive stance, 960x960"
    },
    {
        "name": "03_defense_end",
        "prompt": "Powerful attack hitting energy shield, impact explosion, shield holding strong, sparks flying, anime battle scene, 960x960"
    },
    
    # 场景 4: 特殊能力
    {
        "name": "04_ability_start",
        "prompt": "Spiriting energy ball in hand, blue swirling energy, anime jutsu style, glowing orb, dramatic lighting, 960x960"
    },
    {
        "name": "04_ability_end",
        "prompt": "Serious punch with massive energy trail, yellow energy beam, powerful strike, anime action scene, 960x960"
    },
    
    # 场景 5: 战斗经验
    {
        "name": "05_exp_start",
        "prompt": "Young ninja silhouette training, sunset background, determination in stance, anime flashback style, 960x960"
    },
    {
        "name": "05_exp_end",
        "prompt": "Mature warrior silhouette, confident stance, battle scars, experienced fighter aura, anime style, 960x960"
    },
    
    # 场景 6: 耐力对比
    {
        "name": "06_stamina_start",
        "prompt": "Two fighters standing, energy auras visible, beginning of long battle, dramatic sunset background, anime style, 960x960"
    },
    {
        "name": "06_stamina_end",
        "prompt": "Same fighters still standing after long battle, night sky, stars visible, both still fighting, anime endurance scene, 960x960"
    },
    
    # 场景 7: 成长潜力
    {
        "name": "07_growth_start",
        "prompt": "Timeline showing growth, small figure at start, arrow pointing forward, anime style infographic, 960x960"
    },
    {
        "name": "07_growth_end",
        "prompt": "Same figure now at peak, glowing with maximum power, golden aura, reached ceiling, anime powerup scene, 960x960"
    },
    
    # 场景 8: 综合评估
    {
        "name": "08_analysis_start",
        "prompt": "Radar chart comparison graphic, two colored areas overlapping, stats comparison, anime infographic style, 960x960"
    },
    {
        "name": "08_analysis_end",
        "prompt": "Question mark in center, two silhouettes on sides, thinking atmosphere, anime analysis scene, 960x960"
    },
    
    # 场景 9: 结尾
    {
        "name": "09_end_start",
        "prompt": "Two fighters facing each other, respectful stance, battle ended, sunset background, anime conclusion scene, 960x960"
    },
    {
        "name": "09_end_end",
        "prompt": "End screen with text '你支持谁？', comment icon, subscribe button, anime outro style, 960x960"
    },
]

def generate_image(prompt, output_path):
    """生成单张图片"""
    url = f"https://ark.cn-beijing.volces.com/api/v1/images/generations"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "seedance-1.5-pro",
        "prompt": prompt,
        "size": "960x960",
        "num_images": 1
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=120)
    
    if response.status_code == 200:
        result = response.json()
        if "data" in result and len(result["data"]) > 0:
            image_url = result["data"][0]["url"]
            
            # 下载图片
            img_response = requests.get(image_url, timeout=60)
            with open(output_path, "wb") as f:
                f.write(img_response.content)
            
            return True
        else:
            print(f"  ❌ 无图片数据：{result}")
            return False
    else:
        print(f"  ❌ API 错误：{response.status_code} - {response.text[:200]}")
        return False

def main():
    print("=" * 60)
    print("生成关键帧 - 一拳超人 vs 鸣人")
    print("=" * 60)
    
    total = len(PROMPTS)
    success = 0
    
    for i, item in enumerate(PROMPTS):
        name = item["name"]
        prompt = item["prompt"]
        output_path = f"{OUTPUT_DIR}/{name}.png"
        
        print(f"\n[{i+1}/{total}] 生成：{name}")
        
        if generate_image(prompt, output_path):
            print(f"  ✅ 成功：{output_path}")
            success += 1
        else:
            print(f"  ❌ 失败")
        
        # 避免限流
        if i < total - 1:
            time.sleep(2)
    
    print("\n" + "=" * 60)
    print(f"完成！成功：{success}/{total}")
    print("=" * 60)

if __name__ == "__main__":
    import time
    main()
