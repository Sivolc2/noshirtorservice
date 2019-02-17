# USAGE
# python classify.py --model output/fashion.model \
        #	--categorybin output/category_lb.pickle --colorbin output/color_lb.pickle \
        #	--image examples/black_dress.jpg

# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import tensorflow as tf
import numpy as np
import argparse
import imutils
from imutils import paths
import pickle
import cv2
import pandas as pd
import webcolors
import logging

def get_complementary(color):

    color = color[1:]

    color = int(color, 16)

    comp_color = 0xFFFFFF ^ color

    comp_color = "#%06X" % comp_color

    if comp_color == "#5AD5D5":
        return "blue"
    return webcolors.hex_to_name(comp_color)

def opposite(cat):
    if cat == 'pants':
        return 'shirt'
    else:
        return 'pants'
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True,
        help="path to trained model model")
ap.add_argument("-l", "--categorybin", required=True,
        help="path to output category label binarizer")
ap.add_argument("-c", "--colorbin", required=True,
        help="path to output color label binarizer")
ap.add_argument("-i", "--image", required=True,
        help="path to input image")
args = vars(ap.parse_args())
'''
df = pd.DataFrame([

        ],
                columns=['Color', 'Category', 'Recommendation']
        )
number = 0
'''
imagePaths = sorted(list(paths.list_images(args["image"])))

for image in imagePaths:

    # load the image
        image = cv2.imread(image)
        output = imutils.resize(image, width=400)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # pre-process the image for classification
        image = cv2.resize(image, (96, 96))

        # HISTOGRAM EQUALIZER

        img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)

        # equalize the histogram of the Y channel
        img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])

        # convert the YUV image back to RGB format
        image = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)

        # END HISTOGRAM

        image = image.astype("float") / 255.0
        image = img_to_array(image)
        image = np.expand_dims(image, axis=0)

        # load the trained convolutional neural network from disk, followed
        # by the category and color label binarizers, respectively
        #print("[INFO] loading network...")
        model = load_model(args["model"], custom_objects={"tf": tf})
        categoryLB = pickle.loads(open(args["categorybin"], "rb").read())
        colorLB = pickle.loads(open(args["colorbin"], "rb").read())

        # classify the input image using Keras' multi-output functionality
        #print("[INFO] classifying image...")
        (categoryProba, colorProba) = model.predict(image)

        # find indexes of both the category and color outputs with the
        # largest probabilities, then determine the corresponding class
        # labels
        categoryIdx = categoryProba[0].argmax()
        colorIdx = colorProba[0].argmax()
        categoryLabel = categoryLB.classes_[categoryIdx]
        colorLabel = colorLB.classes_[colorIdx]

        # draw the category label and color label on the image
        '''categoryText = "category: {} ({:.2f}%)".format(categoryLabel,
                categoryProba[0][categoryIdx] * 100)
        colorText = "color: {} ({:.2f}%)".format(colorLabel,
                colorProba[0][colorIdx] * 100)
        cv2.putText(output, categoryText, (10, 25), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2)
        cv2.putText(output, colorText, (10, 55), cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (0, 255, 0), 2)'''

        # display the predictions to the terminal as well
        #print("[INFO] {}".format(categoryText))
        #print("[INFO] {}".format(colorText))

        #df.append(pd.DataFrame([[colorLabel, categoryLabel]]))
        # df.loc[number] = [colorLabel, categoryLabel, get_complementary(webcolors.name_to_hex(colorLabel)) + " " + opposite(categoryLabel)]
        # number += 1

        format_list = [categoryLabel,colorLabel,get_complementary(webcolors.name_to_hex(colorLabel))]
        print("<h2>{}</h2><h1>{}</h1><br/><br/><h3>Try it with</h3><h2>{}</h2>".format(*format_list))
        #print(categoryLabel)
        #print(colorLabel)
        #print(get_complementary(webcolors.name_to_hex(colorLabel)))

        # show the output image
        #cv2.imshow("Output", output)
        #cv2.waitKey(0)

        #python classify.py --model output/fashion.model --categorybin output/category_lb.pickle --colorbin output/color_lb.pickle --image examples/black_dress.jpg
#df.to_csv(r'MacintoshHD/Users/dominatingdonut/Downloads/nsns.csv')
#export_csv = df.to_csv ('nsns.csv', header=True)
