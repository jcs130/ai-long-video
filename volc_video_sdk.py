"""
火山引擎视频生成 SDK 封装 (Volcengine Video Generation)
支持 Seedance 1.5 Pro 模型，提供文生视频、首帧生视频、首尾帧生视频等功能
"""

import os
import time
import requests
import logging
from typing import Optional, Dict, Any, List
from volcenginesdkarkruntime import Ark

# 自我进化集成 - 自动反馈收集 + 重试机制（可选依赖）
try:
    from skill_evolution_manager.auto_feedback import auto_feedback
    from tenacity import retry, stop_after_attempt, wait_exponential
    HAS_EVOLUTION = True
except ImportError:
    HAS_EVOLUTION = False
    # 如果没有安装 skill_evolution_manager，使用空装饰器
    def auto_feedback(*args, **kwargs):
        """空装饰器，当 skill_evolution_manager 未安装时"""
        def decorator(func):
            return func
        return decorator
    
    def retry(**kwargs):
        """空装饰器，当 tenacity 未安装时"""
        def decorator(func):
            return func
        return decorator
    
    def stop_after_attempt(n):
        return n
    
    def wait_exponential(**kwargs):
        return 0


class VolcVideo:
    """火山引擎视频生成客户端（支持 Seedance 1.5 Pro）"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化视频生成客户端
        
        Args:
            api_key: API Key，默认从环境变量读取
        """
        self.api_key = api_key or os.getenv("ARK_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未设置，请传入 api_key 或设置 ARK_API_KEY 环境变量")
        
        self.client = Ark(
            base_url="https://ark.cn-beijing.volces.com/api/v3",
            api_key=self.api_key,
        )
    
    def _build_content(self, prompt: str, watermark: bool, duration: int) -> List[Dict]:
        """构建视频生成请求的 content 参数"""
        params_text = f"{prompt} --wm {'true' if watermark else 'false'} --dur {duration}"
        return [{"type": "text", "text": params_text}]
    
    def _build_content_with_image(
        self,
        prompt: str,
        image_path: str,
        watermark: bool,
        duration: int,
        image_type: str = "first_frame"
    ) -> List[Dict]:
        """构建带图片的视频生成请求 content 参数"""
        params_text = f"--wm {'true' if watermark else 'false'} --dur {duration}"
        
        import base64
        with open(image_path, 'rb') as f:
            image_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        content = []
        
        image_item = {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{image_base64}"
            },
            "role": image_type
        }
        
        content.append(image_item)
        
        text_content = f"{prompt} {params_text}" if prompt else params_text
        content.append({
            "type": "text",
            "text": text_content
        })
        
        return content
    
    def create_task(
        self,
        prompt: str,
        model: str = "ep-20260227022253-b67vh",
        watermark: bool = True,
        duration: int = 5
    ) -> str:
        """
        创建文生视频任务
        
        Args:
            prompt: 视频描述提示词
            model: 模型 ID
            watermark: 是否添加水印
            duration: 视频时长（秒）- 仅支持 5 或 10
            
        Returns:
            任务 ID
        """
        if duration not in [5, 10]:
            duration = 5
        
        content = self._build_content(prompt, watermark, duration)
        
        result = self.client.content_generation.tasks.create(
            model=model,
            content=content
        )
        
        return result.id
    
    def create_task_with_first_frame(
        self,
        image_path: str,
        prompt: str = "",
        model: str = "ep-20260227022253-b67vh",
        watermark: bool = True,
        duration: int = 5
    ) -> str:
        """
        创建首帧生视频任务
        
        Args:
            image_path: 首帧图片路径
            prompt: 视频描述（可选）
            model: 模型 ID
            watermark: 是否添加水印
            duration: 视频时长（5 或 10 秒）
            
        Returns:
            任务 ID
        """
        if duration not in [5, 10]:
            duration = 5
        
        content = self._build_content_with_image(
            prompt, image_path, watermark, duration, "first_frame"
        )
        
        result = self.client.content_generation.tasks.create(
            model=model,
            content=content
        )
        
        return result.id
    
    def create_task_with_first_last_frames(
        self,
        first_frame_path: str,
        last_frame_path: str,
        prompt: str = "",
        model: str = "ep-20260227022253-b67vh",
        watermark: bool = True,
        duration: int = 5
    ) -> str:
        """
        创建首尾帧生视频任务（关键帧插值）
        
        Args:
            first_frame_path: 首帧图片路径
            last_frame_path: 尾帧图片路径
            prompt: 视频描述（可选）
            model: 模型 ID
            watermark: 是否添加水印
            duration: 视频时长（5 或 10 秒）
            
        Returns:
            任务 ID
        """
        if duration not in [5, 10]:
            duration = 5
        
        import base64
        
        with open(first_frame_path, 'rb') as f:
            first_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        with open(last_frame_path, 'rb') as f:
            last_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        params_text = f"--wm {'true' if watermark else 'false'} --dur {duration}"
        if prompt:
            params_text = f"{prompt} {params_text}"
        
        content = [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{first_base64}"
                },
                "role": "first_frame"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{last_base64}"
                },
                "role": "last_frame"
            },
            {
                "type": "text",
                "text": params_text
            }
        ]
        
        result = self.client.content_generation.tasks.create(
            model=model,
            content=content
        )
        
        return result.id
    
    def create_task_with_reference(
        self,
        prompt: str,
        reference_image_path: str,
        model: str = "ep-20260227022253-b67vh",
        watermark: bool = True,
        duration: int = 5
    ) -> str:
        """
        创建图生视频任务（带参考图）
        
        Args:
            prompt: 视频描述
            reference_image_path: 参考图片路径
            model: 模型 ID
            watermark: 是否添加水印
            duration: 视频时长
            
        Returns:
            任务 ID
        """
        import base64
        
        if duration not in [5, 10]:
            duration = 5
        
        with open(reference_image_path, 'rb') as f:
            ref_base64 = base64.b64encode(f.read()).decode('utf-8')
        
        content = [
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{ref_base64}"
                },
                "role": "reference_image"
            },
            {
                "type": "text",
                "text": f"{prompt} --wm {'true' if watermark else 'false'} --dur {duration}"
            }
        ]
        
        result = self.client.content_generation.tasks.create(
            model=model,
            content=content
        )
        
        return result.id
    
    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        """查询任务状态"""
        result = self.client.content_generation.tasks.get(task_id=task_id)
        
        return {
            "id": result.id,
            "status": result.status,
            "video_url": result.content.video_url if hasattr(result.content, 'video_url') else None,
            "error": result.error if hasattr(result, 'error') else None,
            "usage": result.usage if hasattr(result, 'usage') else None,
            "raw": result
        }
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    @auto_feedback(skill_name="volc_video")
    def generate(
        self,
        prompt: str,
        model: str = "doubao-seedance-1-5-pro-250528",
        watermark: bool = True,
        duration: int = 5,
        poll_interval: int = 5,
        timeout: int = 600,
        max_retries: int = 3,
        retry_delay: int = 10
    ) -> Dict[str, Any]:
        """
        生成视频（同步等待完成）- 文生视频
        
        Args:
            prompt: 视频描述
            model: 模型 ID
            watermark: 是否添加水印
            duration: 视频时长
            poll_interval: 轮询间隔（秒）- 默认 5 秒
            timeout: 超时时间（秒）- 默认 600 秒 (10 分钟)
            max_retries: 最大重试次数 - 默认 3 次
            retry_delay: 重试延迟（秒）- 默认 10 秒，指数退避
            
        Returns:
            视频信息字典
            
        Raises:
            TimeoutError: 视频生成超时
            Exception: 视频生成失败
            ConnectionError: 网络错误（重试后仍失败）
        """
        logger = logging.getLogger(__name__)
        
        last_error = None
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    wait_time = retry_delay * (2 ** (attempt - 1))
                    logger.warning(f"视频生成重试 {attempt}/{max_retries}，等待 {wait_time}秒...")
                    time.sleep(wait_time)
                
                task_id = self.create_task(prompt, model, watermark, duration)
                logger.info(f"视频任务创建成功，Task ID: {task_id}")
                
                start_time = time.time()
                last_status = None
                
                while True:
                    if time.time() - start_time > timeout:
                        raise TimeoutError(f"视频生成超时 ({timeout}秒)，Task ID: {task_id}")
                    
                    status = self.get_task_status(task_id)
                    
                    if status["status"] != last_status:
                        logger.info(f"视频任务状态：{task_id} -> {status['status']}")
                        last_status = status["status"]
                    
                    if status["status"] == "succeeded":
                        logger.info(f"视频生成成功：{status['video_url']}")
                        return status
                    elif status["status"] == "failed":
                        error_msg = f"视频生成失败：{status['error']}"
                        logger.error(error_msg)
                        raise Exception(error_msg)
                    
                    time.sleep(poll_interval)
                    
            except (TimeoutError, Exception) as e:
                last_error = e
                logger.error(f"视频生成尝试 {attempt + 1}/{max_retries} 失败：{str(e)}")
                if attempt >= max_retries - 1:
                    logger.error(f"视频生成最终失败，已重试 {max_retries} 次")
                    raise
                continue
        
        raise ConnectionError(f"视频生成失败，已重试 {max_retries} 次：{str(last_error)}")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    @auto_feedback(skill_name="volc_video")
    def generate_from_first_frame(
        self,
        image_path: str,
        prompt: str = "",
        model: str = "ep-20260227022253-b67vh",
        watermark: bool = True,
        duration: int = 5,
        poll_interval: int = 5,
        timeout: int = 600,
        max_retries: int = 3,
        retry_delay: int = 10
    ) -> Dict[str, Any]:
        """
        首帧生视频（同步等待）
        
        Args:
            image_path: 首帧图片路径
            prompt: 视频描述
            model: 模型 ID
            watermark: 是否添加水印
            duration: 视频时长
            poll_interval: 轮询间隔（秒）- 默认 5 秒
            timeout: 超时时间（秒）- 默认 600 秒 (10 分钟)
            max_retries: 最大重试次数 - 默认 3 次
            retry_delay: 重试延迟（秒）- 指数退避
            
        Returns:
            视频信息字典
        """
        logger = logging.getLogger(__name__)
        
        last_error = None
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    wait_time = retry_delay * (2 ** (attempt - 1))
                    logger.warning(f"首帧视频生成重试 {attempt}/{max_retries}，等待 {wait_time}秒...")
                    time.sleep(wait_time)
                
                task_id = self.create_task_with_first_frame(image_path, prompt, model, watermark, duration)
                logger.info(f"首帧视频任务创建成功，Task ID: {task_id}")
                
                start_time = time.time()
                last_status = None
                
                while True:
                    if time.time() - start_time > timeout:
                        raise TimeoutError(f"视频生成超时 ({timeout}秒)，Task ID: {task_id}")
                    
                    status = self.get_task_status(task_id)
                    
                    if status["status"] != last_status:
                        logger.info(f"视频任务状态：{task_id} -> {status['status']}")
                        last_status = status["status"]
                    
                    if status["status"] == "succeeded":
                        logger.info(f"视频生成成功：{status['video_url']}")
                        return status
                    elif status["status"] == "failed":
                        error_msg = f"视频生成失败：{status['error']}"
                        logger.error(error_msg)
                        raise Exception(error_msg)
                    
                    time.sleep(poll_interval)
                    
            except (TimeoutError, Exception) as e:
                last_error = e
                logger.error(f"首帧视频生成尝试 {attempt + 1}/{max_retries} 失败：{str(e)}")
                if attempt >= max_retries - 1:
                    raise
                continue
        
        raise ConnectionError(f"首帧视频生成失败，已重试 {max_retries} 次：{str(last_error)}")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    @auto_feedback(skill_name="volc_video")
    def generate_from_first_last_frames(
        self,
        first_frame_path: str,
        last_frame_path: str,
        prompt: str = "",
        model: str = "ep-20260227022253-b67vh",
        watermark: bool = True,
        duration: int = 5,
        poll_interval: int = 5,
        timeout: int = 600,
        max_retries: int = 3,
        retry_delay: int = 10
    ) -> Dict[str, Any]:
        """
        首尾帧生视频（同步等待）
        
        Args:
            first_frame_path: 首帧图片路径
            last_frame_path: 尾帧图片路径
            prompt: 视频描述
            model: 模型 ID
            watermark: 是否添加水印
            duration: 视频时长
            poll_interval: 轮询间隔（秒）- 默认 5 秒
            timeout: 超时时间（秒）- 默认 600 秒 (10 分钟)
            max_retries: 最大重试次数 - 默认 3 次
            retry_delay: 重试延迟（秒）- 指数退避
            
        Returns:
            视频信息字典
        """
        logger = logging.getLogger(__name__)
        
        last_error = None
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    wait_time = retry_delay * (2 ** (attempt - 1))
                    logger.warning(f"首尾帧视频生成重试 {attempt}/{max_retries}，等待 {wait_time}秒...")
                    time.sleep(wait_time)
                
                task_id = self.create_task_with_first_last_frames(
                    first_frame_path, last_frame_path, prompt, model, watermark, duration
                )
                logger.info(f"首尾帧视频任务创建成功，Task ID: {task_id}")
                
                start_time = time.time()
                last_status = None
                
                while True:
                    if time.time() - start_time > timeout:
                        raise TimeoutError(f"视频生成超时 ({timeout}秒)，Task ID: {task_id}")
                    
                    status = self.get_task_status(task_id)
                    
                    if status["status"] != last_status:
                        logger.info(f"视频任务状态：{task_id} -> {status['status']}")
                        last_status = status["status"]
                    
                    if status["status"] == "succeeded":
                        logger.info(f"视频生成成功：{status['video_url']}")
                        return status
                    elif status["status"] == "failed":
                        error_msg = f"视频生成失败：{status['error']}"
                        logger.error(error_msg)
                        raise Exception(error_msg)
                    
                    time.sleep(poll_interval)
                    
            except (TimeoutError, Exception) as e:
                last_error = e
                logger.error(f"首尾帧视频生成尝试 {attempt + 1}/{max_retries} 失败：{str(e)}")
                if attempt >= max_retries - 1:
                    raise
                continue
        
        raise ConnectionError(f"首尾帧视频生成失败，已重试 {max_retries} 次：{str(last_error)}")
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    @auto_feedback(skill_name="volc_video")
    def generate_and_save(
        self,
        prompt: str,
        output_path: str,
        max_retries: int = 3,
        retry_delay: int = 10,
        **kwargs
    ) -> str:
        """
        生成视频并保存到本地（带重试机制）
        
        Args:
            prompt: 视频描述
            output_path: 保存路径
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
            **kwargs: 传递给 generate() 的参数
            
        Returns:
            保存的文件路径
        """
        logger = logging.getLogger(__name__)
        
        last_error = None
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    wait_time = retry_delay * (2 ** (attempt - 1))
                    logger.warning(f"视频下载重试 {attempt}/{max_retries}，等待 {wait_time}秒...")
                    time.sleep(wait_time)
                
                result = self.generate(prompt, **kwargs)
                video_url = result["video_url"]
                
                if not video_url:
                    raise ValueError("未获取到视频 URL")
                
                logger.info(f"下载视频：{video_url}")
                response = requests.get(video_url, timeout=60)
                response.raise_for_status()
                
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                
                logger.info(f"视频已保存：{output_path}")
                return output_path
                
            except Exception as e:
                last_error = e
                logger.error(f"视频生成/保存尝试 {attempt + 1}/{max_retries} 失败：{str(e)}")
                if attempt >= max_retries - 1:
                    raise
                continue
        
        raise ConnectionError(f"视频生成/保存失败，已重试 {max_retries} 次：{str(last_error)}")


# 便捷函数
def video_generate(prompt: str, **kwargs) -> Dict[str, Any]:
    """便捷函数：视频生成"""
    vid = VolcVideo()
    return vid.generate(prompt, **kwargs)


def video_generate_from_image(image_path: str, prompt: str = "", **kwargs) -> Dict[str, Any]:
    """便捷函数：首帧生视频"""
    vid = VolcVideo()
    return vid.generate_from_first_frame(image_path, prompt=prompt, **kwargs)


if __name__ == "__main__":
    # 测试示例
    print("火山引擎视频生成 SDK")
    print("==================")
    print("使用示例:")
    print('  from volc_video_sdk import video_generate')
    print('  result = video_generate("一只小猫在草地上奔跑", duration=5)')
    print('  print(result["video_url"])')
    print("\n⚠️ 注意：视频时长仅支持 5 或 10 秒")
