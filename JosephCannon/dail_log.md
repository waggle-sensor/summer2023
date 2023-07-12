# Daily logs

## Week 06/05 -- 06/09

### 06/05 Mon

- Read manual regarding the PTZ capabilities of the XNP-6400RW camera model
- Tested different camera functions to learn their purpose and operation
- Met with Raj and Yungho to go over project details

### 06/09

- Turned in experiential agreement for deliverables
- Finished reading PTZ manual and programming guide
- Met with Raj to further develop the scope of the project


## Week 06/12 -- 06/16

### 06/12

- Attended first student connects meeting over Teams

### 06/15 Thur

- Updated the team on project progress.
- Continued working on the API
- Updated the camera time zones and firmware
- Goals: Find a way to encrypt passwords and implement object detection

## Week 06/19 -- 06/24

### 06/19 Mon

- Continued to refine the scope of the project
- Did more research on argparse and its uses with python APIs
- Attened my student connects meeting. Presented a lightning pitch regarding the summer project
- Met with Yungho to further discuss project details

### 06/20 Tue

- Found a book on python APIs
- Installed postman to help with API development
- Continued implementing argeparse with PTZ api


## Week 07/03 -- 07/08

### 07/03 Mon

- Continued working on the Sunapi README document for Hanwha cameras.

### 07/04 Tue

-Happy Fourth!

### 07/05

- Attended Required UCP Seminar with Robert Boomsba. (9am - 10am)
- Attended required training SEC-160 Practical Preparedness for Workplace Violence. (10am-11am)
- Attended guest speaker Dr. Daniele Lezzi's talk.  (11am-12pm)
- Almost finished with the sunapi_control library. Began sunapi_config library.

### 07/06

- Attended guest speaker Dr. Ermin Wei's talk. (10am-11am)
- Began working on Ubiquiti switch API.
- Researched different methods of API calls, determined between xml and ssh.

### 07/07


## Week 07/10 -- 07/14








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

