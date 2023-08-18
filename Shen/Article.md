# Solar Irradiance 
by Alex Shen

Hello, my name is Alex Shen, and I am a incoming second year undergraduate student at Northwestern University. I work at Argonne National Laboratory this summer as a SULI intern. I spent my time at Argonne working on a model that uses deep learning to estimate the Solar Irradiance of the sun. I managed to get the model completed and built my plugin in the ECR on the sage website.


# Data Preprocessing
In the data preprocessing stage we created a csv file that stored all the images to their matching solar irradiance values. The images were taken from the Sage Waggle Node's top camera and the solar irradiance values were taken from the Argonne National Laboratory tower readings. We made sure to exclude night time photos since there is no sun and we exclusively used summer-time photos as we wanted to stick to a seasonal model that would be able to make estimates more consistently. Furthermore we also eventually downsized the images original 2000x2000 images to 500x500 images since the training was taking a bit too long when the images were larger.

![alt text](https://github.com/AlexShen21/example_images/blob/b59b13ede783a2601ef7a0bee47b89c8e62db4fb/1655423969884923771-sample.jpg)
example image


# Training and Model
In our training, before the image was transformed to a tensor, the image was resized down to 224x224 to stay consistent with the pre-trained models. The image was also randomly flipped with a 50% chance and rotated randomly between 0-359 degrees so the model would be able to generalize better. For our model we compared all of the  pretrained ResNet models and the VGG-16 model. However we replaced the last fc layer so that the model would give us a continuous value as an estimate instead of a range. We found that the ResNet 50 model performed the best with the lowest mean absolute error of 82. All in all, I think that the error was small enough to justify creating the plugin. In the plugin the waggle node simply snaps an image of the sky using its top camera, and notes the solar irradiance that the model predicts and publishes it to the Beehive Repository.





