# Daily logs

Link to my [meeting notes](https://docs.google.com/document/d/1LRnpN_eE1WZ5-LrI0CYndENyy3PiCGERJvU9nurvOXs/edit?usp=sharing)

## Week 06/05 -- 06/11

### 06/06 Tue

- Modified `DataLoader` to fit the containerized training environment,
as there are volume binding that changed the original file path
- Tested the containerized training environment. This should conclude
the development for VICReg preprocessing and training, now move to change
the model
- Started to train VICReg with ResNet-50 on `full-node` queue
- Challenged by the batch system on ThetaGPU system, `cobalt` is an imposter
batch system using the "same" syntax as the more popular `PBS` batch job
management system.

### 06/05 Mon

- Truncated the rgb image to similar FoV as the thermal camera and downsampled
the image to reduce its size.
- Tested the training on both single-gpu and single-node with 8 gpus
- Maximum batch-size for 8 gpu on  the `full-node` queue is 128
- Wrote `.def` to create singularity image for training
- Can use conda to setup the environment as well, need to decide later.

## Week 05/29 -- 06/04

### 06/02 Fri

- Attended DSL seminar for a review and discussion of recent update on Scientific Machine Learning.
Unsupervised LG-Net might be interesting to consider for solving well-posed PDEs
- Attempted to train the modified VICReg using a single GPU but have to modify the batch size. This 
likely would yield a meaningless results as the batch size is too small (4) to fit into single GPU.
- Discussed with Dario and found out the training was too slow and not useful as aforementioned.
- After the discussion, there are three things to do:
  1. Parallelize the current single thread VICReg
  2. Increase the batch size. This can be done after parallelization
  3. Download more image data. Now only have 7000 images but would need more.
  images are being downloaded right now to ALCF.

<img src="./plots/training_loss_two_panels.png" alt="isolated" width="800"/>
<img src="./plots/learning_rate.png" alt="isolated" width="400"/>


### 06/01 Thu

- Make the Quad chart!
- Changed the VICReg model to fit two different inputs
  - Two instances of the same architecture (i.e., ResNet) -- done
  - Two different architectures -- TODO
- Need to modify the loss function in order to back-propagate to both branches
- Finished the modification today and successfully ran the code on a single GPU

### 05/31 Wed

- Finished implementing the dataloader for sage images data, now the loader works
- Tested the loading function with a single-gpu and it works without distribution package, i.e., do it sequentially.
- Discussed with Dario about the cloud prediction project, and Dario suggested two frameworks:
  - Two component: Joint embedding architecture (JEA) + single transformer fed with embedding vector from the JEA. JEA for image characterization, while the second transformer is for prediction. See this two papers: [DETR](https://arxiv.org/abs/2005.12872), [I-JEPA](https://arxiv.org/abs/2301.08243)
  - Single component: JEA but with two branches feeding different time of the sky image to let one NN model (current image + time input) match the embedding vector of that of the other NN model with future image.
- TODO: switch out ResNet and make sure the training works with a single gpu before putting the large scale training.
- Will continue to download more SAGE data for training.

### 05/30 Tue

- Transferred local data to ALCF
- Attended the software sustainability seminar
- Data loader and reader look fine but still has issue with multiprocessing, will look into it tomorrow.
- 03/10 - 03/24 data has been downloaded.
- The data format is
  - original unmodified JPG RGB images are in `rgb` directory
  - processed JPG images with only left half (optical images) are in `processed` folder under `rgb` directory
  - thermal images in `.csv` file with celsius degree per pixel are in `thermal` folder
  - metadata files created from querying using `sage_data_client` are in `sage_meta` folder
  - to check data consistency, I created a txt file for each JPG & thermal image pair and put them in `pairs` folder, and put in directories with SAGE node name.

### 05/29 Mon

Memorial day, no work.

## Week 05/22 -- 05/28

### 05/26 Fri

- Finally got access to ALCF!
- Migrated the workflow to ALCF
- Continued to change the input to fit into VICReg framework
- Acquired username and password from Raj to access the private node images

### 05/25 Thu

- Downloaded imaging data based on links in metadata files
- Send Bhupendra a list of URLs to files I cannot download due to a credential issue.
- Tweak the framework to change the input from single input with augmentation to two inputs (optical RGB + thermal IR).
- Still don’t have access to ALCF yet, so will try to use google colab for testing
- The W056 node physical location changed from ANL to San Deigo around 05/20/2023, so there might be some changes in the image quality
- Daytime and night time calculations for each node would need the physical location information to get the timezone. This hasn’t been done yet!

### 05/24 Wed

- Checked the VICReg framework and discussed the detail with Dario
- Automated the data downloading process
- Reformated the downloaded images for training
- Splitted the JPG images to left RGB + right thermal images. (only keep the RGB images)

### 05/23 Tue

- Continued to refine the scope of the project
- Downloaded sage node data but there was an issue with credential to download data
- Inspected the sage node data and developed method to extract specific image
- Getting access to ALCF theta

### 05/22 Mon

- Attended orientation
- Met with Dario and Bhupendra to discuss the project detail
- Discussed the SAGE node data format
  - 4 pointing per column (1, 5, 9,13, …)
  - A total of 32 pointing positions and 8 are pointing sky
  - Client code: https://github.com/RBhupi/sage-data-client
  - Data web: https://portal.sagecontinuum.org/ (use ANL to login)
  - Data model is a CSV file with “celsius” per pixel at each position (read the head to understand that)
  - A sample code to query: ​​https://github.com/RBhupi/Konza_Mobo_Analysis/blob/main/mobo_data_download_nc.py
  - Figure out how many images are available at each position and what’s the production rate for each position
  - Want “thermal.celsius.csv” in file name.
