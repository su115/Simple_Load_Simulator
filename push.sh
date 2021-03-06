#! /bin/bash 

git pull origin $(git rev-parse --abbrev-ref HEAD)
COMMENT="$@"
if [ -z $COMMENT ]; then
	COMMENT="No comment"
	echo "$COMMENT"
fi
#COMMIT_NUM=$( git log -1  | cut -d '#' -f 2- | cut -d ' ' -f 1 ) # set Num commit
#if [ -z COMMIT_NUM ]; then 
COMMIT_NUM=$( cat README.md | grep "Pipeline" | cut -d ' ' -f 3)
#fi

COMMIT_NUM=$(( 1+$COMMIT_NUM ))
echo "Commit #$COMMIT_NUM"
sed -i "s/Pipeline: .*/Pipeline: $COMMIT_NUM/" README.md
git add .
git commit -m "$COMMENT #$COMMIT_NUM $(date)"
git push origin $(git rev-parse --abbrev-ref HEAD)
