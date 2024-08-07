import cv2


def read_video(video_path):
    cap= cv2.VideoCapture(video_path)
    frames= []
    while True:
        #loops over video frame by frame
        ret, frame = cap.read()
        if not ret:
        #ret shows flag whether there is a frame or not
        #if ret is false, then no frame is present and loop wll break
            break
        frames.append(frame)
    return frames
    

def save_video(output_video_frames,output_video_path):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #output video frames[0] includes the video width and hieght
    out = cv2.VideoWriter(output_video_path,fourcc, 24, (output_video_frames[0].shape[1],output_video_frames[0].shape[0]))
    for frame in output_video_frames:
        out.write(frame)
    out.release()