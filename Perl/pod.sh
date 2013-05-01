#!/bin/bash

######################################### pod.sh ####################################################
# USAGE :		Convert plugins POD data into HTML files
# AUTHOR :		Matthieu FOURNET (fournet.matthieu@gmail.com)
# LICENSE :		GPL - http://www.fsf.org/licenses/gpl.txt
#
# NOTES :
#
# COMMAND LINE :	./pod.sh
#
# VERSION :		20130501
########################################## ##########################################################


########################################## ##########################################################
# CONFIG
########################################## ##########################################################
workDir=$(pwd)'/'
tmp="./tmp.$$"
tmpFiles="pod2htmd.tmp pod2htmi.tmp $tmp"

podRoot=$workDir
podPath='./'

# What is output by "file myFile" when "myFile" is a PERL script.
# If the '-w' is missing from the shebang, 'pod.sh' won't detect the file as a legal PERL script
perlDetectedString=': a /usr/bin/perl -w script text executable'

########################################## ##########################################################
# main()
########################################## ##########################################################
clear

./cleanUp.sh

for fichier in $(ls -1);do
	if [[ $(file $fichier) = $fichier$perlDetectedString ]];then # this comparison works but is ugly :-(
		# if file is a PERL file
		hasPod=$(podchecker $workDir$fichier 1>$tmp 2>&1 )
		hasPodExitCode=$?
		# podchecker output (hasPodExitCode) :
		# 0 : no error found in POD code
		# 1 : error found in POD code
		# 2 : no POD code

		if (( $hasPodExitCode == 0 ));then
			echo -n 'Converting '$fichier' ... '
			pod2html --podroot=$podRoot --podpath=$podPath --header --title=$fichier $workDir$fichier > $workDir$fichier'.html'
			echo '[DONE]'
		elif (( $hasPodExitCode == 1 ));then
			cat $tmp
		fi
	fi
done

for file in $tmpFiles;do
	[ -f $file ] && rm $file
done

########################################## ##########################################################
# the end!
########################################## ##########################################################
