import cv2
import os
from pytube import YouTube
import numpy as np

def predict_single_action(video_file_path, SEQUENCE_LENGTH, LRCN_model):

  IMAGE_HEIGHT, IMAGE_WIDTH = 64, 64
  CLASSES_LIST = ["WalkingWithDog", "TaiChi", "Swing", "HorseRace"]

  #Initialize the VideoCapture object to read from the video file
  video_reader = cv2.VideoCapture(video_file_path)

  #Get the width and height of the video
  original_video_width = int(video_reader.get(cv2.CAP_PROP_FRAME_WIDTH))
  original_video_height = int(video_reader.get(cv2.CAP_PROP_FRAME_HEIGHT))

  #Declare a list to store video frames we are extracting
  frames_list = []

  #Initialize a variable to store the predicted action being performed in the video
  predicted_class_name = ''

  #Get the number of frames in the video
  video_frames_count = int(video_reader.get(cv2.CAP_PROP_FRAME_COUNT))

  #Calculate the interval after which frames will be added to the list
  skip_frames_window = max(int(video_frames_count/SEQUENCE_LENGTH),1)

  #Iterating the number of times equal to the fixed length of sequence
  for frame_counter in range(SEQUENCE_LENGTH):
    #Set the current frame position of the video
    video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_counter * skip_frames_window)

    #Read a frame
    success, frame = video_reader.read()

    #Check if frame is not read properly then break the loop
    if not success:
      break

    #Resize the frame to fixed Dimensions
    resized_frame = cv2.resize(frame,(IMAGE_HEIGHT,IMAGE_WIDTH))

    #Normalize the resized frame by dividing it with 255. So that each pixel value then lies between 0 and 1
    normalized_frame = resized_frame/255

    #Appending the pre-processed frame into the frames list
    frames_list.append(normalized_frame)

  #Pass the pre=processed frames to the model and get the predicted probabilities
  predicted_labels_probabilities = LRCN_model.predict(np.expand_dims(frames_list, axis = 0))[0]

  #Get the index of class with highest probability
  predicted_label = np.argmax(predicted_labels_probabilities)

  #Get the class name using the retrieved index
  predicted_class_name = CLASSES_LIST[predicted_label]

  #Release the VideoCapture objects
  video_reader.release()

  return {"label_predicted": f'{predicted_class_name}', "confidence": f'{predicted_labels_probabilities[predicted_label]}'}
  

def download_youtube_videos(youtube_video_url, output_directory):

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Create a YouTube object
    yt = YouTube(youtube_video_url)

    # Get the title of the video
    video_title = yt.title

    # Get the highest resolution stream available
    stream = yt.streams.get_highest_resolution()

    # Download the video to the output directory
    output_file_path = stream.download(output_path=output_directory, filename=video_title)

    return video_title

