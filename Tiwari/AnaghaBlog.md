# Anagha's Daily Work Blog!

#### Here, I will write daily updates for the work done on the Waggle-Sensor project, specifically in understanding feasibility of Waggle sensors in anayzing traffic flow and concentration of ride-sharing vehicles through the streets of Chicago.

<br/>

<details>
<summary> May 31, 2023 </summary>

### May 31, 2023
  
  **Goal:**  Modify image in Python by overlaying Uber (or Lyft) sticker on front car windshield
  
  Worked on image augmentation using OpenCV and Python Imaging Library (PIL):
    
  * Downloaded generic car image and Uber sticker logo from Google
  * Resized Uber sticker through cv2 `resize`
  * Used mouse-click function to identify exact location/coordinate points of Uber sticker location
  * Used cv2, PIL, and Numpy image functions to overlay uber sticker on car, specifically through `warpPerspective` function
  
Other:
  * Gained access to Sage Data Client API Github Repo (contains Waggle sensor street images)
  * Gained authorization credentials for the Sage Continuum Portal (used to download sensor node images from a given timespan, date, location, and plugin)
  
</details>


<br/>


<details>
<summary> June 1, 2023 </summary>

### June 1, 2023
  
  **Goal:**  Download images from `Plugin-Image-Sampler` filter from Waggle nodes in center of Chicago using Sage Continuum Portal and divide all images into equal quadrants for image augmentation
  
  Worked on retrieving and downloading Waggle node images in Chicago from portal for a specific date and sensor:
    
  * Developed `urls.txt` file to retrieve image links from node W026 from Sage Data API, and output the links to a python file to download onto system, with the help of Sean and Yufeng
  * Worked on dividing one image into 4 quadrants using numpy arrays through center x, y, width, and height values, along with cv2 functions
  * Parsed through 20, May 31 images from node W026 using Global python module to divide each image in folder into 4 equal quadrants
  * Wrote each image quadrant into separate file, compiled all quadrants into additional folder
  
Other:
  * First team research meeting today! 
  * Still waiting on ANL login information to access worktation desktop and accounts

</details>


<br/>


<details>
<summary> June 2, 2023 </summary>

### June 2, 2023
  
  **Goal:**  Use quadrant images from `Plugin-Image-Sampler` filter from Waggle nodes and add Uber Stickers to each quadrant (if a car is present)
  
  Worked on writing several functions to read and traverse through one set of quadrant images, add stickers to each car present, and save new image:
    
  * Used OpenCV `imshow` and glob library to read in image and first divide into quadrants
  * Wrote a `setSticker` function to overlay sticker on a chosen section of the image (specifically on the back or front of a car)
  * Parsed through each of the 4 quadrants and called function to overlay sticker on cars if possible (key pressed to skip or move onto next image)
  * Saved each augmented image into the same original file
  
Other:
  * Received ANL login - created Github SSH key and LCRC account to gain access to Waggle Project

</details>


<br/>


<details>
<summary> June 5, 2023 </summary>

### June 5, 2023
  
  **Goal:**  Augment all node images in folder and include randomization feature - traverse through every image (from chosen timespan & node) and add random rideshare logo/sticker on coordinates of choice
  
  Worked on writing several functions to read and traverse through an entire folder of node images, divide them into quadrants, add random sticker in chosen location, and save new image:
    
  * Used OpenCV `imshow` and glob library to read in each image and divide into quadrants
  * Wrote `random_sticker` function to choose random rideshare-vehicle sticker from given folder (from Uber + Lyft)
  * Wrote a `setSticker` function to overlay random sticker on a chosen section of the image (specifically on the back or front of a car)
  * Parsed through each of the 4 quadrants of every image, and call function to overlay sticker on cars if possible (key pressed to skip or move onto next image)
  * Saved each augmented image into the same original file
  
Other:
  * Set up workstation computer, downloaded necessary files/applications and started coding!
  * Committed updated python notebook to GitHub Image_Augmentation folder
  * Downloaded images from node W07B `image-sampler` plugin for the entire month of May (~800 images downloaded) - inspired by Python script + file from Sean

</details>


<br/>


<details>
<summary> June 6, 2023 </summary>

### June 6, 2023
  
  **Goal:**  Start creating training dataset using Node W07B May 1-31, 2023 images.
  
  Add ridesharing vehicle stickers onto images from Node W07B in the Month of May:
    
  * Used image augmentation functions (from RideSharingAddition notebook) to augment more than **960** images 
  * Saved each augmented image into new quadrant file
  
