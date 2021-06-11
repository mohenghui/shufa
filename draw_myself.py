#encoding=utf-8
import cv2
import numpy as np
import time
import os.path
class Pen:
    def __init__(self):
        self.save_txt_dir = "./bihua_data/"
        self.index=0
        self.object_name = ["恒","好","莫"]
        self.object_type = ".txt"
        self.mode="w"
        self.width = 256
        self.height = 256
        self.channles = 1
        self.step=0
        self.flag=True
        while(os.path.isfile(self.save_txt_dir+self.object_name[self.index]+self.object_type)):
            print("[%s]字已存在，请删除后再修改"%self.object_name[self.index])
            self.index+=1
            # print(self.index)
            if (self.index >= len(self.object_name)):
                self.flag=False
                break
        if(self.flag):
            self.f = open(self.save_txt_dir+self.object_name[self.index] + self.object_type, "w")
            add_point = '{},{}\n'.format(-1, -1)
            self.f.write(add_point)
        else:
            print("全部字体已存在，请进行删除后修改")
    def wirte(self,event,x,y,flags,parm):
        if event == cv2.EVENT_MOUSEMOVE and flags == cv2.EVENT_FLAG_LBUTTON:
            cv2.circle(img, (x, y), 1, (0), 5,cv2.LINE_AA,0)
            # cv2.circle(img, center=(x, y), radius=3,
            #            color=(0), thickness=-1)
            self.step += 1
            if self.step == 1:
                add_point = '{},{}\n'.format(x, y)
                self.f.write(add_point)
                self.step = 0
        if event == cv2.EVENT_LBUTTONUP:
            add_point = '{},{}\n'.format(-1, -1)
            self.f.write(add_point)
            print('下一笔')
    def init_write(self,img_init):
        for i in range(self.channles):
            img_init[:, :, i] = 255
    def next_write(self):
        self.f = open(self.save_txt_dir+self.object_name[self.index] + self.object_type, "w")


pen_main=Pen()
if pen_main.flag:
    img=np.zeros((pen_main.width,pen_main.height,pen_main.channles),np.uint8)
    pen_main.init_write(img)
    print("第%s个字[%s]"%(pen_main.index+1,pen_main.object_name[pen_main.index]))
    cv2.namedWindow("block")
    cv2.setMouseCallback("block",pen_main.wirte)
    while(1):
        cv2.imshow("block",img)
        k = cv2.waitKey(1)&0xFF
        if k == ord('q'):
            pen_main.f.close()
            break
        if k == ord('c'):
            pen_main.init_write(img)
            pen_main.f.close()
        if k==ord('n'):
            pen_main.f.close()
            pen_main.init_write(img)
            if(pen_main.index<len(pen_main.object_name)-1):
                pen_main.index+=1
                pen_main.next_write()
                print("下一个字[%s]"%pen_main.object_name[pen_main.index])
            else:
                print("没字了")
                break
    cv2.destroyAllWindows()