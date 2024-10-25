from koubei_watcher.apps.car_review_scraper import CarReviewScraper
from koubei_watcher.apps.series_list_scraper import Series

def main():

    brandid = input('请输入品牌的 brandId: ')
    # 通过 Series 获取该品牌的信息
    series_brand = Series(brandid)  # 假设 279 是品牌代码

    # 初始化爬虫类
    scraper = CarReviewScraper(series_brand)

    # 让用户选择是抓取单个车型还是全部车型
    user_choice = input("输入 '1' 抓取单个车型评论，输入 '2' 抓取所有车型评论: ")

    if user_choice == '1':
        series_id = input("请输入车型的 seriesId: ")
        scraper.scrape_reviews([series_id])  # 传入单个车型 ID 列表
    elif user_choice == '2':
        scraper.scrape_reviews()  # 不传入参数，默认抓取所有车型
    else:
        print("无效输入，程序退出")

if __name__ == "__main__":
    main()
