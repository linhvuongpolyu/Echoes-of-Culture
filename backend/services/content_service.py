from typing import Dict, Any, List

class ContentService:
    def __init__(self):
        self.content_data = self._initialize_content_data()
    
    def _initialize_content_data(self) -> Dict[str, Any]:
        """初始化内容数据"""
        return {
            '香港': {
                '语言模仿': {
                    'title': '粤语模仿',
                    'phrase': '你好 (nei5 hou2)',
                    'description': '学习粤语问候语',
                    'hint': '尝试模仿"nei5 hou2"的发音'
                },
                '画动物': {
                    'title': '中华白海豚',
                    'animal': '中华白海豚',
                    'description': '中华白海豚是香港水域的特色海洋动物，粉红色的外表非常可爱',
                    'image_hint': '尝试画出粉红色的海豚在蓝色海水中游动'
                },
                '视频问答1': {
                    'video_url': 'https://example.com/hongkong_video1.mp4',
                    'questions': [
                        {
                            "question": "香港的特色美食是什么？", 
                            "options": ["北京烤鸭", "上海小笼包", "港式奶茶", "四川火锅"], 
                            "answer": "港式奶茶"
                        },
                        {
                            "question": "香港的官方语言包括？", 
                            "options": ["只有英语", "只有普通话", "粤语和英语", "只有粤语"], 
                            "answer": "粤语和英语"
                        }
                    ]
                },
                '视频问答2': {
                    'video_url': 'https://example.com/hongkong_video2.mp4',
                    'questions': [
                        {
                            "question": "香港的别称是什么？", 
                            "options": ["东方之珠", "北方明珠", "南方之星", "西方宝石"], 
                            "answer": "东方之珠"
                        }
                    ]
                }
            },
            '中国': {
                # 类似结构，北京特定的内容
                '语言模仿': {
                    'title': '普通话模仿',
                    'phrase': '您好 (nín hǎo)',
                    'description': '学习普通话的正式问候语',
                    'hint': '注意"您"的发音比"你"更正式'
                },
                # ... 其他活动内容
            },
            '越南': {
                # 类似结构，越南特定的内容
                '语言模仿': {
                    'title': '越南语模仿',
                    'phrase': 'Xin chào',
                    'description': '学习越南语问候语',
                    'hint': '"Xin chào" 是越南语中的"你好"'
                },
                # ... 其他活动内容
            }
        }
    
    def get_content(self, city: str, activity: str) -> Dict[str, Any]:
        """获取指定城市和活动的内容"""
        if city not in self.content_data:
            raise ValueError(f"城市 '{city}' 不存在")
        
        if activity not in self.content_data[city]:
            raise ValueError(f"活动 '{activity}' 在城市 '{city}' 中不存在")
        
        return self.content_data[city][activity]
    
    def get_available_cities(self) -> List[str]:
        """获取可用的城市列表"""
        return list(self.content_data.keys())