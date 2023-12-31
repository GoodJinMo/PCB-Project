import os
import cv2
import numpy as np
import pandas as pd
import random
import os
import xml.etree.ElementTree as ET

class Augmentation_bri:
    def __init__(self, minv, maxv, data_file, xml_file_path, original_image_path, output_label_path, output_folder):
        self.minv = minv
        self.maxv = maxv
        self.data_file = data_file
        self.xml_file_path = xml_file_path
        self.original_image_path = original_image_path
        self.output_label_path = output_label_path
        self.output_folder = output_folder
        self.save_image()
        self.qa=self.xml_to_txt()
        
    # %% pcb image 불러오는 함수    
    def create_defectlist(self):
        pcb_paths = [os.path.join(self.original_image_path, folder) for folder in self.data_file]

        # PCB 결함 폴더별 이미지 리스트
        defect_list = []
        for folder_path in pcb_paths:
            file_list = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.lower().endswith('.jpg')]
            defect_list.append(file_list)
        return defect_list
    
    # %% pcb 기판 밝기 조절
    def brightness_var(self,image_path):
    
        pcb_image = cv2.imread(image_path)
        
        gmin, gmax = np.min(pcb_image), np.max(pcb_image)
        avg_intensity = np.mean(pcb_image)
        input_val = random.uniform(self.minv, self.maxv)
        target_intensity = avg_intensity + input_val  # 평균조도 input_val 값에 따라 변화
        pcb_var = np.clip(pcb_image * (target_intensity / avg_intensity), 0, 255).astype(np.uint8)
    
        
        filename = os.path.basename(image_path)
        output_file = os.path.join(self.output_folder, f"var_{filename}")
        cv2.imwrite(output_file, pcb_var)
        
        return output_file
    
    # %% 밝기 조절된 pcb 이미지 저장    
    def save_image(self):
        defect_list = self.create_defectlist()
        saved_image_paths = []
        # 모든 이미지들을 어둡게/밝게 만들어서 저장 (output_folder가 없으면 자동으로 생성됨)
        self.output_folder = "C:/work/python/PCB/PCB_DATASET/output_folder/var"
        os.makedirs(self.output_folder, exist_ok=True)
       
        for image_list in defect_list:
            for image_path in image_list:
                saved_path = self.brightness_var(image_path)
                saved_image_paths.append(saved_path)
        return saved_image_paths
        
    # %% xml to txt
    def xml_to_txt(self):
        xml_paths = [os.path.join(self.xml_file_path, folder) for folder in data_file]

        defect_xlist = []
        for xfolder_path in xml_paths:
            xfile_list = [os.path.join(xfolder_path, file) for file in os.listdir(xfolder_path) if file.lower().endswith('.xml')]
            defect_xlist.append(xfile_list)

        output_label_path = "C:/work/python/PCB/PCB_DATASET/output_folder/vart"
        os.makedirs(output_label_path, exist_ok=True)

        object_mapping = {"missing_hole": 0,
                          "mouse_bite": 1,
                          "open_circuit": 2,
                          "short": 3,
                          "spur": 4,
                          "spurious_copper": 5}
        txt_path_list = []
        for xfile_list in defect_xlist:
            for xml_file in xfile_list:
                label_output_filename = f"var_{os.path.basename(xml_file).replace('.xml', '.txt')}"
                label_output_file_path = os.path.join(self.output_label_path, label_output_filename)
                txt_path_list.append(label_output_file_path) 
                tree = ET.parse(xml_file)  # xml_file을 파싱하여 ElementTree를 생성
                root = tree.getroot()

                with open(label_output_file_path, 'w') as label_file:
                    for obj in root.iter('object'):
                        obj_name = obj.find('name').text
                        obj_label = object_mapping[obj_name]  # 객체 이름을 숫자로 매핑
                        bndbox = obj.find('bndbox')
                        xmin = int(int(bndbox.find('xmin').text) )
                        ymin = int(int(bndbox.find('ymin').text) )
                        xmax = int(int(bndbox.find('xmax').text) )
                        ymax = int(int(bndbox.find('ymax').text) )
                        label_file.write(f"{obj_label} {xmin} {ymin} {xmax} {ymax}\n")
        return txt_path_list
    
    def show_dataframe(self):
        img_paths = self.save_image()
        data = {'image_path': img_paths, 'label_path':self.xml_to_txt()}
        df = pd.DataFrame(data)
        df['file_name']=[n.split("\\")[-1][:-4] for n in  df['image_path']]
        
        return df

#%% 실행
data_file = ['Missing_hole' ,'Mouse_bite']#, 'Open_circuit', 'Short', 'Spur', 'Spurious_copper']
xml_file_path = 'C:/work/python/PCB/PCB_DATASET/Annotations'
original_image_path = 'C:/work/python/PCB/PCB_DATASET/images'
output_label_path = "C:/work/python/PCB/PCB_DATASET/output_folder/vart"
output_folder = "C:/work/python/PCB/PCB_DATASET/output_folder/var"

Augmentation_bri(-100,100, data_file, xml_file_path, original_image_path, output_label_path, output_folder)

#result_df= a.show_dataframe()
#result_df
