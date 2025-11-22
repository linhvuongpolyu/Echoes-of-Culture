# backend/api_server.py
from flask import Flask, jsonify, request
from flask_cors import CORS
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

class StarManager:
    def __init__(self):
        # 数据文件放在项目根目录的 data 文件夹中
        self.project_root = Path(__file__).parent.parent
        self.data_file = self.project_root / "data" / "stars.json"
        self.data_file.parent.mkdir(exist_ok=True)
        self._ensure_default_data()
    
    def _ensure_default_data(self):
        """确保数据文件存在并有默认结构"""
        if not self.data_file.exists():
            default_data = {
                'Hong Kong': {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0},
                'China': {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0},
                'Vietnam': {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0}
            }
            self._save_data(default_data)
    
    def _load_data(self):
        """加载数据"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载数据失败: {e}")
            return {}
    
    def _save_data(self, data):
        """保存数据"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存数据失败: {e}")
            return False
    
    def update_stars(self, region, activity, stars):
        """更新星星数量"""
        data = self._load_data()
        
        # 确保地区存在
        if region not in data:
            data[region] = {'Language Imitation': 0, 'Draw Animals': 0, 'Food': 0, 'Performance': 0}
        
        # 更新星星数量
        data[region][activity] = stars
        
        success = self._save_data(data)
        return success
    
    def get_stars(self, region=None):
        """获取星星数据"""
        data = self._load_data()
        
        if region:
            return data.get(region, {})
        else:
            return data
    
    def get_total_stars(self, region=None):
        """获取总星星数量"""
        data = self._load_data()
        
        if region:
            region_data = data.get(region, {})
            return sum(region_data.values())
        else:
            total = 0
            for region_data in data.values():
                total += sum(region_data.values())
            return total