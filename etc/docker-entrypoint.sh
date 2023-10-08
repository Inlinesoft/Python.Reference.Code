#!/bin/bash
set -e

# only needed for local development
if [ -z "$CI" ]
then
    touch /app/.docker_bash_history

    cp -r /opt/ssh /home/appuser/.ssh

    chmod 600 /home/appuser/.ssh/id_rsa

    ssh-keyscan -T 60 bitbucket.org >> /home/appuser/.ssh/known_hosts
fi

exec "$@"