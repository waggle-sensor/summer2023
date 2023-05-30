# Daily logs

Link to my [meeting notes](https://docs.google.com/document/d/1LRnpN_eE1WZ5-LrI0CYndENyy3PiCGERJvU9nurvOXs/edit?usp=sharing)

## Week 05/29 -- 06/04

### 05/30 Tue

- Transferred local data to ALCF
- Attended the software sustainability seminar
- Data loader and reader look fine but still has issue with multiprocessing, will look into it tomorrow.
- 03/10 - 03/24 data has been downloaded.
- The data format is
  - original unmodified JPG RGB images are in `rgb` directory
  - processed JPG images with only left half (optical images) are in `processed` folder
  - thermal images in `.csv` file with celsius degree per pixel
  - metadata file for everyday and each node are in `sage_meta` folder
  - to check data consistency, I created a txt file for each JPG & thermal image pair and put them in `pairs` folder, and ordered them by SAGE node name.

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

