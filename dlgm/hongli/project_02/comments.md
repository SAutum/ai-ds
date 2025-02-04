increasing number of pixels shows different scales of the cell structure and the trained model may not scale well to the new data.
as we tried both 64 and 128 pixels, the model shows improvement in training images with higher resolution

beside the nature of InceptionV3 is not medical, the input of the model is 299x299x3,
and the deepest layer has 2048 features, our generated data is 64x64x3, which is needed to be rescaled to 299x299x3 to be fed into the model, meaning the original image have much less information than the model is trained on. This may cause the model to not scale well to our data (75 x 75 is the minimum size for InceptionV3 https://keras.io/api/applications/inceptionv3/)

For our data, if the image size is small, some regions out of the cell
may be included in the image, which may cause the model to learn the background noise rather than the cell structure. These regions are usually black or while.
one of the solutions to deal with black/whitetiles is to check the median of the pixel values of the image, if it is less than a certain threshold (black) or more than a certain threshold (white), the image is considered as a black/white tile and should be removed from the dataset. In this way the cropped images will be more likely to contain the cell structure. We implemented such thresholding in data sampling.

Possible reasons of why stylegan2 works better than vanilla GAN:
- stylegan introduces
