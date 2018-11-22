#!/bin/bash
if [ "$1" == "" -a "$2" == "" ]; then
 echo "Usage: dran [-c {device}] | -[m|n|u]"
elif [ "$1" == "-e" ]; then
 for t in $(find -type f | sort | sed -e 's:\.\/::g' -e 's: :_spacer_:g' | grep -v '.passwd'); do
   n=0; m=0
  for p in $(cat .passwd | sed -e 's: :_spacer_:g'); do
   num=( $(seq -s _ -w $(cat .passwd | wc -l) | sed 's:_: :g') )
   
   if [ -z "$(echo "$(7z -y -p"$(echo $p | sed 's:_spacer_: :g')"  x "$(echo $t | sed 's:_spacer_: :g')" -oext_fs)" | grep 'Ok')" ]; then
    echo "Wrong pass ${num[$((n++))]} for $(echo $t | sed 's:_spacer_: :g')"
   else
    echo "Sucess pass ${num[$((n++))]} for $(echo $t | sed 's:_spacer_: :g')"
   fi
   if [ "${num[$((m++))]}" == "8" ]; then echo "############"; fi
  done
 done
elif [ "$1" == "-n" ]; then
 if [ "$2" != "" ]; then
  n=0
  if [ "$2" == "e" ]; then
   for t in $(find -type f | sort | sed -e 's:\.\/::g' -e 's: :_spacer_:g' -e 's|\[|_schar-o_|g' -e 's|\]|_schar-c_|g' | grep -v '.passwd'); do
    for int in $(find -type f | wc -l); do
     gdm="$(echo $t | sed 's:[^\]*/::g')"; num=( $(seq -s _ -w $int | sed 's:_: :g') ); rangx=${num[$((n++))]}
     mv "$(echo $t | sed -e 's|_schar-o_|\[|g' -e 's|_schar-c_|\]|g' -e 's:_spacer_: :g')" "$(echo $t | sed 's:'${gdm%.*}':'$rangx'_'$($A | sed 's:[=+/*\\]::g')$($A | sed 's:[=+/*\\]::g')':' | sed -e 's|_schar-o_|\[|g' -e 's|_schar-c_|\]|g' -e 's:_spacer_: :g')"
    done
   done
  elif [ "$2" == "c" ]; then
   for t in $(find -type f | sort | sed -e 's:\.\/::g' -e 's: :_spacer_:g' -e 's|\[|_schar-o_|g' -e 's|\]|_schar-c_|g' | grep -v '.passwd'); do
    for int in $(find -type f | wc -l); do
     gdm="$(echo $t | sed 's:[^\]*/::g')"; num=( $(seq -s _ -w $int | sed 's:_: :g') ); rangx=${num[$((n++))]}
     mv "$(echo $t | sed -e 's|_schar-o_|\[|g' -e 's|_schar-c_|\]|g' -e 's:_spacer_: :g')" "$(echo $t | sed 's:'$gdm':'$rangx'_'$($A | sed 's:[=+/*\\]::g')$($A | sed 's:[=+/*\\]::g')':' | sed -e 's|_schar-o_|\[|g' -e 's|_schar-c_|\]|g' -e 's:_spacer_: :g').genm"
    done
   done
  fi
 else
  echo "Needs an argument!"
 fi
fi
