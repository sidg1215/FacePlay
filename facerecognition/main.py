import cv2
import time
import os
import face_recognition

members = {}
members["Dev"] = "x9zyzskf8w1gnv1gx29rx6ig1"
members["Sid"] = "12169260568"
members["Timmy"] = "2mc1psdu7pcqanh8hlfykox6s"
members["Sahil"] = "4quhvxhrevb3873jm5ncxu2k8"

counter = {}
counter["Dev"] = 0
counter["Sahil"] = 0
counter["Sid"] = 0
counter["Timmy"] = 0




cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0
t0 = time.time()

person = None

while (time.time() - t0)< 5:
    print time.time()-t0
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif int(time.time()-t0) % 2 == 0:
        # SPACE pressed
        img_name = "opencv_frame_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
        images = os.listdir('images')

        # load your image
        image_to_be_matched = face_recognition.load_image_file("opencv_frame_{}.png".format(img_counter-1))

        # encoded the loaded image into a feature vector
        image_to_be_matched_encoded = face_recognition.face_encodings(
            image_to_be_matched)[0]

        # iterate over each image
        for image in images:
            # load the image
            if image <> ".DS_Store":
                current_image = face_recognition.load_image_file("images/" + image)
                # encode the loaded image into a feature vector
                current_image_encoded = face_recognition.face_encodings(current_image)[0]
                # match your image with the image and check if it matches
                result = face_recognition.compare_faces(
                    [image_to_be_matched_encoded], current_image_encoded)
                # check if it was a match
                if result[0] == True:
                    print "Matched: " + image
                    string = ""
                    for i in image:
                        if i == '.':
                            break
                        string = string + i
                    print string
                    counter[string] += 1

                else:
                    print "Not matched: " + image

        maxVal = 0
        for i in counter:
            if counter[i] > maxVal:
                person = i
                maxVal = counter[i]




cam.release()

cv2.destroyAllWindows()

print person
print members[person]

import spotipy
import spotipy.util as util

token = util.prompt_for_user_token(
        username='faceplayadmin',
        scope='playlist-modify-public',
        client_id='16f7f529d0634e6eab61dacb34547e44',
        client_secret='351ef3c86db14e7dabc1b94387078991',
        redirect_uri='http://localhost:8888/callback/')

spotify = spotipy.Spotify(auth=token)

admin_id = '12169260568'
playlist_id = '7iAzX5SjgAWqSzfw0oZqqb'

def get_playlists(user_id):
    playlists = spotify.user_playlists(user_id)
    if 'items' in playlists:
        return [pl['uri'].split(':')[-1] for pl in playlists['items']]
    return []

def get_songs_from_playlist(user_id, playlist_id):
    playlist_tracks = spotify.user_playlist_tracks(user_id, playlist_id, fields='items,uri,name,id,total', market='fr')
    if 'items' in playlist_tracks:
        return [pl['track']['id'] for pl in playlist_tracks['items']]
    return []

def get_all_songs(user_id):
    playlists = get_playlists(user_id)
    songs = []
    count = 0
    for pl in playlists:
        if count >= 2:
            break
        songs += get_songs_from_playlist(user_id, pl)
        count += 1
    return songs

def add_tracks_to_playlist(tracks):
    spotify.trace = False

    if not tracks:
        return None

    for idx in range(0, len(tracks), 100):
        results = spotify.user_playlist_add_tracks(admin_id,
                                              playlist_id,
                                              [tracks] if type(tracks) is not list else tracks[idx:idx+100])
    return (results)

def remove_all_tracks_from_playlist():
    spotify.trace = False
    track_ids = get_songs_from_playlist(admin_id, playlist_id)
    if not track_ids:
        return None
    results = spotify.user_playlist_remove_all_occurrences_of_tracks(admin_id, playlist_id, track_ids)
    return results;


remove_all_tracks_from_playlist()
print add_tracks_to_playlist(get_all_songs(members[person]))
