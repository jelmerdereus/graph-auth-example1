#!/usr/bin/env bash
# get local image IDs
image_names=$(podman image ls | awk '{ if(/localhost/) { print $1 } }' | xargs)
printf "Removing images: %s\n" "$image_names"

# remove images
image_ids=$(podman image ls | awk '{ if(/localhost/) { print $3 } }' | xargs)
podman rmi "$image_ids"