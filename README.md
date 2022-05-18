# Plant_Cam
**Course**: CS 490 Spring 2022 University of San Francisco <br />
**Author**: Adon Anglon <aanglon@dons.usfca.edu>, Peter Cuddihy <pmcuddihy@dons.usfca.edu>,<br />
         Alexander Franklin <acfranklin2@dons.usfca.edu>, Yulong Guo <yguo70@dons.usfca.edu><br />
**Instructor**: Professor Doug Halperin <dhalperin@usfca.edu><br />
&emsp;**TA**: Nikhil Bhutani <nbhutani2@dons.usfca.edu><br />
**Sponsors**: Phil Peterson <phpeterson@usfca.edu>, Saranya Radhakrishnan <saranya@unfold.ag>, Ankush Gola <ankush@unfold.ag><br />

## Overview
&emsp;The Plant Cam utilizes a Raspberry Pi and camera that takes a picture of a plant plot and its respective QR code. This QR code holds the plot id of the plant in a database in the Google Cloud Platform service. By sending images of plants to Google Cloud Platform and its services, Plant Cam is able to automatically add the plant’s image to a database and tie it to the correct plot. This project will greatly assist plant breeding scientists to isolate the best plants with prioritized characteristics, with the intent to grow better produce for the commercial market and consumption.

## Code
&emsp;There are two files of code that are used in this project: the local code on the Raspberry Pi and the code in the cloud that does the image processing and adding to the necessary databases. Within 'camera_mqtt.py', the code enables the Raspberry Pi to take photos, encode these images and groups it together as a dictionary with the date and time of the photo taken along with a specified image bucket, and then sends that dictionary within MQTT messages up to the cloud. Then 'image_processing.py' receives those previously sent messages, decodes the data sent through, and first determines whether the image taken contains a QR code and if the QR code is valid. If so, the image is then added to the specified Google Cloud Storage bucket and a URL is generated to allow referencing of that image. From there, the URL is uploaded to the SQL database that holds all of the images associated with a plot id.
