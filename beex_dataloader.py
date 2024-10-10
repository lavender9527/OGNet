import rosbag
from cv_bridge import CvBridge 
import numpy as np
import os
import cv2 
import matplotlib.pyplot as plt

def extract_data_from_bag(bag_file,topics):
   bridge = CvBridge() 
   topic_images = {topic: [] for topic in topics}
   
   with rosbag.Bag(bag_file, 'r') as bag: 
      for topic, msg, t in bag.read_messages(topics=topics): 
         if topic in topic_images:
            np_arr = np.frombuffer(msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
            topic_images[topic].append(cv_image)

   return topic_images

def preprocess_images(images, target_size=(224, 224)):
   preprocessed_images = []
   for img in images:
      img = cv2.resize(img, target_size) # 调整图像大小
      img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # 转换颜色空间
      img = img / 255.0 # 归一化
      preprocessed_images.append(img)
   return np.array(preprocessed_images)

def save_images_to_folder(topic_images, base_folder):
   for topic, images in topic_images.items():
      folder_name = '_'.join(topic.split('/')[2:-1]) 
      folder_path = os.path.join(base_folder, folder_name)
      if not os.path.exists(folder_path):
         os.makedirs(folder_path)

      for i, img in enumerate(images):
         filename = os.path.join(folder_path, f"{i}.png")
         cv2.imwrite(filename, img)

def display_images(images, num_images):
   plt.figure(figsize=(15, 5))
   for i in range(num_images):
      plt.subplot(1, num_images, i+1)
      plt.imshow(images[i])
      plt.axis('off')
   plt.show()

file_name='2024-02-29--10-25-39_SiteA_revisit_with_rtk_1.beex'
bag_file = 'seabed/'+file_name
topics = [
   '/ikan/front_cam/image_color/compressed',
   ]
'''topics = [
   '/ikan/front_cam/image_color/compressed',
   '/ikan/front_cam/image_color/clahe/compressed',
   '/ikan/sonar/image/compressed',
   '/ikan/sonar_polar/image/compressed',
   '/ikan/profiling_sonar/image/compressed',
   '/ikan/profiling_sonar_polar/image/compressed'
   ]'''
topic_images= extract_data_from_bag(bag_file,topics)

#preprocessed_images = preprocess_images(images)

for topic, images in topic_images.items():
   display_images(images, num_images=5)

output_folder = 'data/'+file_name.split('.')[0]
save_images_to_folder(topic_images, output_folder)
