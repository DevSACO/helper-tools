#!/bin/bash
if [ "$#" -ge "2" ]; then
 if [ "$1" == "-g" ]; then
  if [ ! -x /usr/bin/youtube-dl ]; then
   echo "Please install youtube-dl first"; exit 0
  else
   if [ "$2" != "g" ]; then
    if [ "$3" == "c" ]; then UDO="--recode-video mkv --embed-subs"; if ["$4" != "" ]; then SUDA="--sub-lang $4"; else echo "First enter language for embed"; fi; fi
    if [ "$3" == "a" ]; then PRRO='-f bestaudio'; elif [ "$3" == "h" ]; then PRRO='-f bestvideo+bestaudio'; fi; if [ "$5" != "" ]; then LAN="--playlist-start $5"; fi
    if [ "$3" == "sd" ]; then
     echo "Getting VInfo"; youtube-dl -F -a lst-$2.txt >> .dlf 2>&1
     cat .dlf | grep -v 'hardsub' | grep 'x720' | sed 's|  [^\]*||' | sort | sed ':a;N;$!ba;s|\n|/|g' >> .formats; rm -R .dlf > /dev/null 2>&1
     youtube-dl -f $(cat .formats) $PRRO $LAN $UDO $SUDA -a lst-$2.txt
    else youtube-dl $PRRO $LAN $UDO $SUDA -a lst-$2.txt; fi
   fi
  fi
 elif [ "$1" == "-c" ]; then
  if [ ! -x /usr/bin/ffmpeg ]; then echo "Please install ffmpeg first"
  else
   head_args='-hide_banner -threads 0'
   video_scale_z='720'
   segment_seconds='60'
   audio_clean='silenceremove=0:0:0:-1:1:-50dB'
   audio_stereo="pan='stereo|FL<FL+0.5*FC+0.6*BL+0.6*SL|FR<FR+0.5*FC+0.6*BR+0.6*SR'"
   ### Start Audio container definitions
   ### End Audio container definitions
   ### Start Video container definitions
   if [ "$4" == "mp4" ]; then v_filter='mp4'; v_codec='libx264'; e_out='mp4'; audio_codec='-c:a mp3'; fi
   if [ "$4" == "mkv" ]; then v_filter='matroska'; v_codec='hevc'; e_out='mkv'; audio_codec='-c:a ac3'; fi
   if [ "$4" == "mp3" ]; then audio_codec='-c:a mp3'; audio_ext='mp3'; fi
   if [ "$4" == "m4a" ]; then audio_codec='-c:a ac3'; audio_ext='m4a'; fi
   audio_args=" $audio_codec -b:a 320K -ar 48000 "
   video_args=" -f $v_filter -c:v $v_codec -preset ultrafast -b:v 1M -crf 30 -c:s copy"
   ### End Video container definitions
   ### Start Recusively list of all files in all subdirectories
   printf "#/bin/bash\n" > .remuxer; printf "Listing\n"; for M in $(find -type f | sort | grep -v '\.\/Audio' | grep -v '\.\/Data' | grep -v '\.\/Video' | grep -v '\.passwd' | grep -v '\.remuxer' | grep -v '\.reglog' | grep -v "\.ass" | grep -v "\.srt" | sed "s|\./||;s|%|:scp:|;s| |:scs:|g"); do
    ## Start sanitize namefiles
    name_m="$(echo $M | sed "s|:scp:|%|g;s|:scs:| |g")";name_r="$(echo $M | sed "s|:scs:| |g")"; name_f="$(echo $name_r | sed "s|[^\]*/||g")"; name_s="${name_f%.*}"; name_dir="$(dirname "$name_r")"; f_ext="$(echo $name_f | sed "s|$name_s||")"; s_name="$(echo $name_s | sed 's|:scp:|%|g')"
    ## End sanitize namefiles
    ## Start a/v media detection
   if [ ! -z "$(ffprobe -v 0 -show_entries format=duration -of compact "$name_m" | sed 's|[/|=A-Za-z]||g;s|0.040000||')" ]; then
    # Start streams mapping
    video_map="$(ffprobe -v 0 -show_entries stream=index,codec_type -of compact "$name_m" | grep 'video' | sed 's|[^\]*index\=|-map 0:|;s|\|co[^\]*||' | sed ':a;N;$!ba;s|\n|:scs:|g')"
    audio_map="$(ffprobe -v 0 -show_entries stream=index,codec_type -of compact "$name_m" | grep 'audio' | sed 's|[^\]*index\=|-map 0:|;s|\|co[^\]*||' | sed ':a;N;$!ba;s|\n|:scs:|g')"
    subtt_map="$(ffprobe -v 0 -show_entries stream=index,codec_type -of compact "$name_m" | grep 'subtitle' | sed 's|[^\]*index\=|-map 0:|;s|\|co[^\]*||' | sed ':a;N;$!ba;s|\n|:scs:|g')"
    # End streams mapping
    # Start split definitions
    if [ "$4" == "s" ]; then split_args=" -f segment -segment_time $segment_seconds"; splits='A_MTIME'; mkdir -p "Audio/$name_dir/$s_name" "Video/$name_dir/$s_name"; audio_lang="$5"; subtitle_lang="$6"; else audio_lang="$4"; subtitle_lang="$5"; mkdir -p "Audio/$name_dir" "Video/$name_dir"; fi
    # End split definitions
    # Start volume normalization detection
    if [ "$3" == "n" ]; then
    audio_mvd="$(ffprobe -v 0 -show_entries stream=index,codec_type -of compact "$name_m" | grep -m 1 'audio' | sed 's|[^\]*index\=|-map 0:|;s|\|co[^\]*||')"
    volume_dt="$(ffmpeg $head_args -i "$name_m" $audio_mvd -af volumedetect -f null -c:a flac /dev/null 2>&1 | grep 'max_volume' | sed 's| ||g;s|\-||g;s|[^\]*:||')"
    if [ ! -z "$volume_dt" ]; then dlms=','; modvol="volume=$volume_dt"; fi; audio_lang="$6"; subtitle_lang="$7"; else audio_lang="$5"; subtitle_lang="$6"; fi
    # End volume normalization detection
    # Start mode definitions
    if [ "$3" == "c" ]; then video_args=' -c:v copy'; audio_args=' -c:a copy '
    elif [ "$3" == "p" ]; then audio_convert=" -af $audio_stereo$dlms$modvol"
    elif [ "$3" == "s" ]; then audio_convert=" -af $audio_clean,$audio_stereo$dlms$modvol"
    elif [ "$3" == "z" ]; then video_scale=" -vf scale=-1:$video_scale_z"
    elif [ "$3" == "n" ]; then audio_convert=" -af $modvol"; else audio_convert=""; fi
    # End mode definitions
    # Start helper tool | metadata mapping | remuxer end script
    printf "printf '-'; ffmpeg -y $head_args -i :scq:$name_r:scq:"
    if [ "$2" == "a" ]; then
     k=0;l=0;m=0;printf " -map_chapters -1 -map_metadata -1 $audio_map"
     for A in $(ffprobe -v 0 -show_entries stream=codec_type:stream_tags=language -of compact "$name_r" | grep 'audio' | sed "s|[^\]*tag:||;s|und|$audio_lang|"); do
      printf " -metadata:s:a:$((k++)) handler_name='Sound Media Handler' -metadata:s:a:$((l++)) encoder='Sound Media Encoder' -metadata:s:a:$((m++)) $A"
     done
     printf "$split_args$audio_convert$audio_args:scq:Audio/$name_dir/$(if [ "$4" == "s" ]; then echo "$name_s"; fi)$splits$name_s.$audio_ext:scq:"
    elif [ "$2" == "v" ]; then
     if [ -e "$(echo ${name_r%.*}$subtitle_lang.ass)" ]; then printf " -i :scq:$(echo ${name_r%.*}$subtitle_lang.ass):scq:"; fi
     printf " -map_chapters -1 -map_metadata -1 $video_map $audio_map $subtt_map"
     m=0;n=0;o=0;for V in $(ffprobe -v 0 -show_entries stream=codec_type:stream_tags=language -of compact "$name_r" | grep 'video' | sed "s|[^\]*tag:||;s|und|$audio_lang|"); do printf " -metadata:s:v:$((n++)) handler_name='Video Media Handler' -metadata:s:v:$((o++)) encoder='Video Media Encoder' -metadata:s:v:$((p++)) $V"; done
     p=0;q=0;r=0;for A in $(ffprobe -v 0 -show_entries stream=codec_type:stream_tags=language -of compact "$name_r" | grep 'audio' | sed "s|[^\]*tag:||;s|und|$audio_lang|"); do printf " -metadata:s:a:$((p++)) handler_name='Sound Media Handler' -metadata:s:a:$((q++)) encoder='Sound Media Encoder' -metadata:s:a:$((r++)) $A"; done
     s=0;t=0;u=0; if [ -e "$(echo ${name_r%.*}$subtitle_lang.ass)" ]; then printf " -map 1:0 -metadata:s:s:0 handler_name='Subtitle Media Handler' -metadata:s:s:0 encoder='Subtitle Media Encoder' -metadata:s:s:0 language=$subtitle_lang -disposition:s:0 default"; else for S in $(ffprobe -v 0 -show_entries stream=codec_type:stream_tags=language -of compact "$name_r" | grep 'subtitle' | sed "s|[^\]*tag:||;s|und|$subtitle_lang|"); do printf " -metadata:s:s:$((s++)) handler_name='Subtitle Media Handler' -metadata:s:s:$((t++)) encoder='Subtitle Media Encoder' -metadata:s:s:$((u++)) $S"; done; fi
     printf "$split_args$video_scale$audio_convert$video_args$audio_args:scq:Video/$name_dir/$(if [ "$4" == "s" ]; then echo "$name_s"; fi)$splits$name_s.$e_out:scq:"
    fi; printf " > .reglog 2>&1\n"
   fi >> .remuxer; printf '+'; done; printf "\n"
   # End helper tool | metadata mapping | remuxer end script
   ## End a/v media detection
   ### End Recusively list of all files in all subdirectories
   #### Start clear trash, sanitize and start remuxing
   sed -i "s|\"|$(echo '\\''\"')|g;s|\!|$(echo '\"''\\''\!''\"')|g;s|:scq:|\"|g;s|:scs:| |g;s|:scp:|%|g;s|#/|#!/|;s|/\./|/|g;s|program\|||g;s|A_MTIME|/%05d - |;s|-metadata:s:a:[0-9] stream\|||g;s|-metadata:s:s:[0-9] stream\|||g;s|-metadata:s:v:[0-9] stream\|||g;s| codec_type=audio||g;s| codec_type=subtitle||g;s| codec_type=video||g;s|language= |language=eng |;s|\=.esLA|\=spa|g" .remuxer; printf "Remuxing\n"; . .remuxer; rm -R .remuxer
   #### End clear trash, sanitize and start remuxing script
  fi; printf "\n"
 fi
else
 echo "Usage: script option type mode media_type [extra options] [language]
  * Options
   -g			# Get media from filelist, use -g (name) mode [playlist num start]. file is [(name).ext].
   -c			# Convert media files.
  * Type
   a			# Converts recusively massive audio/video files in high deep subdir to audio m4a, all audio streams are mapped in out file.
   v			# Converts recusively massive video files in high deep subdir to matroska mkv, all streams are mapped in out file, except side data (in some cases).   
   + Mode
    c			# Copy codecs as original in out container
    n			# Volume detects, and try normalize. (up/down in some cases work) 
    p			# Converts 7.1<= to stereo (Debug LFE)
    s			# Truncate silence and converts 7.1<= to stereo (Debug LFE). Changes dB in audio_clean option
    z			# Scale resolution. Changes into script in -vf scale option. Default 720p
   + media type		# Specify mp3, m4a, mp4 or mkv
   + Extra options
     s			# Split into (time)s multiple files. Changes into script in segment_seconds option. Default 60s. (Debug, only audio.)
   + Language options
     (language audio) (language subtitle) # Only if streams have metadata language=und. (Debug)"
fi
