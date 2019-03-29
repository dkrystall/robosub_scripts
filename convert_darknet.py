'''
This script converts image labels in the BBox-Label-Tool format:

<num of objects in the image>
<x_min1> <y_min1> <x_max1> <y_max1> <class1>
<x_min2> <y_min2> <x_max2> <y_max2> <class2>
...

and generates new labels compatible with darknet in this format:

<class_id1> <x_center1> <y_center1> <width1> <height1>
<class_id2> <x_center2> <y_center2> <width2> <height2>
...

Based on voc_label.py under darknet/scripts/
'''

import os

classes = ["dice1", "dice2", "dice3", "dice4", "dice5", "dice6"]
NEW_LABELS_PATH = 'new_labels' # is created if doesn't exist
OLD_LABELS_PATH = 'labels'
IMAGES_PATH = 'images'
IMG_LIST_FILE = 'img_list.txt' # is created if doesn't exist

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

wd = os.getcwd()
if not os.path.exists(NEW_LABELS_PATH):
    os.makedirs(NEW_LABELS_PATH)
label_ids = os.listdir(OLD_LABELS_PATH) # gets file names of all input labels
image_ids = os.listdir(IMAGES_PATH) # gets file names of all images
list_file = open(IMG_LIST_FILE, 'w') # file containing list of image names
for image_id in image_ids:
    list_file.write('%s/%s/%s\n'%(wd, IMAGES_PATH, image_id)) # full image path/name
list_file.close()

# iterates through the old labels and outputs new labels with the same name
for label_id in label_ids:
    with open('%s/%s'%(OLD_LABELS_PATH, label_id)) as in_file: # old label dir
        out_file = open('%s/%s'%(NEW_LABELS_PATH, label_id), 'w') # new label dir
        # assuming all of bumblebee's images are same size; TODO generalize w, h
        w = 1024
        h = 768
        first_line = True
        for line in in_file: # each line describes an object (except the first line which only states num of objs)
            if first_line: # skips first line
                first_line = False
            else:
                xmin, ymin, xmax, ymax, cls = line.split(" ")
                cls_id = classes.index(cls.strip("\n")) # TODO make sure class ids don't clash with pre-existing ids
                b = (float(xmin), float(xmax), float(ymin), float(ymax))
                bb = convert((w,h), b)
                out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        out_file.close()
