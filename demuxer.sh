#!/bin/bash
## Check Zero args
if [ "$#" -ge "3" ]; then
 if [ "$1" == "-g" ]; then
  if [ ! -x /usr/bin/gallery-dl -a ! -x /usr/bin/youtube-dl ]; then
   echo "Please install gallery-dl and youtube-dl first"
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
   if   [ "$#" == "4" ]; then
    ivf="-i $4"
    cns=1
   elif [ "$#" == "5" ]; then
    ivf="-i $4 -i $5"
    cns=2
   elif [ "$#" == "6" ]; then
    ivf="-i $4 -i $5 -i $6"
    cns=3
   elif [ "$#" == "7" ]; then
    ivf="-i $4 -i $5 -i $6 -i $7"
    cns=4
   elif [ "$#" == "8" ]; then
    ivf="-i $4 -i $5 -i $6 -i $7 -i $8"
    cns=5
   elif [ "$#" == "9" ]; then
    ivf="-i $4 -i $5 -i $6 -i $7 -i $8 -i $9"
    cns=6
   fi
   if   [ "$3" == "a" ]; then
    echo "Using advanced mapping for streams"
    aem="-filter_complex '[0:0] [0:1] concat=n=$cns:v=1:a=1 [v] [a]' -map [v] -map [a]"
   elif [ "$3" == "c" ]; then
    echo "Setting complex mapping for streams"
    echo "Video"
    read -p "Default [0:0] [0:1]: " MIS
    if [ "$MIS" == "" ]; then MIS='[0:0] [0:1]'; fi
    echo "Audio"
    read -p "Default [1]: " MIA
    if [ "$MIA" == "" -o "$MIA" == "1" ]; then
     MIA=1
     FFM='[a]'
     FSM='-map [a]'
    elif [ "$MIA" == "2" ]; then
     FFM='[a1] [a2]'
     FSM='-map [a1] -map [a2]'
    elif [ "$MIA" == "3" ]; then
     FFM='[a1] [a2] [a3]'
     FSM='-map [a1] -map [a2] -map [a3]'
    elif [ "$MIA" == "4" ]; then
     FFM='[a1] [a2] [a3] [a4]'
     FSM='-map [a1] -map [a2] -map [a3] -map [a4]'
    elif [ "$MIA" == "5" ]; then
     FFM='[a1] [a2] [a3] [a4] [a5]'
     FSM='-map [a1] -map [a2] -map [a3] -map [a4] -map [a5]'
    elif [ "$MIA" == "6" ]; then
     FFM='[a1] [a2] [a3] [a4] [a5] [a6]'
     FSM='-map [a1] -map [a2] -map [a3] -map [a4] -map [a5] -map [a6]'
    fi
    aem="-filter_complex '$MIS concat=n=$cns:v=1:a=$MIA [v] $FFM' -map [v] $FSM"
   fi
   #-i "concat:F1|F2|F3..." -preset medium -aspect 16:9 -strict -2 -g 40
   #-probesize 4G -analyzeduration 3600M -crf 28 -aspect 16:9 -g 40
   #-metadata:s:s:0 title="English"  -map 0:s:0
   mmo="-vf metadata=mode=delete"
   hfo='-ignore_unknown -hide_banner -threads 0'
   aop='-ar 48000'
   cmav='-map 0:a:0 -c:a aac -b:a 320K'
   cmas='-map 0:a:0 -c:a copy'
   cmvs='-map 0:v:0 -c:v copy'
   cmvv='-f matroska -c:v libx265 -b:v 5M -c:a aac -b:a 320k -aspect 16:9 -r 30 -pixel_format yuv444p10 -crf 28 -g 10'
   cmv='-f mp4 -c:v mpeg4 -b:v 5M -c:a aac -b:a 320k -r 30 -aspect 16:9 -crf 18 -vsync 1'
   echo "#!/bin/bash" > .demux
   if   [ "$2" == "a" ]; then
    if [ "$3" == "c" ]; then
     ssc="-af:a:0 'pan=stereo|FL=FC+0.30*FL+0.30*BL|FR=FC+0.30*FR+0.30*BR'"
    elif [ "$3" == "s" ]; then
     ssc="-af silenceremove=0:0:0:-1:1:-40dB"
    fi
    for A in $(find -type f | sort | sed -e 's:'\"':'$(echo "\"")$(echo '\\''\"')$(echo "\"")':g' -e 's:'\'':'$(echo "\"")$(echo '\\'"'")$(echo "\"")':g' -e 's: :_space_:g' -e 's:\.\/::g' | grep -v '.demux' | grep -v '.passwd'); do
     mmc="$(echo $A | sed 's:_space_: :g' | sed -e 's|\"||g' -e 's|\\||g' | sed 's:[^\]*/::g')";mmd="$(echo Audio/$A | sed 's:_space_: :g' | sed -e 's|\"||g' -e 's|\\||g' | sed "s:/$mmc::")";mmx="$(echo ${mmc%.*})";mkdir -p "$mmd/$mmx"
     echo "ffmpeg -hide_banner -threads 0 -i \"$(echo $A | sed 's:_space_: :g')\" $mmo $ssc $cmav $aop \"$(echo $mmd/$mmx.m4a | sed 's:_space_: :g')\"" >> .demux
     if [ "$4" == "s" ]; then
      echo "ffmpeg -hide_banner -threads 0 -i \"$(echo Audio/${A%.*}.m4a | sed 's:_space_: :g')\" -f segment -segment_time 30 -c copy \"$(echo $mmd/$mmx/%03d_$mmx.m4a | sed 's:_space_: :g')\"" >> .demux
     fi
    done
   elif [ "$2" == "v" ]; then
    for V in $(find -type f | sort | sed -e 's:'\"':'$(echo "\"")$(echo '\\''\"')$(echo "\"")':g' -e 's:'\'':'$(echo "\"")$(echo '\\'"'")$(echo "\"")':g' -e 's: :_spacer_:g' -e 's:\.\/::g' | grep -v '.demux' | grep -v '.passwd'); do
     echo "ffmpeg -y $hfo -i \"$(echo $V | sed 's:_spacer_: :g')\" $cmas \"$(echo ${V%.*}.m4a | sed 's:_spacer_: :g')\"
