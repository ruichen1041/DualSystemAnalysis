import cv2
import glob
import os
import numpy as np
from shutil import copyfile
from PIL import Image
def getFileName(org_name):
    EXT_FLAG=0
    current_name=os.path.basename(org_name)
    while EXT_FLAG==0:
        if os.path.splitext(current_name)[1]=='':
            return current_name
        else:
            current_name=os.path.splitext(current_name)[0]
            
def getInfo(current_name):
    CON_FLAG=1
    current_digit=1
    current_id=''
    while CON_FLAG==1:
        current_id_single=current_name[len(current_name)-current_digit]
        if current_id_single=='-':
            break
        current_id=current_id_single+current_id
        current_digit=current_digit+1
    
    current_second=current_name[len(current_name)-current_digit-2]+current_name[len(current_name)-current_digit-1]
    return current_second,current_id

def sortFileName(file_list):
    index_list=np.zeros([len(file_list)])
    current_num=0
    for fileName in file_list:
        file_name=getFileName(fileName)
        _,current_id=getInfo(file_name)
        #print(int(current_id))
        index_list[current_num]=current_id
        current_num=current_num+1
    return index_list

def enh_imgs(image_list,enh_save_dir):
    if not os.path.exists(enh_save_dir):
        os.makedirs(enh_save_dir)
    image_size=cv2.imread(image_list[0]).shape
    bg=np.zeros(image_size)

    for name in image_list:
        image=cv2.imread(name)
        bg=bg+image.astype(float)
    bg=bg/len(image_list)

    for name in image_list:
        image=cv2.imread(name)
        current_enh = np.abs((image.astype(float)-bg)*2+100)
        current_enh_output=np.zeros([current_enh.shape[0],current_enh.shape[1]])
        current_enh_output=current_enh[:,:,0]
        current_name=os.path.basename(os.path.normpath(name))
        Image.fromarray(current_enh_output.astype(np.uint8)).save(os.path.join(enh_save_dir,current_name))

def autoPair(fluo_folder,dih_folder,paired_folder):
    fluo_folder_name=os.path.basename(fluo_folder)
    dih_folder_name=os.path.basename(dih_folder)

    fluo_folder=fluo_folder+'/'
    dih_folder=dih_folder+'/'
    fluo_image=sorted(glob.glob(os.path.join(fluo_folder, "*.tiff")))
    dih_image=sorted(glob.glob(os.path.join(dih_folder, "*.tiff")))

    try:
        os.mkdir(paired_folder)
    except OSError as error: 
        print(error)

    try:
        os.mkdir(paired_folder+dih_folder_name+'/')
    except OSError as error: 
        print(error)

    try:
        os.mkdir(paired_folder+fluo_folder_name+'/')
    except OSError as error: 
        print(error)


    dih_sorted_index=sortFileName(dih_image)
    current_index=0
    while current_index<len(dih_image):
        print(str(np.array(dih_image)[dih_sorted_index==current_index]))
        current_filename=getFileName(str(np.array(dih_image)[dih_sorted_index==current_index]))
        current_second,_=getInfo(current_filename)
        if current_index==0:
            begin_second=current_second
        else:
            if begin_second!=current_second:
                dih_begin_second=current_second
                break
        current_index=current_index+1

    dih_begin_index=current_index
    print('DIH begins from:')
    print(dih_begin_index)
    #print(dih_begin_second)

    fluo_sorted_index=sortFileName(fluo_image)
    current_index=0
    while current_index<len(fluo_image):
        print(str(np.array(fluo_image)[fluo_sorted_index==current_index]))
        current_filename=getFileName(str(np.array(fluo_image)[fluo_sorted_index==current_index]))
        current_second,_=getInfo(current_filename)
        if current_second==dih_begin_second:
            fluo_begin_index=current_index
            break
        current_index=current_index+1
    print('Fluorescent begins from:')
    print(fluo_begin_index)

    current_fluo_index=fluo_begin_index
    current_dih_index=dih_begin_index

    while current_fluo_index<len(fluo_image) and current_dih_index<len(dih_image):
        current_dih_filename=np.array(dih_image)[dih_sorted_index==current_dih_index][0]
        copyfile(current_dih_filename, paired_folder+dih_folder_name+'/'+os.path.basename(current_dih_filename))
        current_fluo_filename=np.array(fluo_image)[fluo_sorted_index==current_fluo_index][0]
        copyfile(current_fluo_filename, paired_folder+fluo_folder_name+'/'+os.path.basename(current_fluo_filename))

        #print(str(np.array(dih_image)[dih_sorted_index==current_dih_index]))
        #print(str(np.array(fluo_image)[fluo_sorted_index==current_fluo_index]))
        current_dih_index=current_dih_index+1
        current_fluo_index=current_fluo_index+1
        
    image_list=sorted(glob.glob(paired_folder+dih_folder_name+'/*.tiff'))
    enh_save_dir = paired_folder+dih_folder_name+'/'
    enh_imgs(image_list,enh_save_dir)
    
    image_list=sorted(glob.glob(paired_folder+fluo_folder_name+'/*.tiff'))
    enh_save_dir = paired_folder+fluo_folder_name+'/'
    enh_imgs(image_list,enh_save_dir)
    
    image_list=sorted(glob.glob(paired_folder+fluo_folder_name+'/*.tiff'))
    enh_save_dir = paired_folder+fluo_folder_name+'/'
    enh_imgs(image_list,enh_save_dir)
    
