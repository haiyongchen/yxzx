#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新点e交易专区信息抓取脚本 - 最终版
功能：从 https://www.etrading.cn/ 抓取所有专区名称和URL
"""

import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ZoneFetcher:
    def __init__(self, headless=False):
        self.driver = None
        self.wait = None
        self.headless = headless
        self.base_url = "https://www.etrading.cn/"
        self.zones_data = []
        
    def init_driver(self):
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(30)
            self.wait = WebDriverWait(self.driver, 15)
            logger.info("Chrome浏览器初始化成功")
            return True
        except Exception as e:
            logger.error(f"浏览器初始化失败: {e}")
            return False
    
    def close_driver(self):
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
    
    def open_page(self):
        try:
            self.driver.get(self.base_url)
            logger.info(f"已打开页面: {self.base_url}")
            time.sleep(3)
            return True
        except Exception as e:
            logger.error(f"打开页面失败: {e}")
            return False
    
    def get_all_zones(self):
        """获取所有专区信息"""
        try:
            logger.info("正在获取专区列表...")
            
            # 等待页面加载完成
            time.sleep(2)
            
            # 获取页面源码并解析
            page_source = self.driver.page_source
            
            # 使用正则表达式匹配专区链接
            # 匹配模式: <a href="http://xxx.etrading.cn/" target="_blank">专区名称</a>
            pattern = r'<a\s+href="(https?://[^"]+\.etrading\.cn/[^"]*)"\s+target="_blank"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, page_source)
            
            logger.info(f"正则匹配找到 {len(matches)} 个专区链接")
            
            for url, name in matches:
                name = name.strip()
                if name and url and not name.startswith('#'):
                    self.zones_data.append({
                        '专区名称': name,
                        '专区地址': url
                    })
            
            # 如果正则没找到，尝试用Selenium查找
            if len(self.zones_data) < 10:
                logger.info("正则匹配结果较少，尝试Selenium查找...")
                
                # 查找所有包含etrading.cn的链接
                links = self.driver.find_elements(By.XPATH, "//a[contains(@href,'etrading.cn')]")
                logger.info(f"Selenium找到 {len(links)} 个链接")
                
                for link in links:
                    try:
                        url = link.get_attribute("href")
                        name = link.text.strip()
                        
                        if url and name and url.startswith('http') and len(name) > 1:
                            # 去重
                            if not any(d['专区地址'] == url for d in self.zones_data):
                                self.zones_data.append({
                                    '专区名称': name,
                                    '专区地址': url
                                })
                    except:
                        continue
            
            logger.info(f"共获取到 {len(self.zones_data)} 个专区")
            return len(self.zones_data) > 0
            
        except Exception as e:
            logger.error(f"获取专区列表失败: {e}")
            return False
    
    def save_to_excel(self, output_path="zones_output.xlsx"):
        try:
            if not self.zones_data:
                logger.error("没有数据可保存")
                return False
            
            # 去重
            df = pd.DataFrame(self.zones_data)
            df = df.drop_duplicates(subset=['专区地址'])
            
            df.to_excel(output_path, index=False, engine='openpyxl')
            logger.info(f"数据已保存到: {output_path}")
            logger.info(f"共 {len(df)} 条记录")
            
            # 显示前10条
            print("\n前10条数据:")
            print(df.head(10).to_string())
            
            return True
        except Exception as e:
            logger.error(f"保存Excel失败: {e}")
            return False
    
    def run(self, output_path="zones_output.xlsx"):
        logger.info("=" * 50)
        logger.info("开始抓取新点e交易专区信息")
        logger.info("=" * 50)
        
        if not self.init_driver():
            return False
        
        try:
            if not self.open_page():
                return False
            
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