Other:
  * The YoloV7 object identification machine learning framework will be used to create the machine learning ridesharing vehicle model
  * End goal is to finish training, validating, and testing ML model by end of June for Waggle nodes deployed at O'Hare Airport

</details>


<br/>


<details>
<summary> June 7, 2023 </summary>

### June 7, 2023
  
  **Goal:**  Work on training dataset using Node W026 and W02C May 1-31, 2023 images.
  
  Add ridesharing vehicle stickers onto images from Node W026 and W02C in the Month of May:
    
  * Used image augmentation functions (from RideSharingAddition notebook) to augment more than **2000** images (1200 from W026 and 800 from W02C) 
  * Saved each augmented image into new quadrant file
  
Other:
  * Starting to learn about YoloV7 object identification framework + bounding boxes needed to identify stickers on top of cars
  * May need to run model on Google Colab depending on computer GPU capabilities

</details>


<br/>


<details>
<summary> June 8, 2023 </summary>

### June 8, 2023
  
  **Goal:** Start learning (follow/read tutorials, etc.) about YoloV7 object identification ML framework
  
 Start creating Bounding Boxes for sample (30-image) dataset using YoloLabels and train and test data on Google Colab
    
  * Read several tutorials + documentation on YoloV7, its used cases, and basic code blocks on training and testing a custom dataset
  * Set up YoloLabel software to add bounding boxes around the ridesharing stickers - labelled small sample dataset for practice
  * Installed YoloV7 packages, divided sample dataset into training, validation, and testing folders (along with image annotations .txt files)
  * Using Google Colab: trained & tested model - very poor performance but main purpose was to get accustomed to YoloV7 framework
  
Other:
  * Group Research Meeting: May need to add bounding boxes around individual ridesharing stickers or around cars - see which produces optimal results
  * Make sure to use a key metric (i.e. identifying correct number of ridesharing vehicles in picture) to compare different versions of ML model -> seeing which method of bounding boxes produces a number closer to the correct key metric - thanks to Sean for this suggestion
  * Additional thoughts: Can try to use ViLT model proposed by HuggingFace to see its performance - no supervision or previous labeling required (idea proposed by Sean)

</details>


<br/>


<details>
<summary> June 9, 2023 </summary>

