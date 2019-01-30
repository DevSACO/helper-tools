# Massive helper tools
Bash tools for manage massive files, all main dir an subdirectories where executes this tools.

* Features included:
 -- Rename files using [number]_[random_string].[ext]
 -- Move all files into full deep subtree to a new dir
 -- Remux audio/video files into full deep subtree to a new dir using original subtree
    (av_dir/av_file.ext) -> (new_dir/av_dir/av_file.ext)
 -- Remux with scale, split and normalize(Beta) options
 -- Extracting compressed files into (Data) dir, use passwords stored in (.passwd) txt file
 -- Extractor helper requires 7z (at the moment the best), and WinRAR (optional if wine are installed), in some cases.

# Installing
```
git clone https://github.com/DevSACO/helper-tools.git
sudo cp -R helper-tools/randx.sh /usr/bin/randx; sudo chmod +x randx.sh
sudo cp -R helper-tools/remuxer.sh /usr/bin/remuxer; sudo chmod +x remuxer.sh
```

# Removing
```
```
# Examples:

./remuxer.sh or script_name if are installed in your root binary executables (/usr/bin|/usr/xbin) \
[demuxer script] -g list n	# Get all multimedia links in lst-l.txt \
[demuxer script] -c v n		# Convert recursively videos in subdirectories to mkv format \
[demuxer script] -c v d		# Convert recursively videos in subdirectories to mkv format (codec av copy)\
[demuxer script] -c v s m	# Convert recursively videos in subdirectories to mkv format and resize to 720p and clear metadata\
[demuxer script] -c v m s	# Convert recursively videos in subdirectories to mkv format and clear metadata and resize to 720p\
[demuxer script] -c vd n	# Rip dvd to a single mkv format (Beta) \
[demuxer script] -c a n		# Convert recursively videos in subdirectories to m4a format \
[demuxer script] -c a s		# Convert recursively videos in subdirectories to m4a format and truncate silence \
[demuxer script] -c a c		# Convert recursively videos in subdirectories to m4a format and convert 5.1 to stereo \
[demuxer script] -c a s s	# Convert recursively videos in subdirectories to m4a format and truncate silence and split \
[demuxer script] -c a c s	# Convert recursively videos in subdirectories to m4a format and convert 5.1 to stereo and split \
 \
./randx.sh or script_name if are installed in your root binary executables (/usr/bin|/usr/xbin) \
[renamer script] -n e		# Renames recursively files in subdirectories (using original extension) \
[renamer script] -n c		# Renames recursively files in subdirectories (using generic extension .gextd, pretends change to a random extension in future) \
[renamer script] -e   #Extract recursively 7z, zip, rar, etc. with password (stored password list in a .passwd file, creates where u run this script) (Debug for massive splitted files) \
 \
Remember, some functions maybe don't work correctly or requires move first the origin media to another directory.
