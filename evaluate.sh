#!/bin/bash

docker_command=(docker run)
entrypoint=(python3 evaluate.py)
docker_params=(
    --rm
)
script_params+=(
)

while test $# -gt 0; do
    case "$1" in
        --predicted)
            shift
            file_name=$(basename $1)
            docker_params+=(-v "$(realpath $1)":/home/user/workspace/predicted/${file_name}:ro)
            script_params+=(--predicted "/home/user/workspace/predicted/${file_name}")
            shift
            ;;
        --true)
            shift
            file_name=$(basename $1)
            docker_params+=(-v "$(realpath $1)":/home/user/workspace/true/${file_name}:ro)
            script_params+=(--true "/home/user/workspace/true/${file_name}")
            shift
            ;;
        --output-dir)
            shift
            docker_params+=(-v "$(realpath $1)":/home/user/workspace/output)
            script_params+=(--output-dir "/home/user/workspace/output")
            shift
            ;;
        *)
            script_params+=($1)
            shift
            ;;
    esac
  done  

echo "Building enviroment..."

${docker_command[@]} -it \
    ${docker_params[@]} \
    $(docker build -q --build-arg USER_UID=$(id -u) --build-arg USER_GID=$(id -g) .) \
    ${entrypoint[@]} \
    ${script_params[@]} \
