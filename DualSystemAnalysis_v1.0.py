import os
from utils import autoPair
from utils import getBBOXInfo,determineType_Dual,visualCellType
import sys
program_name = sys.argv[0]
arguments = sys.argv[1:]

count = len(arguments)
if count>0:
    if arguments[0]=='part1':
        #### Part1: Pair DIH image with Fluorescent image
        fluo_folder='/media/jp/disk0003/autoPair/Fluor_run7'
        dih_folder='/media/jp/disk0003/autoPair/DIH_run7'
        #### Do not include / in the above two folder names
        #### Sample fluo_folder parameter: 'D:/Research/Astrin_cancer/code/autoPair/Fluor_run7_enh'
        #### Sample dih_folder parameter: 'D:/Research/Astrin_cancer/code/autoPair/DIH_run7_jetson_enh'

        paired_folder='/media/jp/disk0003/paired/'
        #### Remember to include / in the above folder name
        #### Sample paired_folder parameter: 'D:/Research/Astrin_cancer/code/autoPair/paired/'

        autoPair(fluo_folder,dih_folder,paired_folder)

    elif arguments[0]=='part3':
        #### Part3: Use the predicted bbox result to categorize cells and analyze result
        ####type description####
        ####1:Fluorescent + dih type1
        ####2:Fluorescent + dih type2
        ####3:Fluorescent + dih type1&2
        ####4:non-Fluorescent + dih type1
        ####5:non-Fluorescent + dih type2
        ####6:non-Fluorescent + dih type1&2
        dih_folder='/media/jp/DINGO/test/DIH_visual'
        fluor_folder='/media/jp/DINGO/test/Fluor_visual'
        source_dih_folder='/media/jp/disk0003/paired/DIH_run7'
        result_folder='/media/jp/DINGO/test/Result_visual/'
        try:
            os.mkdir(result_folder)
        except OSError as error: 
            print(error)

        dih_bbox_info=getBBOXInfo(dih_folder)
        fluor_bbox_info=getBBOXInfo(fluor_folder)
        cellTypeTotal=determineType_Dual(dih_bbox_info,fluor_bbox_info)
        visualCellType(source_dih_folder,result_folder,cellTypeTotal)
else:
    print('Expect input: part1, or part3')
    print('Part1: Pair DIH image with Fluorescent image')
    print('Part3: Use the predicted bbox result to categorize cells and analyze result')
