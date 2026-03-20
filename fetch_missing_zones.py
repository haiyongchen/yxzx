#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
二次抓取遗漏的专区地址
针对专区接入情况统计表_R列已填充.xlsx中未匹配的专区进行针对性抓取
"""

import pandas as pd
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, WebDriverException
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MissingZoneFetcher:
    """抓取遗漏专区"""
    
    def __init__(self, headless=False):
        self.driver = None
        self.wait = None
        self.headless = headless
        self.base_url = "https://www.etrading.cn/"
        self.found_zones = {}  # 找到的专区 {名称: URL}
        
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
    
    def click_zone_selector(self):
        """点击专区选择按钮"""
        try:
            # 尝试多种方式
            selectors = [
                "//span[contains(text(),'专区选择')]",
                "//a[contains(text(),'专区选择')]",
                "//div[contains(@class,'zone')]",
            ]
            
            for selector in selectors:
                try:
                    zone_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    zone_btn.click()
                    logger.info("已点击'专区选择'按钮")
                    time.sleep(2)
                    return True
                except:
                    continue
            
            return False
        except Exception as e:
            logger.error(f"点击专区选择失败: {e}")
            return False
    
    def search_zone(self, zone_name):
        """搜索特定专区"""
        try:
            # 等待搜索框
            search_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入搜索关键字']"))
            )
            
            # 清空并输入
            search_input.clear()
            search_input.send_keys(zone_name)
            logger.info(f"搜索: {zone_name}")
            
            # 按回车或点击搜索
            try:
                search_btn = self.driver.find_element(By.XPATH, "//i[@class='search-icon']")
                search_btn.click()
            except:
                search_input.send_keys(Keys.RETURN)
            
            time.sleep(2)
            return True
        except Exception as e:
            logger.error(f"搜索失败: {e}")
            return False
    
    def get_search_result(self, zone_name):
        """获取搜索结果"""
        try:
            # 查找搜索结果中的链接
            results = self.driver.find_elements(By.XPATH, "//li[contains(@class,'hot-item')]//a")
            
            for link in results:
                try:
                    url = link.get_attribute("href")
                    name = link.text.strip()
                    
                    if url and name and url.startswith('http'):
                        # 检查是否是目标专区
                        if zone_name in name or name in zone_name:
                            logger.info(f"找到: {name} -> {url}")
                            return url
                except:
                    continue
            
            # 如果没有精确匹配，返回第一个结果
            if results:
                first = results[0]
                url = first.get_attribute("href")
                name = first.text.strip()
                if url and url.startswith('http'):
                    logger.info(f"模糊匹配: {name} -> {url}")
                    return url
            
            return None
        except Exception as e:
            logger.error(f"获取结果失败: {e}")
            return None
    
    def search_and_get_url(self, zone_name):
        """搜索并获取URL"""
        try:
            # 点击专区选择
            if not self.click_zone_selector():
                return None
            
            # 搜索
            if not self.search_zone(zone_name):
                return None
            
            # 获取结果
            url = self.get_search_result(zone_name)
            
            # 重置到首页
            self.driver.get(self.base_url)
            time.sleep(2)
            
            return url
        except Exception as e:
            logger.error(f"搜索过程出错: {e}")
            return None
    
    def fetch_missing_zones(self, missing_names):
        """批量抓取遗漏的专区"""
        logger.info(f"需要抓取的遗漏专区: {len(missing_names)} 个")
        
        if not self.init_driver():
            return {}
        
        try:
            if not self.open_page():
                return {}
            
            for i, name in enumerate(missing_names):
                logger.info(f"[{i+1}/{len(missing_names)}] 查找: {name}")
                
                url = self.search_and_get_url(name)
                if url:
                    self.found_zones[name] = url
                    logger.info(f"✓ 成功: {name} -> {url}")
                else:
                    logger.warning(f"✗ 未找到: {name}")
                
                # 每10个暂停一下
                if (i + 1) % 10 == 0:
                    logger.info(f"进度: {i+1}/{len(missing_names)}, 已找到 {len(self.found_zones)} 个")
            
            logger.info(f"\n抓取完成! 共找到 {len(self.found_zones)} 个专区")
            return self.found_zones
            
        except Exception as e:
            logger.error(f"抓取过程出错: {e}")
            return self.found_zones
        finally:
            self.close_driver()


def main():
    # 1. 读取已填充的表，找出未匹配的专区
    logger.info("读取专区接入情况统计表_R列已填充.xlsx...")
    stats_df = pd.read_excel('专区接入情况统计表_R列已填充.xlsx')
    
    # 找出未匹配的专区
    missing_df = stats_df[stats_df['专区地址'].isna()]
    missing_names = missing_df['专区名称'].dropna().unique().tolist()
    
    logger.info(f"未匹配的专区: {len(missing_names)} 个")
    logger.info(f"示例: {missing_names[:10]}")
    
    if not missing_names:
        logger.info("没有未匹配的专区，无需抓取")
        return
    
    # 2. 抓取遗漏的专区
    fetcher = MissingZoneFetcher(headless=False)
    found_zones = fetcher.fetch_missing_zones(missing_names)
    
    # 3. 保存抓取结果
    if found_zones:
        found_df = pd.DataFrame([
            {'专区名称': name, '专区地址': url}
            for name, url in found_zones.items()
        ])
        found_df.to_excel('二次抓取_遗漏专区.xlsx', index=False)
        logger.info(f"抓取结果已保存: 二次抓取_遗漏专区.xlsx ({len(found_df)} 条)")
    
    # 4. 更新原表
    if found_zones:
        logger.info("\n更新原表...")
        for idx, row in stats_df.iterrows():
            if pd.isna(row['专区地址']) and row['专区名称'] in found_zones:
                stats_df.at[idx, '专区地址'] = found_zones[row['专区名称']]
                logger.info(f"更新: {row['专区名称']} -> {found_zones[row['专区名称']]}")
        
        # 保存更新后的表
        stats_df.to_excel('专区接入情况统计表_二次填充.xlsx', index=False)
        logger.info("更新后的表已保存: 专区接入情况统计表_二次填充.xlsx")
        
        # 统计
        final_count = stats_df['专区地址'].notna().sum()
        logger.info(f"\n最终统计:")
        logger.info(f"总记录: {len(stats_df)}")
        logger.info(f"已有地址: {final_count}")
        logger.info(f"填充率: {final_count/len(stats_df)*100:.1f}%")


if __name__ == '__main__':
    main()