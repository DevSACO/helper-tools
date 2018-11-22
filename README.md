# helper-tools
Beta test bash helper tools

Examples:

./demuxer.sh or ctv if extract in you root binary executables \
[demuxer script] -g l n   #Get all multimedia links in lst-l.txt \
[demuxer script] -c v n   #Convert recursively videos in subdirectories to mkv format \
[demuxer script] -c vc n  #Convert designed videos to mkv format \
[demuxer script] -c vd n  #Rip dvd to a single mkv format (Bugs) \
[demuxer script] -c a n   #Convert recursively videos in subdirectories to m4a format \
[demuxer script] -c a s   #Convert recursively videos in subdirectories to m4a format and truncate silence \
[demuxer script] -c a c   #Convert recursively videos in subdirectories to m4a format and convert 5.1 to stereo (Bugs) \
[demuxer script] -c a s s #Convert recursively videos in subdirectories to m4a format and truncate silence and split \
[demuxer script] -c a c s #Convert recursively videos in subdirectories to m4a format and convert 5.1 to stereo and split (Bugs) \
 \
./randx.sh or dran if extract in you root binary executables \
[renamer script] -n e   #Renames recursively files in subdirectories (usin original extension) \
[renamer script] -n c   #Renames recursively files in subdirectories (using generic extension .genm) \
[renamer script] -e   #Extract recursively 7z, zip, rar, etc. with password (stored password list in .passwd file) \
 \
Remember, maybe don't work correctly.
