#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新点e交易专区信息抓取脚本 V2
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
            time.sleep(3)
            return True
        except Exception as e:
            logger.error(f"打开页面失败: {e}")
            return False
    
    def click_zone_selector(self):
        """点击专区选择按钮"""
        try:
            # 根据截图，找到"专区选择"按钮
            selectors = [
                "//span[contains(text(),'专区选择')]",
                "//a[contains(text(),'专区选择')]",
                "//div[contains(@class,'zone')]//span",
            ]
            
            for selector in selectors:
                try:
                    zone_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    zone_btn.click()
                    logger.info(f"已点击'专区选择'按钮")
                    time.sleep(2)
                    return True
                except:
                    continue
            
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
            logger.info("正在获取专区列表...")
            
            # 查找所有hot-item - 根据截图中的HTML结构
            zone_items = self.driver.find_elements(By.XPATH, "//li[contains(@class,'hot-item')]")
            
            logger.info(f"找到 {len(zone_items)} 个专区项")
            
            for item in zone_items:
                try:
                    # 获取链接元素
                    link = item.find_element(By.TAG_NAME, "a")
                    url = link.get_attribute("href")
                    name = link.text.strip()
                    
                    if url and name and url.startswith('http'):
                        self.zones_data.append({
                            '专区名称': name,
                            '专区地址': url
                        })
                        
                except Exception as e:
                    continue
            
            logger.info(f"共获取到 {len(self.zones_data)} 个专区")
            return len(self.zones_data) > 0
            
        except Exception as e:
            logger.error(f"获取专区列表失败: {e}")
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
        
        if not self.init_driver():
            return False
        
        try:
            if not self.open_page():
                return False
            
            # 直接获取页面上的专区列表（不需要点击）
            if not self.get_all_zones():
                logger.error("获取专区失败")
                return False
            
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


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='新点e交易专区信息抓取工具')
    parser.add_argument('-o', '--output', default='zones_output.xlsx', help='输出Excel文件路径')
    parser.add_argument('--headless', action='store_true', help='无头模式运行')
    
    args = parser.parse_args()
    
    fetcher = ZoneFetcher(headless=args.headless)
    success = fetcher.run(args.output)
    
    if success:
        logger.info(f"✓ 成功！输出文件: {args.output}")
    else:
        logger.error("✗ 失败！")
        exit(1)


if __name__ == '__main__':
    main()
