#!/bin/bash
K_FHEAD='~~~~~~~~~~~~~~~~~~~~~~'
K_SHEAD='######################'
A='openssl rand -base64 3'
if [ "$1" == "" -a "$2" == "" ]; then
 echo "Usage: randx.sh -[e|m|n] (options)"
 echo "Examples: 
        ./randx.sh -e			# Extract all compressed files (Debug for massive splitted)
        ./randx.sh -m (dest_dir)	# Move recursive subdir files to a new dir
        ./randx.sh -n [option]
          Option
           e                     # Change all name files to a random_name.original_ext
           c                     # Change all name files to a random_name.random_ext"
else
 for T in $(find -type f | sort | grep -v '\.\/Audio\|\.\/Data\|\.\/Video\|\.passwd\|randx.sh\|\.reglog' | wc -l); do
  rang_x=( $(seq -s _ -w $T | sed 's|_| |g') ); for M in $(find -type f | sort | grep -v '\.\/Audio\|\.\/Data\|\.\/Video\|\.passwd\|\.remuxer\|\.reglog\|\.ass\|\.srt' | sed "s|\./||;s| |:scs:|g"); do
  name_r="$(echo $M | sed "s|:scs:| |g")"; name_dir="$(dirname "$name_r")"; name_f="$(echo $name_r | sed "s|[^\]*/||g")"; name_s="${name_f%.*}"; f_ext="$(echo $name_f | sed "s|\[||g;s|\]||g;s|$(echo $name_s | sed "s|\[||g;s|\]||g")||")"
  if [ "$1" == "-m" -a "$2" != "" ]; then if [ ! -d $2 ]; then mkdir -p $2; fi; mv "$name_r" $2 > /dev/null 2>&1
  elif [ "$1" == "-e" ]; then r=0; s=0
   if [ ! -e .passwd ]; then printf "Insert all compressed file passwords here. Replace this line." > .passwd; fi
   for P in $(cat .passwd | sed -e 's| |:scs:|g'); do seqnum=( $(seq -s _ -w $(cat .passwd | wc -l) | sed 's|_| |g') ); mkdir -p Data
    if [ -z "$(echo "$(7z -y -p"$(echo $P | sed 's|:scs:| |g')" x "$name_r" -oData)" | grep 'Ok')" ]; then
     if [ -d "$HOME/.wine/drive_c/Program Files/WinRAR" ]; then echo "Trying extract $name_f with WinRAR"; wine C:\\Program\ Files\\WinRAR\\UnRAR x "$name_r" -cl -kb -p"$(echo $P | sed 's|:scs:| |g')" -y Data > .logone 2>&1; cat .logone | grep 'done' > .extlog; rm -R .logone; if [ -z "$(cat .extlog)" ]; then echo "WinRAR can't extract $name_f"; else echo "Sucess extraction for $name_f"; fi; fi
    if [ ! -e .extlog ]; then echo "Wrong pass ${seqnum[$((r++))]} for $name_f"; else rm -R .extlog; fi
    else echo "Sucess pass ${seqnum[$((r++))]} for $name_f"; fi
    if [ "${seqnum[$((s++))]}" == "$seqnum" ]; then echo "$K_FHEAD$K_SHEAD"; fi
   done
  elif [ "$1" == "-n" ]; then
   if   [ "$2" == "e" ]; then
    mv "$name_r" "$name_dir/${rang_x[$((y++))]}-$($A | sed 's|\(.*\)|\L\1|;s|[=+/*\\]||g')$($A | sed 's|\(.*\)|\L\1|;s|[=+/*\\]||g')$f_ext"
   elif [ "$2" == "c" ]; then
    mv "$name_r" "$name_dir/${rang_x[$((z++))]}-$($A | sed 's|\(.*\)|\L\1|;s|[=+/*\\]||g')$($A | sed 's|\(.*\)|\L\1|;s|[=+/*\\]||g').$($A | sed 's|\(.*\)|\L\1|;s|[=+/*\\]||g')"
   else
    echo "Needs an argument!"; exit 0
   fi
  fi; printf "."; done
 done; printf "\n"
fi
