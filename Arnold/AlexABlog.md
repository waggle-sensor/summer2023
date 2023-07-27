# Daily Blog

**June 19th 2023**
I went through orientation in the morning and completed all the required training tasks in Dash just to get them out of the way. Then I created my quad chart and started familiarizing myself with the Waggle github sage python libraries and interface. I talked with Seongha at 2 just to discuss the first steps for my project and to try to make it so I have access to the actual image data. I also set up my environment and plan to start implementing and intial draft of a ResNet model for snow classification tomorrow in PyTorch.

**June 20th 2023**
I created a basic model based on ResNet for transfer learning then worked out getting the images on my computer. I ran into some problems with ubuntu (my firewall was blocking my ability to use apt-get) but after I got that fixed I was able to download all the images between October and November from node W014. Defintely a little rusty in linux, but I'm getting back into it and should be better as the Summer goes on. There are about 750 images with snow on the ground and about 350 without. There are also about 20 where there is only a little bit of snow or where it started snowing in the night and was difficult to tell when there was snow on the ground. I labeled those as unclear. I also excluded the top sensor of W014 as it really only showed the post and there wasn't a good way to see if there was snow on the ground from that angle. Tomorrow I'll take a look at the images from W083, which I assume will have more examples without snow at the very least. Not sure if the different angle/location will matter. Tomorrow I'll also try to complete the training loop and try running the images from W014 through the model to have some results for Thursday.

**June 21st 2023**
Pulled image data from W083 from "2023-02-01T01:00:00Z" to "2023-06-10T01:00:00Z". Camera is pointed at the same location as W014 but a slightly different angle. Also got the classifier working with an test set accuracy of 83%. There are a lot of false positives, and I'm thinking of oversampling the no-snow images to deal with that particular problem and hopefully that helps. If that doesn't work I'll need to start analyzing which images the model is struggling with to see if I can spot any patterns. 

**June 22nd 2023**
Had my first research meeting, I'll have slides ready for next time. Wasn't exactly sure what was expected so I'll be more prepared. Ran into some problems (mostly my own fault) with my pytorch installation and got them all fixed. also decided to remain consistent and count any visible snow as snow. After training ResNet50 for just 9 epochs it achieved an accuracy of 0.980, a precision of 0.988, and a  recall of 0.978. All the false positives are pictures from night and the false negatives are at night or have very little snow at the ground. Regardless, these are very good results and are promising. I'll try ResNet18 to see if I can achieve similar results with a shallower model.

**June 23rd 2023**
This morning my installation decided that sqlite3 wasn't properly installed, so had to sort out that problem again. Also tried using Colab, but confirmed for myself that it is >2 time slower than my local machine since I believe I have a better GPU than the colab machines. I also sorted the images into a new dataset consisting of those which had ice and those that did not. I have a similar problem where it's unclear how much ice covering the river should qualify, but I kicked the can down the road and just counted every image that had any ice on the river as having ice. Could possibly also split images into partial/full covering which could be interesting. Resnet18 had similar metrics but a much stranger loss graph, so I elected to go ahead with Resnet50 as there wasn't a noticable difference in training time on my machine, although that seems strange given the difference in size.

