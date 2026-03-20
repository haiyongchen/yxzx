#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新点e交易专区信息抓取脚本
功能：从 https://www.etrading.cn/ 抓取所有专区名称和URL
输出：Excel文件
"""

import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, WebDriverException
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ZoneFetcher:
    """专区信息抓取器"""
    
    def __init__(self, headless=False):
        self.driver = None
        self.wait = None
        self.headless = headless
        self.base_url = "https://www.etrading.cn/"
        self.zones_data = []
        
    def init_driver(self):
        """初始化Chrome浏览器"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(30)
            self.wait = WebDriverWait(self.driver, 15)
            
            logger.info("Chrome浏览器初始化成功")
            return True
            
        except WebDriverException as e:
            logger.error(f"浏览器初始化失败: {e}")
            return False
    
    def close_driver(self):
        """关闭浏览器"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("浏览器已关闭")
            except Exception as e:
                logger.warning(f"关闭浏览器时出错: {e}")
    
    def open_page(self):
        """打开总站页面"""
        try:
            self.driver.get(self.base_url)
            logger.info(f"已打开页面: {self.base_url}")
            time.sleep(3)  # 等待页面加载
            return True
        except Exception as e:
            logger.error(f"打开页面失败: {e}")
            return False
    
    def click_zone_selector(self):
        """点击专区选择按钮"""
        try:
            # 尝试多种方式定位"专区选择"按钮
            selectors = [
                "//span[contains(text(),'专区选择')]",
                "//a[contains(text(),'专区选择')]",
                "//div[contains(@class,'zone')]//span",
                "//div[contains(@class,'select')]//span",
            ]
            
            for selector in selectors:
                try:
                    zone_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    zone_btn.click()
                    logger.info(f"已点击'专区选择'按钮 (selector: {selector})")
                    time.sleep(2)
                    return True
                except:
                    continue
            
            # 如果上面都失败，尝试通过class找
            try:
                zone_btn = self.driver.find_element(By.CLASS_NAME, "zone-selector")
                zone_btn.click()
                logger.info("已点击'专区选择'按钮 (class)")
                time.sleep(2)
                return True
            except:
                pass
            
            logger.error("无法找到'专区选择'按钮")
            return False
            
        except Exception as e:
            logger.error(f"点击专区选择按钮失败: {e}")
            return False
    
    def get_all_zones(self):
        """
        获取所有专区信息
        根据截图中的HTML结构：
        <li class="hot-item l">
            <a href="http://dtzhztb.etrading.cn/" target="_blank">大田智慧招投标平台</a>
        </li>
        """
        try:
            # 等待专区列表加载
            logger.info("正在等待专区列表加载...")
            
            # 根据截图中的结构，查找所有hot-item
            zone_items = self.driver.find_elements(By.XPATH, "//li[contains(@class,'hot-item')]")
            
            if not zone_items:
                # 尝试其他可能的class
                zone_items = self.driver.find_elements(By.XPATH, "//li[@class='hot-item l']")
            
            if not zone_items:
                # 尝试更通用的方式
                zone_items = self.driver.find_elements(By.XPATH, "//ul[contains(@class,'hot-list')]//li")
            
            logger.info(f"找到 {len(zone_items)} 个专区项")
            
            for item in zone_items:
                try:
                    # 获取链接元素
                    link = item.find_element(By.TAG_NAME, "a")
                    url = link.get_attribute("href")
                    name = link.text.strip()
                    
                    if url and name:
                        self.zones_data.append({
                            '专区名称': name,
                            '专区地址': url
                        })
                        logger.info(f"获取到: {name} -> {url}")
                        
                except Exception as e:
                    logger.warning(f"解析专区项时出错: {e}")
                    continue
            
            logger.info(f"共获取到 {len(self.zones_data)} 个专区")
            return len(self.zones_data) > 0
            
        except Exception as e:
            logger.error(f"获取专区列表失败: {e}")
            return False
    
    def scroll_and_get_more(self):
        """滚动页面获取更多专区"""
        try:
            # 尝试滚动页面
            last_count = 0
            scroll_attempts = 0
            max_attempts = 5
            
            while scroll_attempts < max_attempts:
                # 滚动到底部
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # 重新获取
                zone_items = self.driver.find_elements(By.XPATH, "//li[contains(@class,'hot-item')]")
                current_count = len(zone_items)
                
                if current_count == last_count:
                    scroll_attempts += 1
                else:
                    last_count = current_count
                    scroll_attempts = 0
                    logger.info(f"滚动后找到 {current_count} 个专区项")
            
            return True
            
        except Exception as e:
            logger.warning(f"滚动获取更多时出错: {e}")
            return False
    
    def save_to_excel(self, output_path="zones_output.xlsx"):
        """保存到Excel"""
        try:
            if not self.zones_data:
                logger.error("没有数据可保存")
                return False
            
            df = pd.DataFrame(self.zones_data)
            df.to_excel(output_path, index=False, engine='openpyxl')
            logger.info(f"数据已保存到: {output_path}")
            logger.info(f"共 {len(df)} 条记录")
            return True
            
        except Exception as e:
            logger.error(f"保存Excel失败: {e}")
            return False
    
    def run(self, output_path="zones_output.xlsx"):
        """运行抓取流程"""
        logger.info("=" * 50)
        logger.info("开始抓取新点e交易专区信息")
        logger.info("=" * 50)
        
        # 初始化浏览器
        if not self.init_driver():
            return False
        
        try:
            # 打开页面
            if not self.open_page():
                return False
            
            # 点击专区选择
            if not self.click_zone_selector():
                logger.warning("点击专区选择失败，尝试直接获取页面内容")
            
            # 等待内容加载
            time.sleep(3)
            
            # 尝试滚动获取更多
            self.scroll_and_get_more()
            
            # 获取所有专区
            if not self.get_all_zones():
                logger.error("获取专区失败")
                return False
            
            # 保存到Excel
            if not self.save_to_excel(output_path):
                return False
            
            logger.info("=" * 50)
            logger.info("抓取完成！")
            logger.info("=" * 50)
            return True
            
        except Exception as e:
            logger.error(f"运行过程中出错: {e}")
            return False
        finally:
            self.close_driver()


class ZoneFetcherRequests:
    """使用requests的备用方案（如果Selenium失败）"""
    
    def __init__(self):
        self.zones_data = []
        
    def fetch_with_requests(self, output_path="zones_output.xlsx"):
        """使用requests和BeautifulSoup抓取"""
        try:
            import requests
            from bs4 import BeautifulSoup
            
            logger.info("使用requests方式抓取...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get("https://www.etrading.cn/", headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找所有hot-item
            zone_items = soup.find_all('li', class_=lambda x: x and 'hot-item' in x)
            
            logger.info(f"找到 {len(zone_items)} 个专区项")
            
            for item in zone_items:
                try:
                    link = item.find('a')
                    if link:
                        url = link.get('href', '')
                        name = link.get_text(strip=True)
                        
                        if url and name:
                            self.zones_data.append({
                                '专区名称': name,
                                '专区地址': url
                            })
                            logger.info(f"获取到: {name} -> {url}")
                except Exception as e:
                    logger.warning(f"解析项时出错: {e}")
                    continue
            
            # 保存
            if self.zones_data:
                df = pd.DataFrame(self.zones_data)
                df.to_excel(output_path, index=False, engine='openpyxl')
                logger.info(f"数据已保存到: {output_path} (共 {len(df)} 条)")
                return True
            else:
                logger.error("未获取到任何数据")
                return False
                
        except Exception as e:
            logger.error(f"requests方式失败: {e}")
            return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='新点e交易专区信息抓取工具')
    parser.add_argument('-o', '--output', default='zones_output.xlsx', help='输出Excel文件路径')
    parser.add_argument('--headless', action='store_true', help='无头模式运行')
    parser.add_argument('--requests', action='store_true', help='使用requests方式(备用)')
    
    args = parser.parse_args()
    
    if args.requests:
        # 使用requests方式
        fetcher = ZoneFetcherRequests()
        success = fetcher.fetch_with_requests(args.output)
    else:
        # 使用Selenium方式
        fetcher = ZoneFetcher(headless=args.headless)
        success = fetcher.run(args.output)
    
    if success:
        logger.info(f"✓ 成功！输出文件: {args.output}")
    else:
        logger.error("✗ 失败！")
        exit(1)


if __name__ == '__main__':
    main()