def getBBOXInfo(log_folder):
    log_folder_name=os.path.basename(log_folder)
    log_folder=log_folder+'/'
    log_list=sorted(glob.glob(os.path.join(log_folder, "*.txt")))
    log_sorted_index=sortFileName(log_list)
    current_index=int(min(log_sorted_index))
    log_index=0
    init_flag=0
    while current_index<int(max(log_sorted_index)+1):
        log_index=log_index+1
        current_file_name=os.path.basename(str(np.array(log_list)[log_sorted_index==current_index]))[:-2]
        #print(current_file_name)
        bbox_info=np.loadtxt(log_folder+current_file_name)
        if bbox_info.size==0:
            current_index=current_index+1
            #print('empty')
            continue  
        else:
            try:
                new_bbox_info=np.zeros([bbox_info.shape[0],bbox_info.shape[1]+1])
                new_bbox_info[:,0]=log_index
                new_bbox_info[:,1:bbox_info.shape[1]+1]=bbox_info
                #print(new_bbox_info)
            except: 
                new_bbox_info=np.zeros([1,bbox_info.shape[0]+1])
                new_bbox_info[:,0]=log_index
                new_bbox_info[:,1:bbox_info.shape[0]+1]=bbox_info
                #print(new_bbox_info)
            if init_flag==0:
                all_info=new_bbox_info
                init_flag=1
            else:
                all_info=np.concatenate((all_info, new_bbox_info), axis=0)
            current_index=current_index+1
    return all_info

def determineType(bbox1,bbox2):
    x_diff=np.abs(bbox1[0]-bbox2[0])
    y_diff=np.abs(bbox1[1]-bbox2[1])
    w_avg=(bbox1[2]+bbox2[2])/2
    h_avg=(bbox1[3]+bbox2[3])/2
    x_score=x_diff-w_avg
    y_score=y_diff-h_avg
    #print(x_score)
    #print(y_score)
    if x_score<0 and y_score<0:
        return 1
    else:
        return 0
    