ffmpeg -y $hfo -i \"$(echo $V | sed 's:_spacer_: :g')\" $cmvs \"$(echo ${V%.*}.mpeg | sed 's:_spacer_: :g')\"
ffmpeg -y $hfo -i \"$(echo ${V%.*}.mpeg | sed 's:_spacer_: :g')\" -i \"$(echo ${V%.*}.m4a | sed 's:_spacer_: :g')\" $aem $cmvv $aop \"$(echo ${V%.*}.mkv | sed 's:_spacer_: :g')\"
rm -R \"$(echo ${V%.*}.mpeg | sed 's:_spacer_: :g')\"" >> .demux
    done
   elif [ "$2" == "vc" ]; then
     echo "ffmpeg $hfo $ivf $aem $cmvv $aop \"media.mkv\"" >> .demux
   elif [ "$2" == "vd" ]; then
    vdd=$(echo \'$(pwd)\')
    $GRC mkdir -p /media/dvd && $GRC mount -o ro /dev/sr0 /media/dvd
    vds=$(ls /media/dvd | grep "[Vv]")
    V=$(ls -1v /media/dvd/$vds | grep -e ".I" -e ".i" | grep -e ".B" -e ".b" | grep -v "VTS_[0-9][0-9]_[0]" | grep -v "vts_[0-9][0-9]_[0]" | sed ':a;N;$!ba;s/\n/|\/media\/dvd\/'$vds'\//g')
    echo "ffmpeg $hfo -i \"concat:/media/dvd/$vds/$V\" $aem -c:a ac3 raw_audio.mpeg
ffmpeg $hfo -i \"concat:/media/dvd/$vds/$V\" $cmvs raw_video.mpeg
ffmpeg $hfo -i raw_audio.mpeg -i raw_video.mpeg $aem $cmv $aop 'rip_movie.mkv'" >> $vdd/.demux && cd $vdd
    sed -i 's:::' .demux
    $GRC umount /media/dvd
   elif [ "$2" == "vl" ]; then
    for V in $(find -type f | sort | sed -e 's:'\"':'$(echo "\"")$(echo '\\''\"')$(echo "\"")':g' -e 's:'\'':'$(echo "\"")$(echo '\\'"'")$(echo "\"")':g' -e 's: :_spacer_:g' -e 's:\.\/::g' | grep -v '.demux' | grep -v '.passwd'); do
     echo "ffmpeg $hfo -i \"$(echo $V | sed 's:_spacer_: :g')\" $aem $cmv $aop \"$(echo ${V%.*}.mp4 | sed 's:_spacer_: :g')\"" >> .demux
    done
   fi
   . .demux
   rm -R .demux 2> /dev/null
  fi
 fi
else
 echo "Usage: ctv -g [quality] [slist] | -c [a|v] or [{a|v} {a|c|n} file(s)_in ]
  -g        # Get video
              set quality best normal or audio_only {h|n|a}
              set source list id {o|c|y}
  -c        # Convert video
              set multiple audio or video {a|v}
              set mode Advanced/Complex/Normal(default) {a|c|n}
              set in-files (normal mode only) file1.ext file2.ext ...
              converter uses files output name"
fi
