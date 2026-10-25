#!/usr/bin/env bash
# Checks that every Data source on the curated list still answers from a browser.
#
# Usage: scripts/check-data-sources.sh [SOURCES_FILE]
#
# SOURCES_FILE defaults to scripts/data-sources.tsv. Each line is
#   NAME <tab> KIND <tab> URL [<tab> POST_BODY]
# Blank lines and lines starting with # are ignored.
#
# Prints a pass/fail table and exits non-zero if any source fails.
# Busy answers (HTTP 429, 5xx or no answer) are retried after RETRY_DELAY
# seconds (default 15), up to three attempts in all.
set -uo pipefail

sources_file="${1:-$(dirname "$0")/data-sources.tsv}"
# Stands in for any other site, such as a Participant's own GitHub Pages site.
origin="https://example.github.io"
user_agent="byg-din-egen-gis-applikation data source check (+https://github.com/steenhulthin/byg-din-egen-gis-applikation)"
retry_delay="${RETRY_DELAY:-15}"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

# Fetches URL (POSTing BODY if given) into $work/body and $work/headers.
# Prints the HTTP status, or 000 if the request failed. Retries busy answers.
fetch() {
  local url="$1" body="${2:-}"
  local args=(-s -m 60 -o "$work/body" -D "$work/headers" -w '%{http_code}'
    -A "$user_agent" -H "Origin: $origin")
  [ -n "$body" ] && args+=(--data-binary "$body")
  local attempt status
  for attempt in 1 2 3; do
    status="$(curl "${args[@]}" "$url" < /dev/null)" || status=000
    case "$status" in 000 | 429 | 5??) ;; *) break ;; esac
    [ "$attempt" -lt 3 ] && sleep "$retry_delay"
  done
  echo "$status"
}

# Prints the value of response header NAME from the last fetch, or nothing.
header() {
  awk -v name="$1" '
    tolower($1) == tolower(name ":") { sub(/^[^:]*:[ \t]*/, ""); sub(/\r$/, ""); print; exit }' \
    "$work/headers"
}

# Prints the start of the last response body on one line.
snippet() {
  head -c 80 "$work/body" | tr -s '\r\n\t' ' '
}

# Requests URL like a browser on another site would. Prints the reason and
# returns non-zero unless it answers 200 with Access-Control-Allow-Origin: *.
request() {
  local url="$1" body="${2:-}"
  local status allow_origin
  status="$(fetch "$url" "$body")"
  if [ "$status" != 200 ]; then
    echo "HTTP $status"
    return 1
  fi
  allow_origin="$(header Access-Control-Allow-Origin)"
  if [ -z "$allow_origin" ]; then
    echo "no Access-Control-Allow-Origin header"
    return 1
  fi
  if [ "$allow_origin" != '*' ]; then
    echo "Access-Control-Allow-Origin is $allow_origin, not *"
    return 1
  fi
}

# Succeeds if the last response body is JSON for which jq FILTER is true.
body_matches() {
  jq -e "$1" "$work/body" > /dev/null 2>&1
}

# Checks one source. Prints a detail message and returns non-zero on failure.
check() {
  local kind="$1" url="$2" body="${3:-}"
  request "$url" "$body" || return 1
  case "$kind" in
    geojson)
      body_matches '.type == "FeatureCollection" and (.features | type == "array")' ||
        { echo "response is not GeoJSON: $(snippet)"; return 1; }
      ;;
    json)
      body_matches . || { echo "response is not JSON: $(snippet)"; return 1; }
      ;;
    style)
      body_matches '.version == 8 and (.sources | type == "object")' ||
        { echo "response is not a map style: $(snippet)"; return 1; }
      ;;
    tile)
      body_matches '.tiles[0] | type == "string"' ||
        { echo "response is not TileJSON: $(snippet)"; return 1; }
      local tile_url
      tile_url="$(jq -r '.tiles[0] | gsub("\\{[zxy]\\}"; "0")' "$work/body")"
      request "$tile_url" > "$work/reason" ||
        { echo "tile $tile_url: $(cat "$work/reason")"; return 1; }
      [ -s "$work/body" ] || { echo "tile $tile_url is empty"; return 1; }
      ;;
    *)
      echo "unknown kind $kind"
      return 1
      ;;
  esac
  echo "HTTP 200, CORS ok, $kind"
}

# Prints one table row. Pads by characters, not bytes, so æøå line up.
row() {
  local result="$1" name="$2" detail="$3"
  printf '%-8s%s%*s  %s\n' "$result" "$name" $((40 - ${#name})) '' "$detail"
}

row RESULT SOURCE DETAIL
failed=0
while IFS=$'\t' read -r name kind url body; do
  case "$name" in '' | '#'*) continue ;; esac
  if detail="$(check "$kind" "$url" "$body")"; then
    row PASS "$name" "$detail"
  else
    row FAIL "$name" "$detail"
    failed=$((failed + 1))
  fi
done < "$sources_file"

[ "$failed" -eq 0 ]
