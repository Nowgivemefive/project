import socket
import threading
import struct
import pickle


import os
'''
读取当前文件夹下的.mp3 ,存到songlist文件中
'''
song_list = []
for root, dirs, files in os.walk('music', topdown=False):
    for song in files:
        if song.split('.')[1] == 'mp3':
            song_list.append(song)
            
r_song_list = []
for index in range(0, len(song_list)):
    temp = [song_list[index], index]
    r_song_list.append(temp)

f = open('songlist.txt','w')
for song in r_song_list:
    f.write('{0}\t{1}\n'.format(song[1],song[0]))
f.close()
'''
将playlists文件夹下的playlist.txt文件信息读取到list
'''

res_list = []
f = open('playlists/playlists.txt','r')
for line in f:
    res_list.append(line.strip('\n').split('\t'))
playlists_list = res_list
'''
将读取到的.mp3列表 存到songList ，在之后传给__init__构造器
'''
songList = r_song_list

class Command:
    command = ""
    payload = ""

# This is my thread class.  It inherits from threading.Thread....

class SocketThread(threading.Thread):
    def __init__(self, socketInstance, songList, playlists_list):
        threading.Thread.__init__(self)
        self.mySocket = socketInstance
        self.songList = songList
        self.playlists_list = playlists_list
        
    # this is what gets run when you call start()
    def run(self):
        try:
            while (True):
                print("Reading initial length")
                a = self.mySocket.recv(4)
                print("Wanted 4 bytes got " + str(len(a)) + " bytes")
                messageLength = struct.unpack('i', a)[0]
                
                print("Message Length: ", messageLength)
                data = self.mySocket.recv(messageLength)
                
                try:
                    newCommand = pickle.loads(data)
                except Exception as e:
                    print(e)
                print("Command is: ", newCommand.command)

                if newCommand.command == "GetSong":
                    print("Sending song")
                    replyCommand = Command()            # Make a new command
                    replyCommand.command = "Song Reply" # Set the command type to Song Reply
                    f = open(newCommand.payload, 'rb')  # Open the file, read it in, and use it as the payload
                    print("Sending file: ", newCommand.payload)
                    replyCommand.payload = f.read()
                    f.close()
                elif newCommand.command == "GetSongList":
                    print("Sending song list")
                    replyCommand = Command()
                    replyCommand.command = "SongList"
                    replyCommand.payload = self.songList
                elif "ADDSONG" in newCommand.command and "ADDSONGTOLIST" not in newCommand.command:
                    '''
                    接受上载歌曲
                    '''
                    song_file_name = newCommand.command.split(' ')[1]
                    song_id = len(self.songList)
                    song_file_name = "{0}.mp3".format(song_id)
                    self.songList.append([song_file_name,song_id])
                    f = open('music/{0}'.format(song_file_name),'wb')
                    f.write(newCommand.payload)
                    f.close()
                    print('ADDSONG success')
                    replyCommand = Command()
                    replyCommand.command = "SONGADDED {0}".format(song_id)
                    replyCommand.payload = "empty"
                elif "CREATEPLAYLIST" in newCommand.command:
                    '''
                    question 创建一个播放列表 返回播放列表的ID
                    '''
                    play_list_name = newCommand.command.split(' ')[1]
                    play_list_id = len(self.playlists_list)
                    
                    f = open("playlists/{0}_{1}.txt".format(play_list_id, play_list_name),'w')
                    f.write(play_list_name+'\n')
                    for song in self.songList:
                        f.write('{0}\t{1}\n'.format(song[1],song[0]))
                    f.close()
                    self.playlists_list.append([play_list_id,"{0}_{1}.txt".format(play_list_id, play_list_name)])
                    f = open('playlists/playlists.txt','w')
                    for playlist in self.playlists_list:
                        f.write("{0}\t{1}\n".format(playlist[0],playlist[1]))
                    f.close()
                    replyCommand = Command()
                    replyCommand.command = "PLAYLISTCREATED {0}".format(play_list_id)
                    replyCommand.payload = "empty"
                elif newCommand.command == "GETALLPLAYLISTS":
                    '''
                    ques 3 以列表的形式返回playlists中的信息
                    '''
                    replyCommand = Command()
                    replyCommand.command = "ALLPLAYLISTSLIST"
                    replyCommand.payload = self.playlists_list
                elif "GETPLAYLIST" in newCommand.command:
                    '''
                    查找对应playlist_id的信息，返回一个list
                    '''
                    play_list_id = newCommand.command.split(' ')[1]
                    playlist_name = ''
                    for playlist in self.playlists_list:
                        if play_list_id == playlist[0]:
                            playlist_name = playlist[1]
                            break
                    f = open("playlists/{0}".format(playlist_name),'r')
                    f.readline()
                    playlist = []
                    for song in f:
                        playlist.append(song.strip('\n').split('\t'))
                    f.close()
                    replyCommand = Command()
                    replyCommand.command = "PLAYLISTLIST"
                    replyCommand.payload = playlist
                elif "GETSONG" in newCommand.command:
                    '''
                    ques5 通过歌曲ID 下载歌曲 返回歌曲的二进制
                    '''
                    song_id = newCommand.command.split(' ')[1]
                    song_id = int(song_id)
                    song_name = ''
                    for song in self.songList:
                        if song[1] == song_id:
                            song_name = song[0]
                            break
                    f = open('music/{0}'.format(song_name),'rb')
                    replyCommand = Command()
                    replyCommand.command = "SONGDATA"
                    replyCommand.payload = f.read()
                    f.close()
                elif "ADDSONGTOLIST" in newCommand.command:
                    '''
                    在播放列表中添加歌曲
                    '''
                    song_id = newCommand.command.split(' ')[1]
                    playlist_id = newCommand.command.split(' ')[2]
                    playlist_name = ""
                    for playlist in self.playlists_list:
                        if playlist[0] == playlist_id:
                            playlist_name = playlist[1]
                            break
                    f = open('playlists/{0}'.format(playlist_name),'r')
                    filename = f.readline()
                    playlist = []
                    for song in f:
                        playlist.append(song.strip('\n').split('\t'))
                    f.close()
                    song_name = ""
                    for song in self.songList:
                        if song[1] == int(song_id):
                            song_name = song[0]
                            break
                    playlist.append([song_id, song_name])
                    f = open('playlists/{0}'.format(playlist_name),'w')
                    f.write(filename)
                    for song in playlist:
                        f.write("{0}\t{1}\n".format(song[0],song[1]))
                    f.close()
                    replyCommand = Command()
                    replyCommand.command = "SONGADDED"
                    replyCommand.payload = None
                elif "REMOVESONGFROMLIST" in newCommand.command:
                    '''
                    在播放列表中删除歌曲
                    '''
                    song_id = newCommand.command.split(' ')[1]
                    playlist_id = newCommand.command.split(' ')[2]
                    playlist_name = ""
                    for playlist in self.playlists_list:
                        if playlist[0] == playlist_id:
                            playlist_name = playlist[1]
                            break
                    f = open('playlists/{0}'.format(playlist_name),'r')
                    filename = f.readline()
                    playlist = []
                    for song in f:
                        playlist.append(song.strip('\n').split('\t'))
                    f.close()
                    for song in playlist:
                        if song[0] == song_id:
                            playlist.remove(song)
                            break
                    f = open('playlists/{0}'.format(playlist_name),'w')
                    f.write(filename)
                    for song in playlist:
                        f.write("{0}\t{1}\n".format(song[0],song[1]))
                    f.close()
                    replyCommand = Command()
                    replyCommand.command = "SONGREMOVED"
                    replyCommand.payload = None    
                else:
                    print("Unknown Command")
                    raise Exception("Unknown Command")
                
                if replyCommand.command != '':
                    packedData = pickle.dumps(replyCommand)               # Serialize the class to a binary array
                    self.mySocket.sendall(struct.pack("i", len(packedData))) # Length of the message is just the length of the array
                    self.mySocket.sendall(packedData)
        except Exception as e:
            print("Closing socket")
            print(e)
            self.mySocket.close()

#start our main....

host = "localhost"
port = 4567

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind((host,port))
serverSocket.listen(1)

print("Listening...")

while True:
    (clientSocket, address) = serverSocket.accept()
    print("Got incoming connection")
    newThread = SocketThread(clientSocket, songList, playlists_list)        # make a new instance of our thread class to handle requests
    newThread.start()                             # start the thread running....
    

    
