# encoding=utf-8
import cv2
import numpy as np
import time


class Recurrent:
    def __init__(self, filename):
        self.save_txt_dir = "./bihua_data/"
        self.findname = filename
        self.object_type = ".txt"
        self.findname_len = len(filename)
        self.index = 0
        self.width = 256
        self.height = 256
        self.channles = 1
        self.img = np.zeros((self.width, self.height, self.channles), np.uint8)
        self.f = open(self.save_txt_dir + self.findname[self.index] + self.object_type, "r")

    def start_write(self):
        line = self.f.readline()  # 调用文件的 readline()方法
        while line:
            x, y = line.split(",")
            if (x != "-1") and (y != "-1"):
                for i in range(self.channles):
                    # self.img[int(x),int(y),i]=0
                    cv2.circle(self.img, (int(x), int(y)), 1, (0), 5, cv2.LINE_AA, 0)
                    # cv2.line(self.img, (int(x), int(y)), 1, (0), 5, cv2.LINE_AA, 0)
                    cv2.imshow("write", self.img)
                    # cv2.waitKey(1)
            # print(line, end = '')  # 后面跟 ',' 将忽略换行符
            # print(line, end = '')　      # 在 Python 3 中使用
            line = self.f.readline()
        self.f.close()
        # cv2.waitKey()

    def main(self):
        self.init_write(self.img)
        # self.img[100, 100, 0] = 0
        print("第一个字[%s]" % self.findname[self.index])
        cv2.namedWindow("write")
        # cv2.setMouseCallback("block", self.wirte)
        while (1):
            cv2.imshow("write", self.img)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                break
            if k == ord('s'):
                print("开始书写")
                self.start_write()
                print("书写结束")
            if k == ord('n'):
                self.init_write(self.img)
                if (self.index < self.findname_len - 1):
                    self.index += 1
                    print("下一个字[%s]" % self.findname[self.index])
                    self.f = open(self.save_txt_dir + self.findname[self.index] + self.object_type, "r")
                else:
                    print("没字了")
                    break

        cv2.destroyAllWindows()

    def init_write(self, img_init):
        for i in range(self.channles):
            img_init[:, :, i] = 255
    # def __enter__(self):
    #


if __name__ == '__main__':
    recurrent = Recurrent(["永", "亟", "辉", "斌","恒", "了", "莫"])
    recurrent.main()
