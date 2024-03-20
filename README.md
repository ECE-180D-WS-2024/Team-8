# Team-8

After your create your environment, make sure your python version is 3.11.0; 
	
	1.conda install python=3.11.0
	2.pip install pygame
	3.conda install numpy matplotlib pandas
	4.conda install -c conda-forge opencv
	5.pip install -U scikit-learn
 	6.pip install paho-mqtt

Please keep updating this python libaries installation list after you finish implementing your features to make sure our ultinate pyfile is runnable as we will integrate all the features to the game at the time

We have decided to add the MQTT class and loop in the player class instead of the game class because player is the one accessing the IMU status. In addition, the MQTT.ino file breaks up statuses from 0-8, where 0 represents idle and 1-8 represents 45 degree increments. The MQTT.ino program requires more tweaking to ensure better detection accuracy. Further plans also include adjusting player and enemy speeds to make the gameplay more enjoyable. 
