# Haptic Vest for Indoor Navigation

## Demonstration Video and Final Report

[Watch the video](https://youtu.be/8E0bLfXa-ek)

[Read the Final Report](./KUSRP%20-%20Haptic%20Vest%20for%20Indoor%20Navigation%20-%20Final%20Report.pdf)

## Project Overview

This project focuses on the development of a haptic vest designed to aid individuals in indoor navigation. The vest translates spatial information from the surroundings into tactile feedback, helping the wearer navigate. Using sensors and actuators, the vest provides guidance to avoid obstacles, move through doorways, and reach specific destinations within indoor spaces.

## Team Members

- Ahmet Can Karaaslan
- Can Güray Erkan
- Larissa Malgaz
- Melis Kekeç
- Serap Tuba Kudaloğlu

### Advisors

- Prof. Dr. Çağatay Başdoğan
- Aybars Ağaya
- Emir Bahadır Ünsal

## Key Components

### Image Processing & Artificial Intelligence

We utilized the YOLOv8 library for real-time object detection through a web camera. The YOLOv8 model is known for its efficiency in detecting a wide range of objects. Initially, we integrated the YOLOv8 model with our webcam feed to detect multiple object classes provided by the library. 

#### Key Features:
- Real-time object detection
- Integration with webcam feed
- Performance comparison between YOLOv8 and YOLOv5
- Dynamic tracking of object distribution

### Audio Processing

The processing of audio was a vital part of the project, ensuring interactions between the user and the computer were primarily through an auditory medium. We utilized the Google Speech Recognition API for audio transcription and Google's Text-to-Speech (gTTS) library for generating audible commands.

#### Key Features:
- Accurate audio transcription in multiple languages, including Turkish
- Efficient text-to-speech conversion

### User Interface

We designed a user interface to allow users to start the program, ask questions to the AI, initiate voice commands, and control the vest's vibrations using both voice commands and on-screen arrows. This UI enhances the overall user experience by making interaction with the system intuitive and user-friendly.

### Haptic Communication & WebSockets

We established communication between a computer and the vest using WebSockets. Unique tactile feedback for each directional command was developed, allowing for precise navigation instructions to be delivered through the vest.

#### Key Features:
- Real-time communication via WebSockets
- Custom user interface for controlling the vest
- Automated "Got it!" response for instant message sending

### ArUco Markers & Pathfinding

We utilized 15 ArUco markers placed around the lab to correspond to specific points on a map. Using these markers in conjunction with the A* algorithm, we generated the shortest path from the user's location to their desired object, providing step-by-step navigational commands.

#### Key Features:
- Efficient pathfinding using the A* algorithm
- Real-time updates of user position
- Accurate guidance to target objects

## GitHub Repository

The project's source code and documentation are maintained in a public GitHub repository. We utilized various Git functions and created branches to track and merge our team's work efficiently.

## Conclusion

This project successfully demonstrates the integration of advanced image processing, artificial intelligence, and haptic feedback to aid individuals in indoor navigation. The combination of these technologies creates a robust system that significantly improves the quality of life by enabling safer and more efficient navigation in indoor spaces.

## References

- [Learn OpenCV - YOLOv8](https://learnopencv.com/ultralytics-yolov8/)
- Rachmawati, Dian, and Lysander Gustin. "IOPscience." Journal of Physics: Conference Series, IOP Publishing, 1 June 2020, [IOPscience](https://iopscience.iop.org/article/10.1088/1742-6596/1566/1/012061/meta).

---

*Date: 19 July 2024*

*Koç University Summer Research Program*
