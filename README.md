# stern4most

hoe aan de slag met stern4most

##stap 1 
Clone de repository naar je catkin workspace src folder.
```
catkin_ws/src$ git clone https://github.com/LaurensMignolet/stern4most.git . 
```

##stap 2
Ga naar je catkin_ws, source en make de packages
```
catkin_ws/src$ cd ..
catkin_ws$ source devel/setup.bash 
catkin_ws$ catkin_make
```
##stap 3
Start de simulatie. momenteel werkt de battletrack nog niet. 
```
catkin_ws$ roslaunch turtlebot3_racetrack turtlebot3_pxl_race.launch 
```
##stap  4 
Open een nieuwe terminal en start de computer vision
```
user@basesation:~$ rosrun stern4most_vision_11802808 vision_controller.py 
```

##stap 5
Open nog een nieuwe terminal en start de pilot.
De robot zal nog niet beginnen met rijden. Hiervoor is de gui nodig
```
user@basesation:~$ rosrun stern4most_pilot_11802808 pilot.py 
```

##stap 6
Open opnieuw een nieuwe terminal en start de gui. Rij met de robot naar het midden van een rijvak. Dan kan je op start autopilot klikken 
en zal de robot autonoom beginnen te rijden. 
```
user@basesation:~$ rosrun stern4most_dashboard_11802808 gui.py
```
