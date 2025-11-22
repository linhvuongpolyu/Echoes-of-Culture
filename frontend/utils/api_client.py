# frontend/utils/api_client.py
import requests
import streamlit as st

class StarAPIClient:
    def __init__(self, base_url="http://localhost:8500"):
        self.base_url = base_url
    
    def _make_request(self, endpoint, method='GET', data=None):
        """发送API请求"""
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method == 'GET':
                response = requests.get(url, timeout=5)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=5)
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API请求失败: {response.status_code}")
                return None
                
        except requests.exceptions.ConnectionError:
            st.error("无法连接到星星系统API服务器，请确保后端服务正在运行")
            return None
        except requests.exceptions.Timeout:
            st.error("API请求超时，请检查后端服务状态")
            return None
        except Exception as e:
            st.error(f"API请求错误: {e}")
            return None
    
    def update_stars(self, region, activity, stars):
        """更新星星数量"""
        endpoint = "/api/stars/update"
        data = {
            'region': region,
            'activity': activity,
            'stars': stars
        }
        return self._make_request(endpoint, 'POST', data)
    
    def get_stars(self, region=None):
        """获取星星数据"""
        endpoint = "/api/stars"
        if region:
            endpoint += f"?region={region}"
        return self._make_request(endpoint)
    
    def get_overall_stats(self):
        """获取总体统计"""
        endpoint = "/api/stats/overall"
        return self._make_request(endpoint)
    
    def health_check(self):
        """健康检查"""
        endpoint = "/api/health"
        return self._make_request(endpoint)

# 创建全局API客户端实例
star_client = StarAPIClient()