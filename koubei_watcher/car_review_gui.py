# car_review_gui.py

import sys
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit,
                             QFileDialog, QListWidget, QListWidgetItem, QMessageBox)
from PyQt5.QtCore import Qt
from koubei_watcher.apps.car_review_scraper import CarReviewScraper
from koubei_watcher.apps.series_list_scraper import Series


class CarReviewApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Car Review Scraper')

        # 爬取任务控制
        self.scraping = False  # 是否正在抓取
        self.selected_directory = None  # 保存抓取数据的目录

        # 创建布局
        layout = QVBoxLayout()

        # 输入品牌Id
        self.brand_label = QLabel('请输入品牌的 brandId:')
        self.brand_input = QLineEdit()
        layout.addWidget(self.brand_label)
        layout.addWidget(self.brand_input)

        # 获取车型按钮
        self.get_models_button = QPushButton('获取该品牌的车型')
        self.get_models_button.clicked.connect(self.get_models)
        layout.addWidget(self.get_models_button)

        # 车型选择列表
        self.model_list_label = QLabel('选择车型:')
        self.model_list_widget = QListWidget()
        self.model_list_widget.setSelectionMode(QListWidget.MultiSelection)  # 允许选择多个车型
        layout.addWidget(self.model_list_label)
        layout.addWidget(self.model_list_widget)

        # 选择文件存放目录按钮
        self.select_directory_button = QPushButton('选择文件存放目录')
        self.select_directory_button.clicked.connect(self.select_directory)
        layout.addWidget(self.select_directory_button)

        # 抓取评论按钮
        self.scrape_button = QPushButton('抓取评论')
        self.scrape_button.clicked.connect(self.scrape_reviews)
        layout.addWidget(self.scrape_button)

        # 停止按钮
        self.stop_button = QPushButton('停止抓取')
        self.stop_button.clicked.connect(self.stop_scraping)
        layout.addWidget(self.stop_button)

        # 输出结果显示区域
        self.result_output = QTextEdit()
        self.result_output.setReadOnly(True)  # 设为只读
        layout.addWidget(self.result_output)

        # 设置布局
        self.setLayout(layout)

    def select_directory(self):
        """
        打开文件对话框，选择保存文件的目录
        """
        directory = QFileDialog.getExistingDirectory(self, "选择保存文件的目录")
        if directory:
            self.selected_directory = directory
            self.result_output.append(f'保存目录已选择: {directory}')

    def get_models(self):
        """
        获取该品牌的所有车型并显示在车型列表中
        """
        brand_id = self.brand_input.text()
        if not brand_id:
            QMessageBox.warning(self, '错误', '请填写品牌的 brandId！')
            return

        self.result_output.append(f'正在获取 brandId: {brand_id} 的车型...')

        # 获取该品牌的车型列表
        series_brand = Series(brand_id)
        series_id_list = series_brand.series_code_get('seriesid')

        # 清空之前的列表
        self.model_list_widget.clear()

        # 添加车型和能源方式到列表
        for series_id in series_id_list:
            car_name, is_electric = CarReviewScraper(series_brand).get_car_name_and_type(series_id)
            if car_name:
                energy_type = "新能源" if is_electric else "燃油车"
                item_text = f'{car_name} ({energy_type})'
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, series_id)  # 关联 series_id
                self.model_list_widget.addItem(item)

        self.result_output.append('车型获取完成！请选择车型。')

    def scrape_reviews(self):
        """
        抓取用户选择的车型评论
        """
        if self.scraping:
            QMessageBox.warning(self, '警告', '抓取任务正在进行中，请稍后再试！')
            return

        selected_items = self.model_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, '错误', '请至少选择一个车型！')
            return

        if not self.selected_directory:
            QMessageBox.warning(self, '错误', '请先选择文件存放目录！')
            return

        self.scraping = True
        self.result_output.append('开始抓取...')

        brand_id = self.brand_input.text()
        series_brand = Series(brand_id)
        scraper = CarReviewScraper(series_brand)

        # 获取用户选择的车型 ID 列表
        selected_series_ids = [item.data(Qt.UserRole) for item in selected_items]

        # 执行抓取任务
        for series_id in selected_series_ids:
            if not self.scraping:  # 如果停止按钮被点击
                self.result_output.append('抓取已停止！')
                break

            car_name, is_electric = scraper.get_car_name_and_type(series_id)
            csv_filename = f'[{("新能源" if is_electric else "燃油车")}] {car_name}.csv'
            save_path = os.path.join(self.selected_directory, csv_filename)

            scraper.scrape_reviews([series_id])
            self.result_output.append(f'评论已抓取并保存到 {save_path}')

        self.scraping = False
        self.result_output.append('抓取任务完成！')

    def stop_scraping(self):
        """
        停止抓取
        """
        if self.scraping:
            self.scraping = False
            self.result_output.append('正在停止抓取...')
        else:
            QMessageBox.information(self, '信息', '当前没有进行中的抓取任务。')


# 主函数
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 创建应用窗口
    window = CarReviewApp()
    window.show()

    # 运行应用
    sys.exit(app.exec_())
