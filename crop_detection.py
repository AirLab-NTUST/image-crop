#MASKRCNN don't need root, darken, only using single bud and angle imforamtion.
import cv2
import glob
import math
import numpy as np
import os
from tqdm import tqdm

def cal_dis(pts1,pts2):
    dist = math.sqrt(int(pts2[0]-pts1[0])**2 + int(pts2[1]-pts1[1])**2)
    return dist
def resized_img(img,percent):
    width = int(img.shape[1]*percent/100)
    height = int(img.shape[0]*percent/100)
    dim = (width,height)
    resized = cv2.resize(img,dim,interpolation = cv2.INTER_AREA)
    return resized

if __name__ == "__main__":
     # Change the direction that is used to save the image
    path_save_image = "./Single_bud_dataset/images"

    '''if it had already the annotation files'''

    path_save_annotation = "./Single_bud_dataset/annotation"  

    # If we want to change the resize, I noted below.
    count = 2703
    if not os.path.exists(path_save_image ):
        os.mkdir(path_save_image)
    # path_im = sorted(glob.glob('./subimage_13/*.jpg'))
    path_im = sorted(glob.glob('/home/airlab/Desktop/IMAGE_CROP/Single_bud_dataset/datas3_singlebud/datas3/*.jpg'))
    for file in tqdm(path_im,total=len(path_im)):
        order_im = str(file).split("/")[-1]
        order_im_compare = str(file).split("/")[-1].split(".")[0]
        print("order image", order_im_compare)
        file_im = cv2.imread(file)
        lower = [0, 52, 44]
        upper = [179, 255, 255]
        HSV = np.vstack((lower, upper))
        ORANGE_MIN = np.array([0, 52, 44],np.uint8)
        ORANGE_MAX = np.array([179, 255, 255],np.uint8)
        hsv_img = cv2.cvtColor(file_im,cv2.COLOR_BGR2HSV)
        thresh = cv2.inRange(hsv_img, ORANGE_MIN,ORANGE_MAX)
        kernel1 = np.ones((9,9), np.uint8)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel1)
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel1)
        kernel = np.ones((5, 5), np.uint8)
        thresh = cv2.erode(thresh, kernel, iterations=3)
        thresh = cv2.dilate(thresh, kernel, iterations=9)
        contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        # first_cnt = max(contours, key = cv2.contourArea)
        height =[]
        width = []
        x_w = []
        y_h = []
        for i, cnt in enumerate(contours):
            # cv2.drawContours(file_im, [cnt], 0, (0,255,0), 3)
            x,y,w,h = cv2.boundingRect(cnt)
            height.append(y+h+100)
            width.append(x+w+100)
            x_w.append(x-100)
            y_h.append(y-100)

        max_h = max(height)
        max_w = max(width)
        min_h = min(y_h)
        min_w = min(x_w)
        ct_y = (max_h + min_h)//2 
        ct_x = (min_w + max_w)//2
        xa = min_w
        ya = min_h
        cx = ct_x
        cy= ct_y
        d = int(cal_dis((xa,ya),(cx,cy)))
        # Change here with size you want
        x_min_cut = cx-int(d*0.7*80/57)
        x_max_cut = cx+int(d*0.7*80/57)
        y_min_cut = cy-int(d*0.7)
        y_max_cut = cy+int(d*0.7)
        print("file_im.shape[1]",file_im.shape[1])
        print("y", y_max_cut)
        if x_max_cut > file_im.shape[1]:
            y_max_cut = max_h
            y_min_cut = min_h
            x_min_cut = min_w
            x_max_cut = max_w
        crop_img = file_im[y_min_cut:y_max_cut,x_min_cut:x_max_cut]

        # cv2.circle(file_im, (ct_x,ct_y), 2, (0, 0, 255), 2)
        # cv2.rectangle(file_im, (x_min_cut, y_min_cut), (x_max_cut,y_max_cut),(0, 0, 255), 2)
        # cv2.imshow("image", resized_img(file_im,100))
        # k = cv2.waitKey(0)
        # if k ==ord('q') or k ==ord('Q'):
        #     break
        # Change here
        crop_resize = cv2.resize(crop_img,(640,456),interpolation = cv2.INTER_AREA) #(w,h)
        cv2.imwrite(path_save_image + '{}.jpg'.format(count), crop_resize)