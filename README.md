Digit-Classifier
================

This project is an implementation of a classifier that classifies images of handwritten images as they're actual number using the similarity with K-Nearest Neighbors. Each set of features is represented by a vector. The metric used to measure nearest neighbors is euclidean distance between two vectors.

###Input
The input can be found in /dataset in .csv files. It is divided into *Labels.csv and *Features.csv where the ith line in labels corresponds to the ith line of features. Actual images can be found in /digitimages. Each line represents a 28x28 image.

An example of the input:
#####Image:
![Input image](https://github.com/vinee109/Digit-Classifier/blob/master/digitImages/train/trainDigit1.png "Sample Input")  
#####Label:  
`1`  
#####Features:  
`0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, ...`  
Each number represents a normalized pixel value at a particular pixel. For each line there are at least 784 features 

###Usage
To run the program you can use the following line with optional flags  
`python digit_classification.py`  
Option Flags  
```
-n, --train               <path to training features>
-r, --trainLabel          <path to training labels>
-v, --validation          <path to validation features>
-a, --validationLabel     <path to validation labels>
-k, --k                   <number of nearest neighbors to classify by>
-t, --t                   <path to test features>
-g, --guesses   <add this flag to output guesses during validation>
```
Sample usage to train and validate:  
`python digit_classification.py -n <path to train features> -r <path to train labels> -v <path to val features> -a <path to val labels> -k 5`  

Sample usage to test:  
`python digit_classification.py -n <path to train features> -r <path to train labels> -k 5 -t <path to test features>`  
The test features must follow the same format as the training features and validation features.

### Added Feature
I have added an extra feature along with the normalized pixel value that is the number of black contiguous regions in the image. This allows for added differentiability between (1, 2, 3, 7), (0, 4, 6, 9) and (8) because all the sets have 1, 2 and 3 contiguous regions respectively.  

###Dependencies
NumPy, SciPy
