# helper-tools
RC bash helper tools

Examples:

./demuxer.sh or ctv if extract in you root binary executables \
[demuxer script] -g l n   #Get all multimedia links in lst-l.txt \
[demuxer script] -c v n   #Convert recursively videos in subdirectories to mkv format \
[demuxer script] -c v d   #Convert recursively videos in subdirectories to mkv format (codec av copy)\
[demuxer script] -c v s m #Convert recursively videos in subdirectories to mkv format and resize to 720p and clear metadata\
[demuxer script] -c v m s #Convert recursively videos in subdirectories to mkv format and clear metadata and resize to 720p\
[demuxer script] -c vd n  #Rip dvd to a single mkv format (Beta) \
[demuxer script] -c a n   #Convert recursively videos in subdirectories to m4a format \
[demuxer script] -c a s   #Convert recursively videos in subdirectories to m4a format and truncate silence \
[demuxer script] -c a c   #Convert recursively videos in subdirectories to m4a format and convert 5.1 to stereo \
[demuxer script] -c a s s #Convert recursively videos in subdirectories to m4a format and truncate silence and split \
[demuxer script] -c a c s #Convert recursively videos in subdirectories to m4a format and convert 5.1 to stereo and split \
 \
./randx.sh or dran if extract in you root binary executables \
[renamer script] -n e   #Renames recursively files in subdirectories (using original extension) \
[renamer script] -n c   #Renames recursively files in subdirectories (using generic extension .gextd, pretends change to a random extension in future) \
[renamer script] -e   #Extract recursively 7z, zip, rar, etc. with password (stored password list in a .passwd file, creates where u run this script) (Debug for massive splitted files) \
 \
Remember, some functions maybe don't work correctly or requires move first the origin media to another directory.
