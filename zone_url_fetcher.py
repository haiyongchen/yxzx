#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新点e交易专区地址自动获取脚本
功能：根据Excel中的原专区名称，自动从总站获取专区地址并回填
作者：AI Assistant
日期：2026-03-20
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
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException, 
    ElementNotInteractableException,
    WebDriverException
)
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('zone_url_fetcher.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ZoneUrlFetcher:
    """专区地址获取器"""
    
    def __init__(self, excel_path, headless=False):
        """
        初始化
        :param excel_path: Excel文件路径
        :param headless: 是否无头模式运行
        """
        self.excel_path = excel_path
        self.driver = None
        self.wait = None
        self.headless = headless
        self.base_url = "https://www.etrading.cn/"
        
        # 读取Excel
        logger.info(f"正在读取Excel文件: {excel_path}")
        self.xl = pd.ExcelFile(excel_path)
        self.sheet_names = self.xl.sheet_names
        logger.info(f"发现 {len(self.sheet_names)} 个工作表: {self.sheet_names}")
        
    def init_driver(self):
        """初始化Chrome浏览器"""
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument('--headless')
            
            # 基础配置
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
            
            # 禁用通知和弹窗
            chrome_options.add_argument('--disable-notifications')
            chrome_options.add_argument('--disable-popup-blocking')
            
            # 创建驱动
            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.set_page_load_timeout(30)
            self.wait = WebDriverWait(self.driver, 10)
            
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
    
    def open_base_page(self):
        """打开总站页面"""
        try:
            self.driver.get(self.base_url)
            logger.info(f"已打开页面: {self.base_url}")
            time.sleep(2)  # 等待页面加载
            return True
        except Exception as e:
            logger.error(f"打开页面失败: {e}")
            return False
    
    def click_zone_selector(self):
        """点击专区选择按钮"""
        try:
            # 等待并点击"专区选择"按钮
            zone_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'专区选择')]"))
            )
            zone_btn.click()
            logger.info("已点击'专区选择'按钮")
            time.sleep(1)
            return True
            
        except TimeoutException:
            # 尝试其他定位方式
            try:
                zone_btn = self.driver.find_element(By.XPATH, "//a[contains(text(),'专区选择')]")
                zone_btn.click()
                logger.info("已点击'专区选择'按钮(通过xpath)")
                time.sleep(1)
                return True
            except Exception as e:
                logger.error(f"点击专区选择按钮失败: {e}")
                return False
        except Exception as e:
            logger.error(f"点击专区选择按钮失败: {e}")
            return False
    
    def search_zone(self, zone_name):
        """
        搜索专区
        :param zone_name: 专区名称
        :return: 是否成功
        """
        try:
            # 等待搜索框出现
            search_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入搜索关键字']"))
            )
            
            # 清空并输入搜索词
            search_input.clear()
            search_input.send_keys(zone_name)
            logger.info(f"已输入搜索词: {zone_name}")
            
            # 点击搜索按钮或按回车
            try:
                search_btn = self.driver.find_element(By.XPATH, "//i[@class='search-icon']")
                search_btn.click()
            except:
                search_input.send_keys(Keys.RETURN)
            
            logger.info("已执行搜索")
            time.sleep(2)  # 等待搜索结果
            return True
            
        except Exception as e:
            logger.error(f"搜索专区失败: {e}")
            return False
    
    def click_search_result(self, zone_name):
        """
        点击搜索结果
        :param zone_name: 专区名称
        :return: 是否成功
        """
        try:
            result_found = False
            
            # 方式1: 通过包含专区名称的元素
            try:
                result = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(),'{zone_name}')]"))
                )
                result.click()
                result_found = True
                logger.info(f"已点击搜索结果: {zone_name}")
            except:
                pass
            
            # 方式2: 通过部分匹配
            if not result_found:
                try:
                    keywords = zone_name.replace("专区", "").replace("平台", "").replace("电子交易", "")
                    if len(keywords) > 2:
                        result = self.driver.find_element(By.XPATH, f"//a[contains(text(),'{keywords}')]")
                        result.click()
                        result_found = True
                        logger.info(f"已点击搜索结果(模糊匹配): {keywords}")
                except:
                    pass
            
            # 方式3: 点击第一个搜索结果
            if not result_found:
                try:
                    results = self.driver.find_elements(By.XPATH, "//div[contains(@class,'zone-item')]//a")
                    if results:
                        results[0].click()
                        result_found = True
                        logger.info("已点击第一个搜索结果")
                except:
                    pass
            
            if result_found:
                time.sleep(3)
                return True
            else:
                logger.warning(f"未找到搜索结果: {zone_name}")
                return False
                
        except Exception as e:
            logger.error(f"点击搜索结果失败: {e}")
            return False
    
    def get_new_window_url(self):
        """
        获取新窗口的URL
        :return: URL字符串或None
        """
        try:
            handles = self.driver.window_handles
            
            if len(handles) > 1:
                new_window = handles[-1]
                self.driver.switch_to.window(new_window)
                time.sleep(2)
                url = self.driver.current_url
                logger.info(f"获取到新窗口URL: {url}")
                
                # 关闭新窗口，切回原窗口
                self.driver.close()
                self.driver.switch_to.window(handles[0])
                
                return url
            else:
                # 如果没有新窗口，获取当前URL
                url = self.driver.current_url
                if url != self.base_url:
                    logger.info(f"当前页面URL: {url}")
                    self.driver.get(self.base_url)  # 返回首页
                    return url
                return None
                
        except Exception as e:
            logger.error(f"获取URL失败: {e}")
            return None
    
    def reset_to_home(self):
        """重置到首页"""
        try:
            # 关闭所有其他窗口
            handles = self.driver.window_handles
            while len(handles) > 1:
                self.driver.switch_to.window(handles[-1])
                self.driver.close()
                handles = self.driver.window_handles
            
            # 切回主窗口
            if handles:
                self.driver.switch_to.window(handles[0])
            
            # 刷新页面
            self.driver.get(self.base_url)
            time.sleep(2)
            logger.info("已重置到首页")
            return True
        except Exception as e:
            logger.error(f"重置到首页失败: {e}")
            return False
    
    def process_single_zone(self, zone_name):
        """
        处理单个专区
        :param zone_name: 专区名称
        :return: URL或None
        """
        if not zone_name or pd.isna(zone_name):
            return None
        
        # 清理专区名称
        zone_name = str(zone_name).strip()
        if not zone_name:
            return None
        
        logger.info(f"开始处理专区: {zone_name}")
        
        try:
            # 1. 点击专区选择
            if not self.click_zone_selector():
                logger.error("点击专区选择失败，尝试重置")
                self.reset_to_home()
                if not self.click_zone_selector():
                    return None
            
            # 2. 搜索专区
            if not self.search_zone(zone_name):
                logger.error(f"搜索专区失败: {zone_name}")
                return None
            
            # 3. 点击搜索结果
            if not self.click_search_result(zone_name):
                logger.warning(f"未找到搜索结果或点击失败: {zone_name}")
                return None
            
            # 4. 获取URL
            url = self.get_new_window_url()
            return url
            
        except Exception as e:
            logger.error(f"处理专区时出错: {zone_name}, 错误: {e}")
            return None
    
    def process_excel(self, output_path=None):
        """
        处理整个Excel文件
        :param output_path: 输出路径，默认覆盖原文件
        """
        if output_path is None:
            output_path = self.excel_path
        
        # 初始化浏览器
        if not self.init_driver():
            logger.error("浏览器初始化失败，退出")
            return False
        
        try:
            # 打开首页
            if not self.open_base_page():
                logger.error("打开首页失败")
                return False
            
            # 处理每个工作表
            all_data = {}
            for sheet_name in self.sheet_names:
                logger.info(f"\n{'='*50}")
                logger.info(f"处理工作表: {sheet_name}")
                logger.info(f"{'='*50}")
                
                # 读取工作表
                df = pd.read_excel(self.excel_path, sheet_name=sheet_name)
                
                # 检查是否有"原专区名称"列
                if '原专区名称' not in df.columns:
                    logger.warning(f"工作表 {sheet_name} 没有'原专区名称'列，跳过")
                    all_data[sheet_name] = df
                    continue
                
                # 检查是否有"专区地址"列，没有则创建
                if '专区地址' not in df.columns:
                    df['专区地址'] = ''
                    logger.info(f"已创建'专区地址'列")
                
                # 处理每一行
                total = len(df)
                success = 0
                failed = 0
                
                for idx in range(total):
                    zone_name = df.at[idx, '原专区名称']
                    current_url = df.at[idx, '专区地址']
                    
                    # 如果已有地址，跳过
                    if pd.notna(current_url) and str(current_url).strip():
                        logger.info(f"[{idx+1}/{total}] {zone_name} 已有地址，跳过")
                        continue
                    
                    # 处理专区
                    url = self.process_single_zone(zone_name)
                    
                    if url:
                        df.at[idx, '专区地址'] = url
                        success += 1
                        logger.info(f"[{idx+1}/{total}] ✓ 成功获取地址: {url}")
                    else:
                        failed += 1
                        logger.warning(f"[{idx+1}/{total}] ✗ 获取地址失败: {zone_name}")
                    
                    # 每处理5个保存一次
                    if (idx + 1) % 5 == 0:
                        logger.info(f"进度: {idx+1}/{total}, 成功: {success}, 失败: {failed}")
                        # 保存中间结果
                        self._save_to_excel(all_data, output_path, df, sheet_name)
                
                # 保存工作表数据
                all_data[sheet_name] = df
                logger.info(f"工作表 {sheet_name} 处理完成: 成功 {success}, 失败 {failed}")
            
            # 最终保存
            self._save_final_excel(all_data, output_path)
            logger.info(f"\n所有工作表处理完成，已保存到: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"处理Excel时出错: {e}")
            return False
        finally:
            self.close_driver()
    
    def _save_to_excel(self, all_data, output_path, current_df, current_sheet):
        """保存中间结果"""
        try:
            all_data[current_sheet] = current_df
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                for sheet_name, df in all_data.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            logger.info(f"已保存中间结果")
        except Exception as e:
            logger.error(f"保存中间结果失败: {e}")
    
    def _save_final_excel(self, all_data, output_path):
        """保存最终结果"""
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                for sheet_name, df in all_data.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)
            logger.info(f"最终结果已保存")
        except Exception as e:
            logger.error(f"保存最终结果失败: {e}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='新点e交易专区地址自动获取工具')
    parser.add_argument('excel_path', help='Excel文件路径')
    parser.add_argument('-o', '--output', help='输出文件路径(默认覆盖原文件)')
    parser.add_argument('--headless', action='store_true', help='无头模式运行')
    
    args = parser.parse_args()
    
    # 创建获取器
    fetcher = ZoneUrlFetcher(args.excel_path, headless=args.headless)
    
    # 处理Excel
    success = fetcher.process_excel(output_path=args.output)
    
    if success:
        logger.info("处理完成！")
    else:
        logger.error("处理失败！")
        exit(1)


if __name__ == '__main__':
    main()
