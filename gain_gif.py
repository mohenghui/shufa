from PIL import Image
import os
import cv2
import numpy as np
import math
import sys
import imutils

"""
    将一张GIF动图分解到指定文件夹
    src_path：要分解的gif的路径
    dest_path：保存后的gif路径
"""


def intermediates(p1, p2, nb_points=8):
    """"Return a list of nb_points equally spaced points
    between p1 and p2"""
    # If we have 8 intermediate points, we have 8+1=9 spaces
    # between p1 and p2
    x_spacing = (p2[0] - p1[0]) / (nb_points + 1)
    y_spacing = (p2[1] - p1[1]) / (nb_points + 1)

    return [[p1[0] + i * x_spacing, p1[1] + i * y_spacing]
            for i in range(1, nb_points + 1)]


def cal_distance(p1, p2):
    return math.sqrt(math.pow((p2[0] - p1[0]), 2) + math.pow((p2[1] - p1[1]), 2))


class Gain():
    def __init__(self):
        self.index = 0
        self.save_txt_dir = "./bihua_data/"
        self.object_name = ["亟", "两", "匧", "辉", "斌", "了"]
        self.object_type = ".txt"
        self.image_type = ".gif"
        self.save_dir = './pics'
        self.mode = "w"
        self.width = 256
        self.height = 256
        self.channles = 1
        self.frame_only = False
        self.start = False
        self.step = 0
        self.flag = True
        self.dir = "./image/"
        while (os.path.isfile(self.save_txt_dir + self.object_name[self.index] + self.object_type)):
            print("[%s]字已存在，请删除后再修改" % self.object_name[self.index])
            self.index += 1
            # print(self.index)
            if (self.index >= len(self.object_name)):
                self.flag = False
                break
        if (self.flag):
            self.f = open(self.save_txt_dir + self.object_name[self.index] + self.object_type, "w")
        else:
            print("全部字体已存在，请进行删除后修改")
            sys.exit()

    def choose_contours(self, contours, MIN_AREA=10):
        point_list = []
        contour_list = []
        for item in contours:
            # cv2.boundingRect用一个最小的矩形，把找到的形状包起来
            rect = cv2.boundingRect(item)
            x = rect[0]
            y = rect[1]
            width = rect[2]
            height = rect[3]
            # print(width / height)
            # print(width * height)
            # 计算方块的大小比例,符合的装到集合
            if (width * height > MIN_AREA):
                point_list.append((x, y, width, height))
                # print(width * height)
                # print(width / height)
                contour_list.append(item)
        return point_list, contour_list

    def txt_add_point(self, px, py):
        add_point = '{},{}\n'.format(int(px), int(py))
        self.f.write(add_point)

    def gifSplit(self, src_path, dest_path, suffix="png"):
        frameNum = 0
        img = Image.open(src_path)
        point_x = -1
        point_y = -1
        for i in range(img.n_frames):
            img.seek(i)
            # seek() 方法用于移动文件读取指针到指定位置。
            new = Image.new("RGB", img.size)
            # new=new.resize((width, height), Image.ANTIALIAS)
            new.paste(img)
            new.save(os.path.join(self.save_dir, "%d.%s" % (i, suffix)))
            new = cv2.cvtColor(np.asarray(new), cv2.COLOR_RGBA2GRAY)
            new_img = cv2.resize(new, (self.width, self.height))
            frameNum += 1

            if (frameNum == 1):
                previousframe = new_img
            if (frameNum >= 2):
                currentframe = new_img
                currentframe_abs = cv2.absdiff(currentframe, previousframe)
                currentframe_median = cv2.medianBlur(currentframe_abs, 3)
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
                currentframe_open = cv2.morphologyEx(currentframe_median, cv2.MORPH_OPEN, kernel)
                #        img = cv2.imread("E:/chinese_ocr-master/4.png")
                #        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                ret, threshold_frame = cv2.threshold(currentframe_open, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
                # ret, threshold_frame = cv2.threshold(currentframe_abs, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                # gauss_image = cv2.GaussianBlur(threshold_frame, (3, 3), 0)
                contours = cv2.findContours(threshold_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                contours = contours[1] if imutils.is_cv3() else contours[0]
                font_point_list, _ = self.choose_contours(contours)

                if (not font_point_list) and (self.flag):
                    if (self.frame_only):
                        # self.txt_add_point(point_x, point_y)
                        for point_and_point_x, point_and_point_y in intermediates([point_x - 5, point_y - 5],
                                                                                  [point_x, point_y], 12):
                            point_x, point_y = point_and_point_x, point_and_point_y
                            self.txt_add_point(point_x, point_y)
                        # point_x, point_y = point_x+10, point_y+10
                        # self.txt_add_point(point_x, point_y)
                        self.frame_only = False

                    point_x, point_y = -1, -1
                    self.txt_add_point(point_x, point_y)
                    self.flag = False
                elif (font_point_list):
                    for (x, y, width, height) in font_point_list:
                        if (point_x == -1) and (point_y == -1):
                            point_x, point_y = x, y
                            self.frame_only = True
                        else:
                            # print("距离",cal_distance([point_x,point_y],[x,y]))
                            if (cal_distance([point_x, point_y], [x, y]) >= 40):
                                point_x, point_y = x, y
                                self.txt_add_point(point_x, point_y)
                            else:
                                self.txt_add_point(point_x, point_y)
                                for point_and_point_x, point_and_point_y in intermediates([point_x, point_y], [x, y]):
                                    point_x, point_y = point_and_point_x, point_and_point_y
                                    self.txt_add_point(point_x, point_y)
                                point_x, point_y = x, y
                                self.txt_add_point(point_x, point_y)
                            self.frame_only = False
                    self.flag = True
                cv2.imshow("Frame", threshold_frame)

                previousframe = currentframe
                # cv2.imshow(str(i),new)

            cv2.waitKey(10)
        self.f.close()

    def next_write(self):
        self.f = open(self.save_txt_dir + self.object_name[self.index] + self.object_type, "w")

    def collect(self):
        self.gifSplit((self.dir + self.object_name[self.index] + self.image_type), (self.image_type))
        self.f.close()

    def main(self):
        print("第%s个字[%s]" % (self.index + 1, self.object_name[self.index]))
        print("开始采集")
        self.collect()
        print("采集结束")
        while (1):
            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                self.f.close()
                break
            if (k == ord('c')) and (self.start):
                print("开始采集")
                self.collect()
                print("采集结束")
            if k == ord('n'):
                self.f.close()
                self.start = True
                if (self.index < len(self.object_name) - 1):
                    self.index += 1
                    self.next_write()
                    self.flag = True

                    print("下一个字[%s]" % self.object_name[self.index])
                else:
                    print("没字了")
                    break


gain = Gain()
# gain.gifSplit('image/匧.gif', r'./pics')
gain.main()
