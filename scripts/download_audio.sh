#!/bin/sh
set -eu

if [ "$#" -ne 2 ]; then
  echo "usage: download_audio.sh <url> <output_mp3_path>" >&2
  exit 1
fi

url="$1"
output_path="$2"
output_dir="$(dirname "$output_path")"
template="${output_path%.mp3}.%(ext)s"

mkdir -p "$output_dir"

yt-dlp \
  --no-playlist \
  --extract-audio \
  --audio-format mp3 \
  --audio-quality 0 \
  --output "$template" \
  "$url"

if [ ! -f "$output_path" ]; then
  echo "downloaded file not found: $output_path" >&2
  exit 1
fi

printf '{"file_path":"%s"}\n' "$output_path"
