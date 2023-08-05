"""
豆瓣爬虫: 用beautifulsoup4库获取豆瓣排行榜上每部电影的有利于分析的数据细节再写入csv文件

更新2.2: packaging the project, some little fixes
V3: 将对数据进行细致处理并可视化 *更新日期待定
Introduction: This program is to output the information of each movie in the top ten latest movie charts to a csv file
** API由豆瓣提供: https://developers.douban.com/wiki/?title=movie_v2#subject

__author__ = v1siuol
__date__ = 2017-03-23
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
import csv
import random
import re
import json
import time


class webSpider_duobanFilms:
    def __init__(self, inputOption=1):
        # Option:1 for short, 2 for details
        self.option = inputOption

    def setOption(self, newOption):
        self.option = newOption

    def for_love(self):
        print("Begin----------------------------------")
        startTime = time.time()
        showTimeSet = "%Y-%m-%d %X"
        filePath = "./"
        fileName = "lstMoviesAnaCharts.csv"
        chartUrl = "https://movie.douban.com/chart"
        baseUrl = "https://api.douban.com/v2/movie/subject/"
        counter = 0

        # 打开或创建csv文件 / Open or create a csv file
        csvFile = open(filePath + fileName, "w+")

        # 从豆瓣新片榜获取电影id / Retrieve movie_id from top ten latest movie charts
        html = urlopen(chartUrl)
        bs0bj = BeautifulSoup(html, "lxml")
        lstMovies = bs0bj.find("div", {"class": "indent"}).findAll("div", {"id": re.compile("collect_form_\d+")})
        lstMoviesId = [movie.attrs["id"][13:] for movie in lstMovies]

        try:
            # 在csv文件创建表头 / Create the headings in csv file
            writer = csv.writer(csvFile)
            print("* Top 10 films info will be written into lstMoviesAnaCharts.csv, located in the same folder. *")
            writer.writerow(["Updated time: " + time.strftime(showTimeSet, time.localtime(startTime))])

            if self.option == 1:
                writer.writerow(["原名"])  # testing
            elif self.option == 2:
                writer.writerow(("条目id", "原名", "导演名字", "主演名字", "制片国家/地区", "影片类型", "平均评分",
                                 "年代", "评分人数", "想看人数", "看过人数", "短评数量", "影评数量"))
        except Exception as e:
            print("Exception:", e)

        for mId in lstMoviesId:
            # 接入api并解析json / Get data from api and deal with json
            responseJson = json.loads(urlopen(baseUrl + mId).read().decode("utf-8"))  # {}

            movieId = responseJson["id"]  # 条目id
            movieOriginalTitle = responseJson["original_title"]  # 原名
            movieRating = responseJson["rating"]  # 评分
            movieAveRating = movieRating["average"]  # 平均评分
            movieRatingsCount = responseJson["ratings_count"]  # 评分人数
            movieWishCount = responseJson["wish_count"]  # 想看人数
            movieCollectCount = responseJson["collect_count"]  # 看过人数

            movieDirectors = responseJson["directors"]  # 导演，数据结构为影人的简化描述
            movieDirectorsName = ""  # 导演名字
            for director in movieDirectors:
                movieDirectorsName += director["name"]
                if director != movieDirectors[-1]:
                    movieDirectorsName += " / "

            movieCasts = responseJson["casts"]  # 主演，最多可获得4个，数据结构为影人的简化描述
            movieCastsName = ""  # 主演名字
            for cast in movieCasts:
                movieCastsName += cast["name"]
                if cast != movieCasts[-1]:
                    movieCastsName += " / "

            movieYear = responseJson["year"]  # 年代
            movieGenres = responseJson["genres"]  # 影片类型，最多提供3个
            movieGenresName = ""  # 影片类型名字
            for genre in movieGenres:
                movieGenresName += genre
                if genre != movieGenres[-1]:
                    movieGenresName += " / "

            movieCountries = responseJson["countries"]  # 制片国家/地区
            movieCountriesName = ""  # 制片国家/地区名字
            for country in movieCountries:
                movieCountriesName += country
                if country != movieCountries[-1]:
                    movieCountriesName += " / "

            movieCommentsCount = responseJson["comments_count"]  # 短评数量
            movieReviewsCount = responseJson["reviews_count"]  # 影评数量

            try:
                # 把处理好的数据写入csv文件 / Write data into the csv file
                if self.option == 1:
                    writer.writerow([movieOriginalTitle])
                elif self.option == 2:
                    writer.writerow((movieId, movieOriginalTitle, movieDirectorsName, movieCastsName, movieCountriesName,
                                     movieGenresName, movieAveRating, movieYear, movieRatingsCount,
                                     movieWishCount, movieCollectCount, movieCommentsCount, movieReviewsCount))
                counter += 1
            except Exception as e:
                print("Exception:", e)

            print("Finished %d/%d" % (counter, len(lstMoviesId)))
            # 设置爬虫间隔2s(公开api接口: 40次请求/分钟) / Set the crawl span 2 seconds (public api: 40 requests per minute)
            time.sleep(1.5+random.randint(1, 100)/100)

        # 关闭csv文件 / Close csv file
        csvFile.close()
        print("------------------------------------End")
        print("Time elapsed: %.6f(s)" % (time.time() - startTime))


# -------------test case-----------------
if __name__ == "__main__":
    if True:
        love = webSpider_duobanFilms(1)
        love.for_love()
