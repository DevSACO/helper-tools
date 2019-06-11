# Massive helper tools
Bash tools for manage massive files, all main dir an subdirectories where executes this tools.

* Features included:
 - Rename files using [number]_[random_string].[ext]
 - Move all files into full deep subtree to a new dir
 - Remux audio/video files into full deep subtree to a new dir using original subtree
    (av_dir/av_file.ext) -> (new_dir/av_dir/av_file.ext)
 - Remux with scale, split and normalize(Beta) options
 - Extracting compressed files into (Data) dir, use passwords stored in (.passwd) txt file
 - Extractor helper requires 7z (at the moment the best), and WinRAR (optional if wine are installed), in some cases.

## Installing
```
git clone https://github.com/DevSACO/helper-tools.git
sudo cp -R helper-tools/randx.sh /usr/bin/randx; sudo chmod +x /usr/bin/randx
sudo cp -R helper-tools/remuxer.sh /usr/bin/remuxer; sudo chmod +x /usr/bin/remuxer
```

## Removing
```
sudo rm -R /usr/bin/randx /usr/bin/remuxer
```
* Usage: ./remuxer.sh option type mode [] () [language]
  - ***Options***
  ```
    -g		# Get media from filelist, use -g (name) mode [playlist num start]. file is [(name).ext].
    -c		# Convert media files.
  ```
  - ***Type***
  ```
     a	# Converts recusively massive audio/video files in high deep subdir to audio m4a, all audio streams are mapped in out file.
     v	# Converts recusively massive video files in high deep subdir to matroska mkv, all streams are mapped in out file, except side data (in some cases).
  ```
  - ***Mode***
  ```
     * c	# Copy codecs as original in out container
     * n	# If option $5=n try Volume_normalize, else, do nothing.
     * p	# Converts 7.1<= to stereo (Dont see LFE)
     * s	# Truncate silence and converts 7.1<= to stereo (Debug LFE). Changes dB in audio_clean option
     * z	# Scale resolution. Changes into script in -vf scale option. Default 720p
  ```
  - ***Extra options***
  ```
     * s  # Split into (time)s multiple files. Changes into script in segment_seconds option. Default 60s. (Debug, only audio.)
     * [media_type] # Specify mp4 or mkv
  ```
  - ***Beta option***
  ```
     * n  # Volume detects, and try normalize. (Turtle time detection, issue: deppends of the media size)
  ```
  - ***Language options***
  ```
     * (language audio) (language subtitle) # Only if streams have metadata language=und. (Debug)
  ```
## Examples:
```
./remuxer.sh -g [name] h		# Get all multimedia (hd) links in [name].ext or other file text
./remuxer.sh -c v c mkv eng eng		# Convert videos to mkv container and set audio_language/subtitle_language tag to eng
./remuxer.sh -c v c mkv n eng eng	# Convert videos to mkv container, applies volume_normalize and set audio_language/subtitle_language tag to eng
./remuxer.sh -c v z mp4 n jap jap	# Convert videos to mp4 format (720p scaling) and set audio_language/subtitle_language tag to jap
./remuxer.sh -c a s s			# Convert audio to m4a format (transcode 7.1>stereo, truncate silence) and split
./remuxer.sh -c a p eng n		# Convert audio to m4a format (transcode 7.1>stereo), applies volume_normalize and set audio_language tag to eng

./renamer.sh -n e	# Renames files (using original extension)
./renamer.sh -n c	# Renames files (using random extension)
./renamer.sh -e		# Extract recursively 7z, zip, rar, etc. with password (store passwords list in a .passwd file) (Issue for splitted files: 001,002..010, etc.), if exist wine and have winrar installed, in some cases tries extraction with C:\program files\winrar\(un)rar.exe
```
###### Remember, some functions maybe don't work correctly or first move the origin media to another directory.