I used the same model model as the snow classifier based on Resnet50. It had final test metrics of {'epoch': 10, 'accuracy': 0.9746478873239437, 'precision': 0.9577039274924471, 'recall': 0.9875389408099688, 'loss': 0.3476980721866581 which are similar to the snow classifier as well. In fact, some of the mistakes look to be ones that I miscategorized when labeling the data. One issue is that the majority of the incorrectly labeled images are at night, so this could be an area for improvement but overall the model seems to be doing well.

One worry I have is that the images look too similar to each other so the model is really just memorizing, but given that the data is being used specifically for the Bad River this may not be an issue? Going to schedule a meeting for next week to discuss next steps/outling the problem and the best design decisions I can make to suit it.

**June 24th 2023**
Wrapped up initial ice classifier today. It didn't converge quite as quickly as the snow classifer, so I trained it for 1.5x longer to get better results.

I also checked through the images form W083 for wild rice, and in the June images I can clearly see the wild rice in the floating-leaf stage, but I don't see them standing up yet. Just from quickly looking online it looks like that usually happens in July so we can check back later in the summer to see if that's visible from the camera, and I expect it will be. As for the question about detecting boat wakes I don't think that would be possible with the current data since the camera doesn't collect images often enough to realistically get pictures of boats with wakes.

Also made a better data pipeline. I was using ImageFolder which I figured out was significantly increasing my training time by >6x which was very bad. This change also allows me to more easily apply augmentations to the training set should I need to. Overall makes my life alot easier and faster. I was very confused as to why it was taking so long so it was good to see that I wasn't going crazy.

List of questions so far
- Do we need to augment the image dataset to make it more generalizable, or does it not matter as much since it's only for images from this site?
- How to pull image metadata? (trying to figure this out today, documentation on using images is lacking)
- Updates on other data sources/other problems to solve
- Target accuracy for the classifiers

**June 25th 2023**
Tried running the snow classifier with noise the model was unable to learn anything, but it could be due to my implementation? Standardized my results for both classiers without noise and scheduled a meeting for tomorrow.

Figured out how to link the image tensors with the other data gathered from the node. Will be important (especially the date/time) when linking it with data collected with other sources

**June 26th 2023**
- Do we need to augment the image dataset to make it more generalizable, or does it not matter as much since it's only for images from this site?
    Going to check how the model does on other nodes such as the one in Oregon in the mountains
- Updates on other data sources/other problems to solve
    None yet, but soon
Wrote a script to divide the images into 16 sub-images and a quick way to sort them into having snow/not having snow. It's going to have to be done manually, but it should go pretty quickly. I might do a preliminary sort based on the brightness of the images calculated from HSV to speed things up. Taking some time to get more familiar with the OpenCV library to work with the images

**July 3rd 2023**
Spent the past few days creating the new dataset from patches of the original one which took  awhile since it was mostly manual. Certainly some mistakes in there but hoping that it won't matter too much. There's a lot more data so it takes a lot longer to train given the limited memory I have, but it does train. 

**July 5th 2023**
Downloaded images from W084. Ran into some problems finding a good node to pull from that a good mix of snow/no snow pictures but eventually settled on the the top camera. The bottom one included the mountain which had snow a lot more often and may not have been as good for intial tests of generalizability. If this set goes well I can try it, but I expect it would be a better use of time to start working on learning and creating a docker application.

**July 6th 2023**
The model performs with about 80% accuracy on the data from Idaho which is a good sign especially since it's a very different image than the nodes on the bad river. Also trying to learn how to create an application for the node now (hopefully to be deployed on the bad river node). Basing a lot of the code from the standing water app since the general idea seems to be pretty similar. Need to look at how arg parser works (and how working through the node works in general)

**July 7th 2023**

Got a working prototype of an app for the node and was able to login in to the waggle folder in the lcrc computer. Need to figure out how to actually test it.

**July 10th 2023** 
Spent some time today cleaning up my data for ease of use. I was keeping copies of images all over sorted in different categories. Have a new file (metadata.csv) that keeps track of which images have snow and which don't as well as an estimate of weather they are during the day or at night. I'm working on performing image segmentation on the snow using guassian mixed means, and it seems more feasible to perform it only on the images taken during the day where it is more clear what has snow and what doesn't. I got a preliminary model working but haven't figured out how to train it on multiple images (if that's even possible) so I'll try to think of a better method tomorrow. Regardless, I have some results which is a good sign that it can be done and may help me create an even better model with some extra steps or using this as a preprocessing step of some kind.

**July 12th 2023**
Got access to the W083 node and got my plugin up and running. Spent time using docker and building it on the node, and prelimary tests are good (saying there isn't snow).

**July 13th 2023**
Had my first real presentation (with slides) this morning that I think went pretty well. Got some good suggestions for things to change or look at. Added a solarization transform to the model to reduce it's reliance on color, and plan on cropping the image to exclude the horizon line above the images for the W083 node. I tried using local binary patterns but those performed even worse than color even on the image they were fit to. It may be a parameter problem, but it didn't seem to capture the difference in textures well enough for clustering. I've also looked at Gabor filters which may be more useful but didn't have time to implement it. Refactored my dataset to crop out the sky/horizon on the W083 images to get a better more accurate dataset for that node at least.

**July 17th 2023**
Debated the best way to format the patches to create an actually useful model. Felt like snow on the ground might be more useful but much harder to train the model on such a small dataset, and so opted to instead classify images based on how much snow is in the image in general

**July 18th 2023**
The model works well on the test and training sets from the W083 node (90% accuracy for all three classes) which is a good early sign, but not sure how it will do on new data since there are a lot of examples so it could face the same problem as the earlier model.

**July 19th 2023**
Sounds like we're kind of at a dead end for the snow side of the project which is annoying but it is what it is. I updated the model and app on the node with the improvements I've been working on and I'm shelving the segmentation stuff since it sounds like it won't be needed. Moved on to working on a method to enhance images which can be useful in tasks such as the rideshare stickers since the images are so small and could lead to better predictions if upscaled. Had some trouble with scp but got the rideshare files from Anagha which will be useful.

**July 20th 2023**
Ideas for applications
1. UNET architecture from Seongha 
2. Measuring stick enhancement
3. Using IR image dataset
4. Use new dataset from generated from Anagha plugin 

Citations so far
- Improving Scene Text Image Super-Resolution via Dual Prior Modulation Network
- Image Super-Resolution via Iterative Refinement
- ESRGAN: Enhanced Super-Resolution Generative Adversarial Networks
- Transformer for Single Image Super-Resolution
Unsupervised approach for one image: “Zero-Shot” Super-Resolution using Deep Internal Learning

Two approaches that seem interesting are the self learning approaches such as ZSSR and MZSR which preform better on real world images, but are slower to use since they train for one image. However, they don't require large training sets or even a HR image pair. Could be worth testing. ZSSR might be a good first model to try, then MZSR if that fails to give readable measurements.
The original is in tensorflow (which I am not familiar with and may not integrate as well with other plugins), but I found a pytorch implementation of ZSSR [here](https://github.com/HarukiYqM/pytorch-ZSSR)

https://arxiv.org/pdf/2206.01777.pdf A lightweight edge-computing friendly friendly version, but might not work on real world images. The major problem with a lot of networks is that they only perform well on specific degradation patterns, so need to find a model that does well on RL datasets or retrain a model on a custom dataset (like was suggested during the meeting). For practical use it would likely need to be retrained for the specific camera used on the nodes since those will be the best way to correct for the degradation on the nodes.

**July 21st 2023**
Ran some tests with ZSSR using the measuring stick and rideshare images. Overall quality was pretty good, but where the image was indecipherable it didn't help too much. With the measuring sticks it might actually be better because it increases the size of the ticks even if the numbers themselves aren't any clearer. If we can get a dataset using the actual camera on the node it might work better

**July 24th 2023**
Updated my snow plugin to download the .pth file from _LCRC_ instead of being uploaded from my computer. Also started working on my snow classifier plog post for next week, should be relatively straightforward.

On the super-resolution front, I've started implementing SRCNN, which is a simple convolutional network. There are a lot of more complicated versions but given time constraints (and my own limitations) I'll start with this. If it works great, if it doesn't I'll try other methods. ZSSR will be a good pretrained model to compare it to. Using the Div2k dataset to train the model. A common method is to use bicubic resampling to create the LRimage pair, so that's what I'll start with. Next thing will be the unknown degradation to mirror the conditions on the node camera.

Wrote the simple model, downloaded an initial train/test set of DIV2K and set up a dataset to load the data into tensors. Had to do it lazily due to memory constraints which will impact speed but shouldn't be terrible hopefully.

**July 25th 2023**
Trained a preliminary SRCNN model. It trains by randomly cropping the high res and low res images. It then upscales the LR image bicubicly and is fed into the network, where it tries to minimize MSE loss.  

**July 26th 2023**
The SRCNN results look like it's just blurring the bicubic interpolation on the mild blur set which i strange. When I tried with with bicubic degradation it doesn't seem to change much, which leads me to think there might be some bug in my code or data loading pipeline? Very confused.
