from ultralytics import YOLO

model = YOLO('training/models/best.pt')

results= model('input_videos/08fd33_4.mp4',save=True)

