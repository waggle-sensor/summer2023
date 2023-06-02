# Anagha's Daily Work Blog

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



