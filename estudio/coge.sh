for id in "$@"; do
  mkdir -p v/$id; cd v/$id
  yt-dlp --skip-download --write-info-json --write-auto-subs --write-subs --sub-langs "es-orig,en-orig,es,en" --sub-format vtt -o "x" "https://www.youtube.com/shorts/$id" >/dev/null 2>&1
  yt-dlp -f sb0 -o "sb.%(ext)s" "https://www.youtube.com/shorts/$id" >/dev/null 2>&1
  python3 ../../saca.py sb.mhtml sb >/dev/null 2>&1
  python3 -c "import json;d=json.load(open('x.info.json'));print(d.get('view_count'),'|',d.get('duration'),'|',d.get('channel'),'|',d.get('title'))" 2>/dev/null > info.txt
  echo "$id $(cat info.txt) subs:$(ls x*.vtt 2>/dev/null | tr '\n' ' ') sb:$(ls sb 2>/dev/null | wc -l)"
  cd ../..; sleep 4
done