def determineType_Dual(dih_bbox_info,fluor_bbox_info):
    max_index=np.max([max(dih_bbox_info[:,0]),max(fluor_bbox_info[:,0])])
    ####type description####
    ####1:Fluorescent + dih type1
    ####2:Fluorescent + dih type2
    ####3:Fluorescent + dih type1&2
    ####4:non-Fluorescent + dih type1
    ####5:non-Fluorescent + dih type2
    ####6:non-Fluorescent + dih type1&2
    for i in range(int(max_index)):
        debug_flag=0
        current_dih_bbox=dih_bbox_info[dih_bbox_info[:,0]==i+1,:]
        current_fluor_bbox=fluor_bbox_info[fluor_bbox_info[:,0]==i+1,:]
        if current_fluor_bbox.size>0:
            #print(current_fluor_bbox)
            #print(current_dih_bbox)
            total_status_list=np.zeros([current_dih_bbox.shape[0],1])
            for j in range(current_fluor_bbox.shape[0]):
                current_status_list=np.zeros([current_dih_bbox.shape[0],2])
                for k in range(current_dih_bbox.shape[0]):
                    current_status=determineType(current_fluor_bbox[j,2:6],current_dih_bbox[k,2:6])
                    current_status_list[k,0]=k
                    current_status_list[k,1]=current_status
                #print(current_status_list)
                if np.sum(current_status_list[:,1])==1:
                    total_status_list[current_status_list[:,1]==1,0]=current_dih_bbox[current_status_list[:,1]==1,1]+1
                elif np.sum(current_status_list[:,1])>1:
                    total_status_list[current_status_list[:,1]==1,0]=3   
            for j in range(current_dih_bbox.shape[0]):
                current_status_list=np.zeros([current_dih_bbox.shape[0],2])
                #print(j)
                for k in range(current_dih_bbox.shape[0]):
                    current_status=determineType(current_dih_bbox[j,2:6],current_dih_bbox[k,2:6])
                    if k==j:
                        current_status=0
                    if current_dih_bbox[j,1]==current_dih_bbox[k,1]:
                        current_status=0
                    current_status_list[k,0]=k
                    current_status_list[k,1]=current_status
                #print(current_status_list)
                if np.sum(current_status_list[:,1])==0:
                    if total_status_list[j,0]==0:
                        total_status_list[j,0]=current_dih_bbox[j,1]+4
                elif np.sum(current_status_list[:,1])>0:
                    if total_status_list[j,0]==0:
                        debug_flag=1
                        total_status_list[j,0]=6
        else:
            total_status_list=np.zeros([current_dih_bbox.shape[0],1])
            for j in range(current_dih_bbox.shape[0]):
                current_status_list=np.zeros([current_dih_bbox.shape[0],2])
                #print(j)
                for k in range(current_dih_bbox.shape[0]):
                    current_status=determineType(current_dih_bbox[j,2:6],current_dih_bbox[k,2:6])
                    if k==j:
                        current_status=0
                    if current_dih_bbox[j,1]==current_dih_bbox[k,1]:
                        current_status=0
                    current_status_list[k,0]=k
                    current_status_list[k,1]=current_status
                #print(current_status_list)
                if np.sum(current_status_list[:,1])==0:
                    if total_status_list[j,0]==0:
                        total_status_list[j,0]=current_dih_bbox[j,1]+4
                elif np.sum(current_status_list[:,1])>0:
                    if total_status_list[j,0]==0:
                        debug_flag=1
                        total_status_list[j,0]=6
        current_bboxWithType=np.zeros([current_dih_bbox.shape[0],current_dih_bbox.shape[1]+1])
        current_bboxWithType[:,0:current_dih_bbox.shape[1]]=current_dih_bbox
        #print(current_bboxWithType.shape)
        current_bboxWithType[:,current_dih_bbox.shape[1]]=total_status_list.T
        if i==0:
            bboxWithTypeTotal=current_bboxWithType
        else:
            bboxWithTypeTotal=np.concatenate((bboxWithTypeTotal, current_bboxWithType), axis=0)
        '''
        if debug_flag==1:
            print(i)
            print(current_dih_bbox)
            print(total_status_list)
        '''
    return bboxWithTypeTotal

def visualCellType(log_folder,result_folder,cellTypeTotal):
    statResult=open(result_folder+'resultStat.txt','a')
    colorMap=[[0,255,255],
          [255,0,255],
          [255,255,0],
          [255,0,0],
          [0,255,0],
          [0,0,255]]
    log_folder_name=os.path.basename(log_folder)
    log_folder=log_folder+'/'
    log_list=sorted(glob.glob(os.path.join(log_folder, "*.tiff")))
    log_sorted_index=sortFileName(log_list)
    #print(max(log_sorted_index))
    current_index=int(min(log_sorted_index))
    log_index=0
    while current_index<int(max(log_sorted_index)+1):
        #print(current_index)
        log_index=log_index+1
        current_file_name=os.path.basename(str(np.array(log_list)[log_sorted_index==current_index]))[:-2]
        #print(log_folder+current_file_name)
        current_canvas=cv2.imread(log_folder+current_file_name)
        current_bbox_info=cellTypeTotal[cellTypeTotal[:,0]==log_index,:]
        current_stat=np.zeros([1,7])
        current_stat[0,0]=log_index
        #print(current_bbox_info.shape)
        for i in range(current_bbox_info.shape[0]):
            x1=int(current_bbox_info[i,2])
            y1=int(current_bbox_info[i,3])
            x2=int(current_bbox_info[i,2]+current_bbox_info[i,4])
            y2=int(current_bbox_info[i,3]+current_bbox_info[i,5])
            current_stat[0,int(current_bbox_info[i,6])]=current_stat[0,int(current_bbox_info[i,6])]+1
            current_canvas=cv2.rectangle(current_canvas, (x1, y1), (x2, y2), colorMap[int(current_bbox_info[i,6]-1)], 2)
            current_canvas=cv2.putText(current_canvas, str(int(current_bbox_info[i,6])), (x1-10, y1-10), cv2.FONT_HERSHEY_SIMPLEX,1, [255,255,255], 2, cv2.LINE_AA)
        current_index=current_index+1
        cv2.imwrite(result_folder+'type_'+current_file_name,current_canvas)
        if log_index==1:
            total_stat=current_stat
        else:
            total_stat=np.concatenate((total_stat, current_stat), axis=0)
    for i in range(log_index):
        np.savetxt(statResult,total_stat[i,:], fmt='%3d', newline=' ')
        statResult.write('\n')
    print(total_stat)
    statResult.close()
   
