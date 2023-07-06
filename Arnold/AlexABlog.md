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