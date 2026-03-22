#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
无限时长视频生成测试 - 使用 Project 001 关键帧

测试目标：验证首尾帧 chaining 能否生成流畅的长视频
测试方案：使用 6 张关键帧生成 5 段视频，然后合并
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path

# 添加 SDK 路径
sys.path.insert(0, '/home/jcs130/ai-long-video')
from volc_video_sdk import VolcVideo

# 配置
API_KEY = "8d27bf88-53b0-4656-9946-f21934f4f24b"
MODEL_ID = "ep-20260227022253-b67vh"  # 用户端点

# Project 001 关键帧路径
KEYFRAMES = [
    "/home/jcs130/ai-long-video/examples/project_001/source/frame1.jpeg",
    "/home/jcs130/ai-long-video/examples/project_001/source/frame2.jpeg",
    "/home/jcs130/ai-long-video/examples/project_001/source/frame3.jpeg",
    "/home/jcs130/ai-long-video/examples/project_001/source/frame4.jpeg",
    "/home/jcs130/ai-long-video/examples/project_001/source/frame5.jpeg",
    "/home/jcs130/ai-long-video/examples/project_001/source/frame6.jpeg",
]

OUTPUT_DIR = Path("/home/jcs130/ai-long-video/examples/project_001/test_infinite")
OUTPUT_DIR.mkdir(exist_ok=True)


def generate_chain_video(first_frame, last_frame, prompt, output_path, duration=12):
    """生成单段首尾帧视频"""
    print(f"🎬 生成：{first_frame.split('/')[-1]} → {last_frame.split('/')[-1]}")
    
    video = VolcVideo(api_key=API_KEY)
    
    try:
        result = video.generate_from_first_last_frames(
            first_frame_path=first_frame,
            last_frame_path=last_frame,
            prompt=prompt,
            model=MODEL_ID,
            duration=duration
        )
        
        # result 已经是 status 字典，包含 video_url
        video_url = result.get('video_url')
        if video_url:
            print(f"✅ 生成成功：{video_url}")
            # 直接下载到 output_path
            import requests
            response = requests.get(video_url)
            with open(output_path, 'wb') as f:
                f.write(response.content)
            print(f"💾 已保存：{output_path}")
            return output_path
        else:
            print(f"❌ 失败：{result}")
            return None
            
    except Exception as e:
        print(f"❌ 错误：{e}")
        return None


def merge_videos(segments, output_path):
    """合并视频片段"""
    print(f"\n🔗 合并 {len(segments)} 个片段...")
    
    # 创建合并列表
    list_file = OUTPUT_DIR / "concat_list.txt"
    with open(list_file, 'w') as f:
        for segment in segments:
            f.write(f"file '{segment}'\n")
    
    # FFmpeg 合并
    cmd = [
        'ffmpeg', '-f', 'concat', '-safe', '0',
        '-i', str(list_file),
        '-c', 'copy',
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ 合并成功：{output_path}")
        # 获取视频时长
        probe_cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(output_path)
        ]
        duration = subprocess.run(probe_cmd, capture_output=True, text=True).stdout.strip()
        print(f"⏱️  总时长：{float(duration):.2f}秒")
        return True
    else:
        print(f"❌ 合并失败：{result.stderr}")
        return False


def main():
    print("=" * 60)
    print("无限时长视频生成测试")
    print("=" * 60)
    print(f"📊 关键帧数量：{len(KEYFRAMES)}")
    print(f"📊 预计片段数：{len(KEYFRAMES) - 1}")
    print(f"📊 预计总时长：{(len(KEYFRAMES) - 1) * 12}秒")
    print()
    
    # 提示词序列（根据 Project 001 脚本）
    prompts = [
        "镜头推进，展现传统视频制作的复杂流程，创作者面对多个屏幕和素材库",
        "画面转换，出现 AI 界面，简洁现代的设计风格",
        "AI 自动处理画面，文案、分镜、视频生成的流程展示",
        "时间快速流逝，展示高效制作过程",
        "最终成品展示，数据看板显示低成本高回报"
    ]
    
    segments = []
    
    # 生成每个片段
    for i in range(len(KEYFRAMES) - 1):
        print(f"\n【片段 {i+1}/{len(KEYFRAMES)-1}】")
        output_path = OUTPUT_DIR / f"chain_segment_{i+1:02d}.mp4"
        
        # 如果已存在则跳过
        if output_path.exists():
            print(f"⏭️  已存在，跳过")
            segments.append(str(output_path))
            continue
        
        result = generate_chain_video(
            KEYFRAMES[i],
            KEYFRAMES[i+1],
            prompts[i],
            output_path,
            duration=12
        )
        
        if result:
            segments.append(str(result))
        else:
            print(f"⚠️  片段 {i+1} 失败，继续下一个")
    
    print("\n" + "=" * 60)
    print(f"✅ 生成完成：{len(segments)}/{len(KEYFRAMES)-1} 个片段")
    
    if len(segments) >= 2:
        # 合并视频
        final_output = OUTPUT_DIR / "infinite_test_final.mp4"
        merge_videos(segments, final_output)
        
        # 输出统计
        print("\n📊 测试统计:")
        print(f"   生成片段：{len(segments)}")
        print(f"   输出文件：{final_output}")
        if final_output.exists():
            size_mb = final_output.stat().st_size / 1024 / 1024
            print(f"   文件大小：{size_mb:.2f}MB")
    else:
        print("⚠️  片段太少，跳过合并")


if __name__ == "__main__":
    main()
