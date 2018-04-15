#!/usr/bin/env bash

echo "> You are about to replace all your local files. This will to remove all your uncommited changes. ARE YOU SURE? [Y/n]"
read resp
if [ "$resp" == "Y" ]; then
  echo "Pulling files..."
  #This command will replace our workspace folder by host's workspace folder.
  sudo docker cp babelnet-container:./workspace/ .
  sudo chmod -R 777 .
  echo "Done."
else
  echo "Aborted. Your local files are safe now."
fi