### June 9, 2023
  
  **Goal:** Start annotating data using YoloLabel platform
  
 Start creating Bounding Boxes around ridesharing sticker images for each node's data
    
  * Read several tutorials + installation guides on YoloLabel, and the proper method to annotate data (bounding box should only enclose object, and no more)
  * Set up YoloLabel software to add bounding boxes around the ridesharing stickers
  * Started adding bounding boxes for Nodes W07B - currently adding bounding boxes around specific ridesharing stickers (and not the entire car) - may have to test accuracy of model against key metric (# of ridesharing vehicles in image) to test performance
  
Other:
  * Played around with ViLT model by HuggingFace (followed basic tutorial and asked question on pre-trained model - poor performance, but will have to look into it more later!)

</details>


<br/>


<details>
<summary> June 10, 2023 </summary>

### June 10, 2023
  
  **Goal:** Finish annotating data with YoloLabel platform and randomly divide data for model training, validation, and testing
  
 Finish creating Boundary Boxes for all nodes, divided data for each node into folders
    
  * Finished creating boundary boxes for Nodes W02C and W026 - added boxes around specific ridesharing stickers in images - total ~2960 labelled images + text annotation files
  * Wrote Python script (`divide_data.ipynb`) to randomly divide original images + corresponding labelled text files into 3 folders (train, val, test) using Python's `random`, `glob`, and `shutil` libraries
  
Other:
  * Finished 3 required trainings

</details>



<br/>


<details>
<summary> June 13, 2023 </summary>

### June 13, 2023
  
  **Goal:** Start creating YoloV7 model trained on custom rideshare vehicle data
  
 Uploaded data + Yolov7 folder to Google drive, created python script to train model
    
  * Upload divided data into Google Drive
  * Used basic Yolov7 tutorial to train model on custom data (75 epochs - took about 5-6 hrs), used custom `weight.py`
  * Tested model with 15% confidence level on test images - classified 0 images as rideshare vehicles :'(
  * Read guides explaining how to train model with transfer learning approach, next goal is to use pretrained model and train with additional custom data for higher accuracy
  
Other:
  * Finished 2 required trainings

</details>


<br/>


<details>
<summary> June 14, 2023 </summary>

### June 14, 2023
  
  **Goal:** Create transfer-learned model using PyTorch pretrained weights + CNN
  
 Uploaded node data, used transfer-learning approach to improve accuracy of rideshare sticker recognition, analyzed loss-charts + accuracy, tested model with images
    
  * Upload W07B randomly divided data into Google Drive (saved into 3 folders, each with 2 class - Normal and Rideshare)
  * Used Pytorch convolutional neural network model and pretrained weights (`IMAGENET1K_V1`) to reset and train last layer of model with custom data (approx. 2000 images)
  * Final accuracy of 91.0526%, trained twice with 25 epochs each (cnn model also finetuned with custom data)
  * Created epochs vs. training loss chart - training loss decreased from 0.6976 to 0.3578 throughout first 25 epochs
  
Other:
  * Finished several required trainings

</details>



<br/>



<details>
<summary> June 15, 2023 </summary>

### June 15, 2023
  
  **Goal:** Create new training transfer-learned model with `ResNet18` pretrained weights for **entire** Chicago dataset
  
 Created training transfer learned model and developed Validation and Training Accuracy and Loss Charts
    
  * Randomly divided nodes W07B, W026, and W02C data into training and validation folders
  * Uploaded node W07B, W026, and W02C folders (zip files) to Colab - changed python script to account for entire dataset
  * Trained transfer-learned model with `Resnet18 IMAGENET1K_V1` preweights - 2 stages
    * Stage 1: Loading pretrained model, optimizing all parameters with custom data - finetuning Convolutional Neural network
    * Stage 2: Loading pretrained model, optimizing only final few layers with custom data
  * Made updates to training python script and included epoch accuracy and loss data feature to store data values
  * Created training + validation loss and accuracy stage 1 charts (see `Plots` folder)
  
Other:
  * Finished 2 required trainings

</details>



<br/>



<details>
<summary> June 16, 2023 </summary>

### June 16, 2023
  
  **Goal:** Create new training transfer-learned model with `ResNet50 IMAGENET1K_V2`  pretrained weights for **entire** Chicago dataset
  
 Created ResNet50 transfer learned model and developed Validation and Training Accuracy and Loss Charts
    
  * Does ResNet50 Model perform better than ResNet18?
    * ResNet50: Bottleneck Residual Building Block = faster training, higher accuracy, updated model with more training data
  * Final accuracy of `0.936968` for Stage 1 (optimizing all model parameters)   
  * Created training + validation loss and accuracy stage 1 charts (see `Plots` folder, image 2)
  
Other:
  * Finished 3 required trainings (only 5 left!)
  * GPU in Colab ran out :(

</details>



<br/>



<details>
<summary> June 19, 2023 </summary>

### June 19, 2023
  
  **Goal:** Create new ml model using finetuning approach with YoloV7 pretrained model
  
 Finetuned Yolov7 model (previously trained on COCO dataset)
    
  * Uploaded all images into alternative drive account (to access additional GPU without waiting
  * Created new image recognition model using pretrained YoloV7 model, and finetuning/custom training final layers with custom dataset
    * 100 epochs (`results.txt` file generated after) 
  * Created extra testing dataset using W07A node images
  
Other:
  * Finished all required trainings (only SEC160 left)
  * GPU in Colab ran out :(

</details>



<br/>



<details>
<summary> June 20, 2023 </summary>

### June 20, 2023
  
  **Goal:** Create new ML model using finetuning approach with YoloV7 pretrained model
  
 Finetuned using training stages + create new **YoloV8** model
    
  * Previous model not able to finish training due to GPU limits (only trained about 40 epochs)
  * New approach: Train model in stages of 10 epochs at once
    * Used pre-trained COCO dataset Yolov7 weight for stage1, for additional stages use previous 10 epoch `best.pt` weight generated from model
  * Only 4 stages (total 40 epochs) ran before GPU allocated in Colab ran out
  * Generated new YoloV8 model trained on custom data using 30 epochs (may need to train for longer) and with `yolov8n.pt` weights
    * Precision: `0.804`, Recall: `0.803 ` 
    * See `Plots` and `Yolov8_Model` file for precision-recall chart and test predictions
  * YoloV8 model detects stickers in large image quadrants (not able to detect rideshare stickers given full image)
  
Other:
  * Yolov8 custom-trained model may be a promising approach, as Recall & Precision values are ~80% and predictions are much better than YoloV7 with just 30 epochs!!
  * Talked to Sean about Jupyter offerings in ALCF without GPU restrictions


</details>




