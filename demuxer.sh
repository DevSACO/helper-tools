#!/bin/bash
if [ "$#" -ge "3" ]; then
 if [ "$1" == "-g" ]; then
  if [ ! -x /usr/bin/gallery-dl -a ! -x /usr/bin/youtube-dl ]; then
   echo "Please install gallery-dl and youtube-dl first"; exit 0
  else
   if [ "$2" != "g" ]; then
    if [ "$2" == "c" ]; then UDO='--recode-video mkv --embed-subs'; fi
    if [ "$3" == "a" ]; then PRO='-f bestaudio'; elif [ "$3" == "h" ]; then PRO='-f bestvideo+bestaudio'; elif [ "$3" == "n" ]; then PRO='-f mkv/mp4/avi/webm/flv'; fi
    if [ "$4" != "" ]; then LAN="--playlist-start $4"; fi
     youtube-dl $PRO $LAN $UDO -a lst-$2.txt
   else
     gallery-dl --no-part -i data
   fi
  fi
 elif [ "$1" == "-c" ]; then
  if [ ! -x /usr/bin/ffmpeg ]; then
   echo "Please install ffmpeg first"
  else
   # Alternative test options
   # -metadata:s:s:0 title="English" -i "concat:F1|F2|F3..." -preset medium -aspect 16:9 -strict -2 -g 40 -probesize 4G -analyzeduration 3600M
   hfo='-ignore_unknown -hide_banner -threads 0'
   aop='-ar 48000'
   cmav='-c:a ac3 -b:a 320K'
   cmvv='-crf 20 -f matroska -c:v hevc -b:v 10M'
   cmv='-f mp4 -c:v mpeg4 -b:v 10M'
   echo "#!/bin/bash" > .demux
   if [ "$5" != "" ]; then ssl="$5"; fi
   if   [ "$2" == "a" ]; then
    if [ "$3" == "c" ]; then
     ssc="-af 'pan=stereo|FL=FC+0.30*FL+0.30*BL|FR=FC+0.30*FR+0.30*BR'"
    elif [ "$3" == "s" ]; then
     ssc="-af silenceremove=0:0:0:-1:1:-40dB,pan='stereo|FL=FC+0.30*FL+0.30*BL|FR=FC+0.30*FR+0.30*BR'"
    fi; if [ "$4" == "s" ]; then segt='-f segment -segment_time 15'; segf='%04d_'; fi
    for A in $(find -type f | sort | sed -e 's:'\"':'$(echo "\"")$(echo '\\''\"')$(echo "\"")':g' -e 's:'\'':'$(echo "\"")$(echo '\\'"'")$(echo "\"")':g' -e 's: :_space_:g' -e 's:\.\/::g' | grep -v '\.ass' | grep -v '\.demux' | grep -v '\.passwd'); do
     # Set file name, dir and optional extensions.
     mmc="$(echo $A | sed 's:_space_: :g' | sed -e 's|\"||g' -e 's|\\||g' | sed 's:[^\]*/::g')";mmd="$(echo Audio/$A | sed 's:_space_: :g' | sed -e 's|\"||g' -e 's|\\||g' | sed "s:/$mmc::")";mmx="$(echo ${mmc%.*})";mkdir -p "$mmd/$mmx"
     # Recursive search
     for AUDIO in $(ffprobe -v 0 -show_entries stream=index,codec_type:stream_tags=language -of compact "$(echo $A | sed 's:_space_: :g')" | grep 'audio' | sed "s|\|tag:|_space_|;s|[^\]*index=|-map_space_0:|;s|\|codec_type=|_space_-metadata:s:|" | sed "s|audio|a:0|g"); do echo "ffmpeg -hide_banner -threads 0 -i \"$(echo $A | sed 's:_space_: :g')\" $(if [ "$(ffprobe -v 0 -show_entries stream=codec_type -of compact "$(echo $A | sed 's:_space_: :g')" | grep 'video' | sed 's|[^\]*video|vs|')" == "vs" ]; then echo '-vf metadata=mode=delete'; fi) $segt $(echo $AUDIO | sed 's:_space_: :g') $ssc $cmav $aop \"$(echo $mmd/$mmx/$segf$mmx.m4a | sed 's:_space_: :g')\"" | sed 's|  | |g'  >> .demux
    done; done
   elif [ "$2" == "v" ]; then
    x=0; y=0; if [ "$3" == "s" ]; then vsf='-vf scale=-1:480'; else asl="$3"; fi; if [ "$4" == "c" ]; then mmo=",metadata=mode=delete"; else ssl="$4";fi
    for V in $(find -type f | sort | sed -e 's:'\"':'$(echo "\"")$(echo '\\''\"')$(echo "\"")':g' -e 's:'\'':'$(echo "\"")$(echo '\\'"'")$(echo "\"")':g' -e 's: :_spacer_:g' -e 's:\.\/::g' | grep -v '\.ass' | grep -v '\.demux' | grep -v '\.passwd'); do
     # Set file name, dir and optional extensions.
     mmc="$(echo $V | sed 's:_spacer_: :g' | sed -e 's|\"||g' -e 's|\\||g' | sed 's:[^\]*/::g')";mmd="$(echo Video/$V | sed 's:_spacer_: :g' | sed -e 's|\"||g' -e 's|\\||g' | sed "s:/$mmc::")";mmx="$(echo ${mmc%.*})";mkdir -p "$mmd"
     # Recursive search
     for VIDEO in $(ffprobe -v 0 -show_entries stream=index,codec_type:stream_tags=language -of compact "$(echo $V | sed 's:_spacer_: :g')" | sed "s|\|tag:|_spacer_|;s|[^\]*index=|-map_spacer_0:|;s|\|codec_type=|_spacer_-metadata:s:|" | sed "s|\-metadata:s:video[^\]*||;s|audio|a:0|g;s|subtitle|s:0|g" | sed "s|a:0 language=und|a:0 language=$asl|;s|s:0 language=und|s:0 language=$ssl|" | sed ':a;N;$!ba;s|\n|_spacer_|g'); do
     echo "ffmpeg -y $hfo -i \"$(echo $V | sed 's:_spacer_: :g')\" $(if [ -e "$(echo ${V%.*}$ssl.ass | sed 's:_spacer_: :g')" ]; then echo "-i \"$(echo ${V%.*}$ssl.ass | sed 's:_spacer_: :g')\""; fi) $vsf$mmo $(echo $VIDEO | sed 's:_spacer_: :g') $(if [ -e "$(echo ${V%.*}$ssl.ass | sed 's:_spacer_: :g')" ]; then echo '-map 1:0 -metadata:s:s:0 language=spa -disposition:s:0 default'; fi) $cmvv $cmav \"$(echo $mmd/$mmx.mkv | sed 's:_spacer_: :g')\"" | sed 's|  | |g' >> .demux; done; done
   elif [ "$2" == "vd" ]; then
    x=0; vdd=$(echo \'$(pwd)\')
    sudo mkdir -p /media/dvd && sudo mount -o ro /dev/sr0 /media/dvd
    vds=$(ls /media/dvd | grep "[Vv]")
    V=$(ls -1v /media/dvd/$vds | grep -e ".I" -e ".i" | grep -e ".B" -e ".b" | grep -v "VTS_[0-9][0-9]_[0]" | grep -v "vts_[0-9][0-9]_[0]" | sed ':a;N;$!ba;s/\n/|\/media\/dvd\/'$vds'\//g')
    echo "ffmpeg $hfo -i \"concat:/media/dvd/$vds/$V\" $aem -c:a ac3 raw_audio.mpeg
ffmpeg $hfo -i \"concat:/media/dvd/$vds/$V\" $cmvs raw_video.mpeg
ffmpeg $hfo -i raw_audio.mpeg -i raw_video.mpeg $aem $cmv $aop '$((x++)) - $($K_XUDSC).mkv'" >> $vdd/.demux && cd $vdd
    sudo umount /media/dvd
   fi
   . .demux
   rm -R .demux
  fi
 fi
else
 echo "Usage: ctv option type mode [extra options] [language]
  Options
   -g			# Get media filelist, use -g name, filelist is [lst-(name).txt]
   -c			# Convert media
  Type
   a			# Converts massive audio files, all audio streams in file
    Mode
     c			# Converts 5.1 to stereo
     s			# Silence remove and converts 5.1 to stereo
      Extra options
       s		# Split into (time)s multiple files. Changes into script in -segment_time option. Default 60s
       (language)	# Only if streams have metadata language=und  (Debug)

   v			# Converts massive video files, all audio, video and subtitle streams in file
    Mode
     s			# Scale resolution. Changes into script in -vf scale option. Default 720p
      Extra options
       s		# Split into (time)s multiple files. Changes into script in -segment_time option. Default 60s
        c		# Clear metadata in video stream. (in some converted files maybe don't work/needed)
       (language)	# Only if streams have metadata language=und  (Debug)

   vd			# RIP dvd's (bugs)
"
fi
