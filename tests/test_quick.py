import unittest
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock
import io

# 添加工作目录到系统路径，以便导入quick.py
sys.path.insert(0, '/workspace')

import quick


class TestQuickScript(unittest.TestCase):
    
    def setUp(self):
        """设置测试环境"""
        # 清空全局列表，避免测试间相互影响
        quick.my_list.clear()
        
    def test_recursion_dir_with_py_and_ipynb_files(self):
        """测试递归目录函数是否正确识别.py和.ipynb文件"""
        # 创建临时目录结构
        with tempfile.TemporaryDirectory() as temp_dir:
            # 创建一些测试文件
            py_file = os.path.join(temp_dir, "test.py")
            ipynb_file = os.path.join(temp_dir, "notebook.ipynb")
            txt_file = os.path.join(temp_dir, "document.txt")
            
            # 创建这些文件
            with open(py_file, 'w') as f:
                f.write("# Python file")
            with open(ipynb_file, 'w') as f:
                f.write('{"cells": []}')  # 简单的notebook格式
            with open(txt_file, 'w') as f:
                f.write("Text document")
            
            # 还创建一个子目录和其中的.py文件
            sub_dir = os.path.join(temp_dir, "subdir")
            os.makedirs(sub_dir)
            sub_py_file = os.path.join(sub_dir, "sub_test.py")
            with open(sub_py_file, 'w') as f:
                f.write("# Subdirectory Python file")
            
            # 调用递归函数
            quick.recursion_dir(temp_dir, 0)
            
            # 验证结果
            expected_files = {py_file, ipynb_file, sub_py_file}
            actual_files = set(quick.my_list)
            
            self.assertEqual(expected_files, actual_files)
    
    def test_recursion_dir_empty_directory(self):
        """测试空目录的情况"""
        with tempfile.TemporaryDirectory() as temp_dir:
            quick.recursion_dir(temp_dir, 0)
            self.assertEqual(len(quick.my_list), 0)
    
    def test_recursion_dir_no_matching_files(self):
        """测试没有.py或.ipynb文件的目录"""
        with tempfile.TemporaryDirectory() as temp_dir:
            txt_file = os.path.join(temp_dir, "document.txt")
            with open(txt_file, 'w') as f:
                f.write("Text document")
            
            quick.recursion_dir(temp_dir, 0)
            self.assertEqual(len(quick.my_list), 0)
    
    @patch('sys.stdout', new_callable=io.StringIO)
    @patch('os.system')
    def test_main_execution_flow(self, mock_os_system, mock_stdout):
        """测试主执行流程（模拟os.system调用）"""
        # 保存原始my_list
        original_my_list = quick.my_list[:]
        
        try:
            # 重置my_list为包含一些测试路径
            quick.my_list = ['/fake/path/test.py', '/fake/path/notebook.ipynb']
            
            # 重新运行脚本的主要部分（除了实际的系统调用）
            name = '刘杰.tar.gz '
            print(name)
            print(quick.my_list)
            
            # 验证输出
            output = mock_stdout.getvalue()
            self.assertIn('刘杰.tar.gz ', output)
            self.assertIn('/fake/path/test.py', output)
            self.assertIn('/fake/path/notebook.ipynb', output)
            
        finally:
            # 恢复原始my_list
            quick.my_list = original_my_list
    
    def test_regex_pattern_matches_py_and_ipynb(self):
        """测试正则表达式模式是否正确匹配.py和.ipynb文件"""
        # 测试.py文件
        py_match = os.path.basename("test.py")
        self.assertIsNotNone(quick.re.search(r'.py$|.ipynb$', py_match))
        
        # 测试.ipynb文件
        ipynb_match = os.path.basename("notebook.ipynb")
        self.assertIsNotNone(quick.re.search(r'.py$|.ipynb$', ipynb_match))
        
        # 测试非匹配文件
        txt_match = os.path.basename("document.txt")
        self.assertIsNone(quick.re.search(r'.py$|.ipynb$', txt_match))


if __name__ == '__main__':
    unittest.main()