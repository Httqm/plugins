#!/bin/bash

######################################### cleanUp.sh ################################################
# Move backup files to the specified "local trash" folder
#
# version : 20130423
########################################## ##########################################################

trashName='Poubelle'
trashFolder='./'$trashName
tmpFile='tmp.'$$

# $tmpFile is necessary to count the number of trashed files at each execution of the script
# (could have done a function for that also...)
# better than 'touch' as this creates an empty file if it doesn't exist yet, or empties an existing file.
> $tmpFile


# create the trash folder if it doesn't exist yet
[ ! -d $trashFolder ] && mkdir $trashFolder


# find and move backup files to the trash folder
find . -regextype posix-egrep -regex '.*(*~|*_OLD|*pyc)' -a ! -regex '.*('$trashName').*' -exec echo {} >> $tmpFile \;


while read fileForTheTrash;do
#	echo $fileForTheTrash
    mv "$fileForTheTrash" $trashFolder
done < $tmpFile


nbTrashedFiles=$(find $trashFolder -type f | wc -l)
nbTrashedFolders=$(find $trashFolder -type d | wc -l) # also counts '.', so need to subtract 1
let nbTrashedFolders--

trashSize=$(du -sh $trashFolder | cut -f1)

echo $(cat $tmpFile | wc -l)' file(s) moved to '$trashFolder' ( '$nbTrashedFiles' files, '$nbTrashedFolders' folders trashed so far. Trash size = '$trashSize' )'

rm $tmpFile
