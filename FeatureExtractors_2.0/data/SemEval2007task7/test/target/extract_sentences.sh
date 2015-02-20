#!/bin/bash

FILE=$1
TEXTS=$2
SENTENCES=$3
DESTINATION=$4
IFS=$'\n'
mkdir -p $DESTINATION/$SENTENCES"S"
rm -rf $DESTINATION/$SENTENCES"S"/*.xml
file_count=0
current_sentence="s000"
for text in `seq 1 $TEXTS`; do
	sentence_count=0
	echo "$text"
	for instance in `cat $FILE | grep "d00$text" | grep instance`;do
		export target=$DESTINATION/$SENTENCES"S"/text$text"_"$SENTENCES"S"_$file_count.xml
		if [ "$sentence_count" -le "$SENTENCES" ]; then
            if [ "$sentence_count" -eq "$SENTENCES" ]; then
                echo -e "</text>\n" >> $target
                echo -e "</corpus>\n" >> $target
                let "file_count++"
                export target=$DESTINATION/$SENTENCES"S"/text$text"_"$SENTENCES"S"_$file_count.xml
                echo -e "<corpus>" >$target
                echo -e "<text id=\"d00$text\">\n" >>$target
                let "sentence_count=0"
            fi
            if [ "$sentence_count" -eq "0" ]; then
                echo -e "<corpus>" >$target
                echo -e "<text id=\"d00$text\">\n" >>$target
                let "sentence_count=0"
            fi
                if [[ "$current_sentence" != "`echo $instance | cut -d'.' -f2`" ]]; then
                    if [[ "$current_sentence" != "s000" ]]; then
                        echo -e "</sentence>" >> $target
                    fi
                    current_sentence=`echo $instance | cut -d'.' -f2`
                    let "sentence_count++"
                    if [ "$sentence_count" -lt "$SENTENCES" ]; then
                        echo -e "<sentence id=\"$current_sentence\">\n" >> $target
                    fi
                fi
            if [ "$sentence_count" -lt "$SENTENCES" ]; then
                echo "$instance" >> $target
            fi
		fi
	done
	let "file_count=0"
	echo -e "</text>\n" >> $target
	echo -e "</corpus>\n" >>$target
done