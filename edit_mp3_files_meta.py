import os
from mutagen.mp3 import MP3
import mutagen.id3
#import lib for managing user input and help menu
import argparse

# function defining the help menu
#get user args
def get_args():
    parser = argparse.ArgumentParser(description='populate mp3 meta data for album')
    #required argument directory, default pwd
    parser.add_argument('-d', '--directory', help='directory of mp3 files. default pwd', default='pwd')
    #change artist attribute
    parser.add_argument('-ar', '--artist', help='artist name, "Fisrt Last"', default=None)
    #change album name attribute
    parser.add_argument('-al', '--album', help='album name', default=None)
    #change publisher attribute
    parser.add_argument('-p', '--publisher', help='publisher name', default=None)
    #set song names bool -- uses file names
    parser.add_argument('-s', '--song', help='set song names from file name', action='store_true')
    #add album art
    parser.add_argument('-art', '--art', help='add album art, add pic to directory and rename pic.jpg', action='store_true')
    #year
    parser.add_argument('-y', '--year', help='year', default=None)
    return parser.parse_args()

# function to get a list of mp3 based on get_args --directory
def get_mp3_files(directory):
    #check directory is pwd or path
    if directory == 'pwd':
        directory = os.getcwd()
    #does directory exist
    if not os.path.exists(directory):
        print(f'{directory} does not exist')
        exit(1)

    #get list of files in directory
    files = os.listdir(directory)
    #filter mp3 files
    mp3_files = [file for file in files if file.endswith('.mp3')]
    #return list of mp3 files
    return mp3_files

#  function that takes the file name and returns the name minus the extension
def remove_extension(file):
    return os.path.splitext(file)[0]



#function to loop through mp3
def set_mp3_meta(mp3_files, arg):
    #for each mp3 file
    for mp3_file in mp3_files: 
        #open the mp3 file
        mp3 = MP3(mp3_file)
        #get the song name
        song_name = remove_extension(mp3_file)
        #call function that sets the meta data based on arg
        
        
        set_data(mp3, song_name, arg)

#convert string with under scores to spaces
def convert_to_spaces(string):
    return string.replace('_', ' ')

#function set_mp3_meta
def set_data(mp3, song_name, args,):
    #get the param
        if args.song:
            mp3["TIT2"] = mutagen.id3.TIT2(encoding=3, text=[song_name])
        if args.album:
            mp3["TALB"] = mutagen.id3.TALB(encoding=3, text=[args.album])
        if args.publisher:
            mp3["TPUB"] = mutagen.id3.TPUB(encoding=3, text=[args.publisher])
        if args.artist:
            mp3["TPE1"] = mutagen.id3.TPE1(encoding=3, text=[args.artist])
            mp3["TPE2"] = mutagen.id3.TPE2(encoding=3, text=[args.artist])
        if args.art:
            mp3["APIC"] = mutagen.id3.APIC(encoding=3, mime='image/jpeg', type=3, desc=u'Cover', data=open('pic.jpg', 'rb').read())
        if args.year:
            mp3["TDRC"] = mutagen.id3.TDRC(encoding=3, text=[args.year])
        
        mp3.save()




#main
def main():
    #get user args
    args = get_args()
    #get list of mp3 files
    mp3_files = get_mp3_files(args.directory)
    #get list of arguments passed
    set_mp3_meta(mp3_files, args)

if __name__ == '__main__':
    main()
