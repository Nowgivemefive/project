import socket
import struct
import pickle
import threading

host = "localhost"
port = 4567

def getSong(songName, s):
    getCommand = Command()
    getCommand.command = "GetSong"
    getCommand.payload = songName
    packedData = pickle.dumps(getCommand)
    totalLen = len(packedData)
    s.sendall(struct.pack("i", totalLen))
    s.sendall(packedData)

    replyLen = struct.unpack("i", s.recv(4))[0]
    replyData = s.recv(replyLen)
    replyCommand = pickle.loads(replyData)

    f = open("download/"+songName.replace('.mp3','')+"_new.mp3", "wb")
    f.write(replyCommand.payload)
    f.close()

def getSongList(s):
    getCommand = Command()
    getCommand.command = "GetSongList"
    packedData = pickle.dumps(getCommand)
    totalLen = len(packedData)

    s.sendall(struct.pack("i", totalLen))
    s.sendall(packedData)

    replyLen = struct.unpack("i", s.recv(4))[0]
    replyData = s.recv(replyLen)
    replyCommand = pickle.loads(replyData)

    print("Song List is: ", replyCommand.payload)
'''
上载歌曲
'''
def addSong(s, song_file_name):
    addCommand = Command()
    addCommand.command = r"ADDSONG {0}".format(song_file_name)
    f = open("songF.mp3",'rb')
    addCommand.payload = f.read()
    f.close()
    packedData = pickle.dumps(addCommand)           # Serialize the class to a binary array
    s.sendall(struct.pack("i", len(packedData))) # Length of the message is just the length of the array
    s.sendall(packedData)
    
    replyLen = struct.unpack("i", s.recv(4))[0]
    replyData = s.recv(replyLen)
    replyCommand = pickle.loads(replyData)
'''
创建播放列表  返回播放列表ID test access
'''
def create_playlist(s, play_list_name):
    createConmmand = Command()
    createConmmand.command = r"CREATEPLAYLIST {0}".format(play_list_name)
    createConmmand.payload = None
    packedData = pickle.dumps(createConmmand)           # Serialize the class to a binary array
    s.sendall(struct.pack("i", len(packedData))) # Length of the message is just the length of the array
    s.sendall(packedData)
    
    replyLen = struct.unpack("i", s.recv(4))[0]
    replyData = s.recv(replyLen)
    replyCommand = pickle.loads(replyData)
    
    print("play list id:{0}".format(replyCommand.command.split(' ')[1]))

'''
下载歌曲通过歌曲ID test access
'''    
def download_song_by_id(s, song_id):
    getConmmand = Command()
    getConmmand.command = r"GETSONG {0}".format(song_id)
    getConmmand.payload = None
    packedData = pickle.dumps(getConmmand)           # Serialize the class to a binary array
    s.sendall(struct.pack("i", len(packedData))) # Length of the message is just the length of the array
    s.sendall(packedData)
    
    replyLen = struct.unpack("i", s.recv(4))[0]
    replyData = s.recv(replyLen)
    replyCommand = pickle.loads(replyData)
    
    f = open("download/music/{0}_new.mp3".format(song_id), "wb")
    f.write(replyCommand.payload)
    f.close()

'''
下载可用播放列表 返回的是playlists.txt文件中的信息，
格式为列表 比如[[1, 1_happy.txt][2,2_sad.txt]] test access
'''
def download_playlists(s):
    createConmmand = Command()
    createConmmand.command = "GETALLPLAYLISTS"
    createConmmand.payload = None
    packedData = pickle.dumps(createConmmand)           # Serialize the class to a binary array
    s.sendall(struct.pack("i", len(packedData))) # Length of the message is just the length of the array
    s.sendall(packedData)
    
    replyLen = struct.unpack("i", s.recv(4))[0]
    replyData = s.recv(replyLen)
    replyCommand = pickle.loads(replyData)
    
    print("playlists:{0}".format(replyCommand.payload))
'''
下载一个播放列表 ，返回的是list格式的playlist文件中的歌曲信息
'''
def download_playlist(s, playlist_id):
    getConmmand = Command()
    getConmmand.command = r"GETPLAYLIST {0}".format(playlist_id)
    getConmmand.payload = None
    packedData = pickle.dumps(getConmmand)           # Serialize the class to a binary array
    s.sendall(struct.pack("i", len(packedData))) # Length of the message is just the length of the array
    s.sendall(packedData)
    
    replyLen = struct.unpack("i", s.recv(4))[0]
    replyData = s.recv(replyLen)
    replyCommand = pickle.loads(replyData)
    print("song list:{0}".format(replyCommand.payload))
'''
从 playlist 中根据歌曲ID 删除歌曲
method == add or method == remove
'''
def add_remove_song(s, method, song_id, playlist_id):
    if method == 'add':
        getConmmand = Command()
        getConmmand.command = r"ADDSONGTOLIST {0} {1}".format(song_id, playlist_id)
        getConmmand.payload = None
    elif method == 'remove':
        getConmmand = Command()
        getConmmand.command = r"REMOVESONGFROMLIST {0} {1}".format(song_id, playlist_id)
        getConmmand.payload = None
    packedData = pickle.dumps(getConmmand)           # Serialize the class to a binary array
    s.sendall(struct.pack("i", len(packedData))) # Length of the message is just the length of the array
    s.sendall(packedData)
    
    replyLen = struct.unpack("i", s.recv(4))[0]
    replyData = s.recv(replyLen)
    replyCommand = pickle.loads(replyData)
    print("{0}".format(replyCommand.command))
        
class ClientThread(threading.Thread):
    # you need to override the constructor, but make sure to call the base constructor
    def __init__(self, songName):
        threading.Thread.__init__(self)  # make sure you do this or it won't work...
        self.songName = songName
        
    # this is what gets run when you call start()
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        '''
        获取歌曲列表， 歌曲列表是music文件夹下的.mp3文件
        '''
        getSongList(s)
        '''
        下载 songName对应的.mp3文件，下载到download/music文件夹下 你输入的参数要确保这个song是存在于music中的
        '''
        #getSong(self.songName, s)
        '''
        上传一首歌到music文件夹下，你要确保上传的这首歌在对应路径下是存在的，不然你上传空气？？？,上传的song名字是song_id.mp3
        '''
        #song_file_name = r"songF.mp3"
        #addSong(s, song_file_name)
        '''
        创建一个playlist
        '''
        #create_playlist(s, "five")
        '''
        返回playlist的列表，就是playlists.txt文件中的内容
        '''
        #download_playlists(s)
        '''
        下载歌曲通过 song id
        '''
        #download_song_by_id(s, 3)
        '''
        返回playlist内容，通过playlist—id
        '''
        #download_playlist(s, 0)
        '''
        添加song_id playlist_id
        '''
        #add_remove_song(s, "remove", 1, 0)
        '''
        删除song_id playlist_id
        '''
        #add_remove_song(s, "add", 1, 0)
        s.close()

class Command:
    command = ""
    payload = ""

client1 = ClientThread("music/songD.mp3")
client1.start()








        

