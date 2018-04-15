#!/usr/bin/env bash

echo "> You are about to commit and push your local files. ARE YOU SURE? [Y/n]"
read resp
if [ "$resp" == "Y" ]; then
  echo "Pushing files...";
  #This command will replace docker's workspace folder by our workspace folder.
  sudo docker cp ./workspace babelnet-container:./
  echo "Done.";
else
  echo "Aborted.";
fi
