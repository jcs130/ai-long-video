#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project 003: 木屋烧烤宣传视频 - 生成关键帧
雨夜海边，两个男人吃烧烤谈人生
"""

import sys
sys.path.insert(0, '/home/jcs130/.copaw/active_skills')

from volc_multimedia_sdk import VolcImage
import os
import time

# 配置
API_KEY = "8d27bf88-53b0-4656-9946-f21934f4f24b"
MODEL = "ep-20260227121917-j9vll"  # Seedream-5.0-lite

OUTPUT_DIR = "/home/jcs130/.copaw/workspaces/64cKss/media/project_003/keyframes"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 20 个关键帧提示词（电影质感，雨夜烧烤）
PROMPTS = [
    # 场景 0: 开场（5s）
    ("00_start", "Rainy night beach scene, wooden BBQ restaurant sign glowing with warm yellow light in rain, ocean waves in background, cinematic mood, deep blue and warm yellow contrast, photorealistic, 1920x1920"),
    ("00_end", "Close-up of wooden BBQ sign at rainy night, warm yellow light creating halo effect in raindrops, cozy atmosphere, cinematic lighting, photorealistic, 1920x1920"),
    
    # 场景 1: 推近（3s）
    ("01_start", "Medium shot of outdoor BBQ stall at night, charcoal fire with sparks and steam rising, rainy dark background, warm lighting on food, cinematic food scene, 1920x1920"),
    ("01_end", "Extreme close-up of burning charcoal, red hot coals with flying sparks, heat waves visible, macro food photography, professional shot, 1920x1920"),
    
    # 场景 2: 人物登场（4s）
    ("02_start", "Two middle-aged Asian men sitting at wooden table outdoors, rain drops falling from eaves, warm yellow light illuminating faces, side profile view, rainy night atmosphere, cinematic, 1920x1920"),
    ("02_end", "Front view of two men at table, casual clothing, beer bottles and BBQ skewers on table, natural smiles, rainy night background, cinematic portrait, photorealistic, 1920x1920"),
    
    # 场景 3: 烤肉特写（4s）
    ("03_start", "Close-up of meat skewers grilling over charcoal fire, oil dripping onto coals creating smoke, hand sprinkling cumin and chili powder, professional food photography, 1920x1920"),
    ("03_end", "Perfectly grilled meat skewers close-up, golden brown and crispy texture, glossy with oil, covered in red chili and cumin seeds, appetizing, macro shot, 1920x1920"),
    
    # 场景 4: 回忆（4s）
    ("04_start", "Asian man side profile close-up, smiling and shaking head slightly, eyes full of memories and stories, warm light on face, rainy night background blurred, cinematic emotion, 1920x1920"),
    ("04_end", "Same man front view, nostalgic smile with visible laugh lines, wrinkles at eye corners showing middle age, life experience in expression, cinematic portrait quality, 1920x1920"),
    
    # 场景 5: 吃肉（4s）
    ("05_start", "Asian man picking up meat skewer with hand, about to take big bite, anticipatory happy expression, warm lighting, food in sharp focus, 1920x1920"),
    ("05_end", "Same man eating meat with great satisfaction, slight oil on lips, eyes closed enjoying food, authentic genuine expression, slice of life feeling, 1920x1920"),
    
    # 场景 6: 倒酒（4s）
    ("06_start", "Brown beer bottle tilting, golden beer liquid pouring into clear glass, white foam rising, slow motion capture, liquid photography, 1920x1920"),
    ("06_end", "Full beer glass with thick white foam overflowing top, cold water droplets on glass surface, refreshing cold look, extreme close-up, commercial photography, 1920x1920"),
    
    # 场景 7: 感悟（6s）
    ("07_start", "Asian man profile looking out at dark ocean, contemplative thoughtful expression, rain drops falling from roof edge, deep blue sea background, moody atmosphere, 1920x1920"),
    ("07_end", "Same man front view with realization expression, determined eyes, mature man's wisdom, warm light on face vs cool blue background contrast, cinematic lighting, 1920x1920"),
    
    # 场景 8: 碰杯（6s）
    ("08_start", "Two men raising beer glasses together, about to toast clink, sincere warm smiles, golden beer with foam in glasses, medium shot, brotherhood moment, 1920x1920"),
    ("08_end", "Beer glasses clinking moment captured, white foam splashing from impact, both men laughing genuinely, brotherhood emotion, warm atmosphere, close-up shot, 1920x1920"),
    
    # 场景 9: 品牌（10s）
    ("09_start", "Camera pulling back wide shot, full view of wooden BBQ restaurant building, warm yellow lights glowing in rainy night, two men still chatting at outdoor table, long shot, 1920x1920"),
    ("09_end", "Wide establishing shot of wooden BBQ restaurant sign, rainy night beach setting, warm yellow light illuminating surroundings and sign, brand logo clearly visible, cinematic ending frame, 1920x1920")
]

def main():
    print("=" * 60)
    print("Project 003: 木屋烧烤 - 生成关键帧")
    print("=" * 60)
    
    img = VolcImage(api_key=API_KEY)
    
    total = len(PROMPTS)
    success = 0
    
    for i, (name, prompt) in enumerate(PROMPTS):
        output_path = f"{OUTPUT_DIR}/{name}.png"
        
        print(f"\n[{i+1}/{total}] 生成：{name}")
        print(f"  提示词：{prompt[:80]}...")
        
        try:
            result = img.generate(
                prompt=prompt,
                size="1920x1920",
                model=MODEL
            )
            
            if result and result.get('urls'):
                # 下载图片
                img_url = result['urls'][0]
                img_data = requests.get(img_url).content
                with open(output_path, 'wb') as f:
                    f.write(img_data)
                
                print(f"  ✅ 成功：{output_path}")
                success += 1
            else:
                print(f"  ❌ 失败：{result}")
        except Exception as e:
            print(f"  ❌ 错误：{e}")
        
        # 避免限流
        if i < total - 1:
            time.sleep(2)
    
    print("\n" + "=" * 60)
    print(f"✅ 完成！成功：{success}/{total}")
    print(f"📁 输出目录：{OUTPUT_DIR}")
    print("=" * 60)

if __name__ == "__main__":
    import requests
    main()
