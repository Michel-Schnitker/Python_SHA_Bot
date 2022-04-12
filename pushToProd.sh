#!/bin/bash

SSH_ALIAS="hetzner-vserver"

if [ $USER != "emily" ]; then
  echo "Nicht meine Shell-Skripte benutzen 😡"
  exit 1
fi

rsync -e ssh --info=progress2 --exclude "venv/" -a . "shabot@$SSH_ALIAS:code"

ssh $SSH_ALIAS "sudo systemctl daemon-reload; sudo systemctl restart shabot.service"
