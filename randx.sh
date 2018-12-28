#!/bin/bash
if [ "$1" == "" -a "$2" == "" ]; then
 echo "Usage: randx.sh -[e|m|n] (options)"
 echo "Examples: 
        ./randx.sh -e            # Extract all compressed files (Debug for massive splitted)
        ./randx.sh -m (dest_dir) # Move all files to an new dir
        ./randx.sh -n
          Options
           e                     # Change all name files to a random_name.original_ext
           c                     # Change all name files to a random_name.random_ext"
elif [ "$1" == "-m" -a "$2" != "" ]; then
   for t in $(find -type f | sort | sed -e 's:\.\/::g' -e 's: :_space_:g' -e 's|\[|_schar-o_|g' -e 's|\]|_schar-c_|g'); do fody="$(echo $t | sed -e 's|_schar-o_|\[|g' -e 's|_schar-c_|\]|g' -e 's:_space_: :g')"
    if [ ! -d $2 ]; then mkdir -p $2; fi
    if [ "$3" != "" ]; then fido="${fody%.*}.$3"; else fido="$fody"; fi; mv "$fido" $2 > /dev/null 2>&1; printf "."; done
elif [ "$1" == "-e" ]; then
 for t in $(find -type f | sort | sed -e 's:\.\/::g' -e 's: :_spacer_:g' | grep -v '\.part[2-9]' | grep -v '.passwd'); do
  n=0; m=0
  for p in $(cat .passwd | sed -e 's: :_spacer_:g'); do num=( $(seq -s _ -w $(cat .passwd | wc -l) | sed 's:_: :g') ); mkdir -p Data
   if [ -z "$(echo "$(7z -y -p"$(echo $p | sed 's:_spacer_: :g')" x "$(echo $t | sed 's:_spacer_: :g')" -oData)" | grep 'Ok')" ]; then
    # Requires any wine recent version and winrar 5.20+ or winrar extractor of rar type 5+ (optional)
    if [ -d "$HOME/.wine/drive_c/Program Files/WinRAR" ]; then echo "Trying extract with WinRAR"
     wine C:\\Program\ Files\\WinRAR\\UnRAR x "$(echo $t | sed 's:_spacer_: :g')" -cl -kb -p"$(echo $p | sed 's:_spacer_: :g')" -y Data > .logone 2>&1; cat .logone | grep 'correcto' > .extlog; rm -R .logone; if [ -z "$(cat .extlog)" ]; then echo "WinRAR can't extract $(echo $t | sed 's:_spacer_: :g')"; else echo "Sucess extraction for $(echo $t | sed 's:_spacer_: :g')"; fi; fi
    # If don't exists any .wine dir, prints normal wrong message.
    if [ ! -e .extlog ]; then echo "Wrong pass ${num[$((n++))]} for $(echo $t | sed 's:_spacer_: :g')"; else rm -R .extlog; fi
   else
    echo "Sucess pass ${num[$((n++))]} for $(echo $t | sed 's:_spacer_: :g')"
   fi
   # Change (---) to desired header
   if [ "${num[$((m++))]}" == "$num" ]; then echo "---"; fi
  done
 done
elif [ "$1" == "-n" ]; then
 if [ "$2" != "" ]; then
  n=0
  if [ "$2" == "e" ]; then
   for t in $(find -type f | sort | sed -e 's:\.\/::g' -e 's: :_spacer_:g' -e 's|\[|_schar-o_|g' -e 's|\]|_schar-c_|g' | grep -v '.passwd'); do
    for int in $(find -type f | wc -l); do
     gdm="$(echo $t | sed 's:[^\]*/::g')"; num=( $(seq -s _ -w $int | sed 's:_: :g') ); rangx=${num[$((n++))]}
     mv "$(echo $t | sed -e 's|_schar-o_|\[|g' -e 's|_schar-c_|\]|g' -e 's:_spacer_: :g')" "$(echo $t | sed 's:'${gdm%.*}':'$rangx'_'$($(openssl rand -base64 5) | sed 's:[=+/*\\]::g')$($() | sed 's:[=+/*\\]::g')':' | sed -e 's|_schar-o_|\[|g' -e 's|_schar-c_|\]|g' -e 's:_spacer_: :g')"
    done
   done
  elif [ "$2" == "c" ]; then
   for t in $(find -type f | sort | sed -e 's:\.\/::g' -e 's: :_spacer_:g' -e 's|\[|_schar-o_|g' -e 's|\]|_schar-c_|g' | grep -v '.passwd'); do
    for int in $(find -type f | wc -l); do
     gdm="$(echo $t | sed 's:[^\]*/::g')"; num=( $(seq -s _ -w $int | sed 's:_: :g') ); rangx=${num[$((n++))]}
     mv "$(echo $t | sed -e 's|_schar-o_|\[|g' -e 's|_schar-c_|\]|g' -e 's:_spacer_: :g')" "$(echo $t | sed 's:'$gdm':'$rangx'_'$($(openssl rand -base64 5) | sed 's:[=+/*\\]::g')$($(openssl rand -base64 5) | sed 's:[=+/*\\]::g')':' | sed -e 's|_schar-o_|\[|g' -e 's|_schar-c_|\]|g' -e 's:_spacer_: :g').gextd"
    done
   done
  fi
 else
  echo "Needs an argument!"
 fi
fi
