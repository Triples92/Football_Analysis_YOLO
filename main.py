from utils import read_video, save_video
from trackers import Tracker
from team_assigner import TeamAssigner
from player_ball_assigner import PlayerBallAssigner
import numpy as np
import cv2

def main():
    #read video
    video_frames = read_video('input_videos/08fd33_4.mp4')
    
  

    tracker = Tracker('training/models/best.pt')
    tracks = tracker.get_object_tracks(video_frames,read_from_stub=True,stub_path='stubs/track_stubs.pkl')
    
    #interpolate ball positions

    tracks['ball']= tracker.interpulate_ball_position(tracks['ball'])

    #assign player teams

    team_assigner = TeamAssigner()

    team_assigner.assign_team_colour(video_frames[0],tracks['players'][0]) #will get colours from players in the first frame to assign to teams

    for frame_number,player_track in enumerate(tracks['players']):
        for player_id, track in player_track.items():
            team = team_assigner.get_player_team(video_frames[frame_number],
                                                 track['bbox'],
                                                 player_id)
            tracks['players'][frame_number][player_id]['team'] = team 
            tracks['players'][frame_number][player_id]['team_colour'] = team_assigner.team_colours[team]

    #Assign Ball Aquisition 
    player_assigner = PlayerBallAssigner()
    team_ball_control = []

    for frame_num, player_track in enumerate(tracks['players']):
        ball_bbox = tracks['ball'][frame_num][1]['bbox']
        assigned_player = player_assigner.assign_ball_to_player(player_track,ball_bbox)

        if assigned_player != -1:
            tracks['players'][frame_num][assigned_player]['has_ball'] = True
            team_ball_control.append(tracks['players'][frame_num][assigned_player]['team'])
      
        else:
            team_ball_control.append(team_ball_control[-1])
    
    team_ball_control = np.array(team_ball_control)

    #draw output
    ## draw object tracks
    output_video_frames = tracker.draw_annotations(video_frames,tracks,team_ball_control)

      #save video
    save_video(output_video_frames, 'output_videos/output_video.mp4')


if __name__ == '__main__':
    main()

