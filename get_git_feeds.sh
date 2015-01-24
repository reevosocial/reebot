#!/bin/bash
cp sources.txt sources.txt.old
LIST=`xidel http://git.reevo.org/  -e "<td class='sublevel-repo'><a>{@href}</a></td>*"` && for i in `echo $LIST`; do echo "GIT|http://git.reevo.org$i/atom"; done >> sources.txt && sort -u sources.txt > sources.txt.tmp && mv sources.txt.tmp sources.txt

echo "Se agregaron las siguientes fuentes: "
diff sources.txt sources.txt.old
#rm sources.txt.old
