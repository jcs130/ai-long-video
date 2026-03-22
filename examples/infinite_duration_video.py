#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
无限时长视频生成示例 - 通过首尾帧拼接实现任意时长

原理:
1. 生成一系列关键帧（场景变化点）
2. 使用首尾帧功能生成相邻关键帧之间的过渡视频
3. 合并所有视频片段得到完整长视频

优势:
- 突破单段 12 秒限制
- 理论上可生成任意时长视频
- 过渡流畅，无硬切痕迹
"""

import os
import sys
import subprocess
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from volc_video_sdk import VolcVideoSDK

# 配置 API Key（从环境变量读取）
API_KEY = os.getenv("VOLC_API_KEY")
if not API_KEY:
    raise ValueError("请设置 VOLC_API_KEY 环境变量")

sdk = VolcVideoSDK(api_key=API_KEY)


def generate_keyframes(scenes, output_dir="keyframes"):
    """
    生成关键帧序列
    
    Args:
        scenes: 场景描述列表
        output_dir: 输出目录
    
    Returns:
        关键帧文件路径列表
    """
    Path(output_dir).mkdir(exist_ok=True)
    keyframes = []
    
    for i, scene in enumerate(scenes):
        print(f"🎨 生成关键帧 {i+1}/{len(scenes)}: {scene[:30]}...")
        # 这里可以使用 VolcImage 生成关键帧
        # 为简化示例，假设已有图片文件
        keyframe_path = f"{output_dir}/frame_{i:03d}.jpg"
        keyframes.append(keyframe_path)
    
    return keyframes


def generate_segments(keyframes, output_dir="segments", duration=12):
    """
    生成视频片段（相邻关键帧之间的过渡）
    
    Args:
        keyframes: 关键帧路径列表
        output_dir: 输出目录
        duration: 每段时长（秒）
    
    Returns:
        视频片段路径列表
    """
    Path(output_dir).mkdir(exist_ok=True)
    segments = []
    
    for i in range(len(keyframes) - 1):
        print(f"🎬 生成片段 {i+1}/{len(keyframes)-1}")
        
        video = sdk.generate_from_first_last_frames(
            first_frame_path=keyframes[i],
            last_frame_path=keyframes[i+1],
            prompt="流畅自然的过渡",
            duration=duration
        )
        
        segment_path = f"{output_dir}/segment_{i:03d}.mp4"
        # 下载视频到本地（实际使用时需要实现下载逻辑）
        # download_video(video['video_url'], segment_path)
        segments.append(segment_path)
    
    return segments


def merge_videos(segments, output_path="final_video.mp4"):
    """
    使用 FFmpeg 合并所有视频片段
    
    Args:
        segments: 视频片段路径列表
        output_path: 输出文件路径
    """
    # 创建文件列表
    list_file = "video_list.txt"
    with open(list_file, 'w') as f:
        for segment in segments:
            f.write(f"file '{segment}'\n")
    
    # 使用 FFmpeg 合并
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', list_file,
        '-c', 'copy',
        output_path
    ]
    
    print(f"🔗 合并 {len(segments)} 个片段...")
    subprocess.run(cmd, check=True)
    
    # 清理临时文件
    os.remove(list_file)
    
    print(f"✅ 视频已生成：{output_path}")


def main():
    """
    完整流程示例：生成 60 秒视频（5 段 × 12 秒）
    """
    print("=" * 60)
    print("无限时长视频生成示例")
    print("=" * 60)
    
    # 定义场景序列（6 个关键场景）
    scenes = [
        "清晨，阳光透过窗户洒进房间",
        "主角起床，伸懒腰",
        "洗漱完毕，穿上正装",
        "出门，走在街道上",
        "到达办公室，开始工作",
        "傍晚，夕阳西下"
    ]
    
    print(f"\n📋 场景数量：{len(scenes)}")
    print(f"📊 预计时长：{(len(scenes)-1) * 12}秒")
    print(f"📊 片段数量：{len(scenes)-1}")
    
    # 步骤 1: 生成关键帧
    print("\n【步骤 1】生成关键帧...")
    keyframes = generate_keyframes(scenes, output_dir="keyframes")
    
    # 步骤 2: 生成视频片段
    print("\n【步骤 2】生成视频片段...")
    segments = generate_segments(keyframes, output_dir="segments", duration=12)
    
    # 步骤 3: 合并视频
    print("\n【步骤 3】合并视频...")
    merge_videos(segments, output_path="final_60s_video.mp4")
    
    print("\n✅ 完成！")
    print(f"📹 最终视频：final_60s_video.mp4")
    print(f"⏱️  总时长：{(len(scenes)-1) * 12}秒")


if __name__ == "__main__":
    main()
