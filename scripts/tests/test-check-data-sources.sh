#!/usr/bin/env bash
# Tests for scripts/check-data-sources.sh against a local fixture server.
set -uo pipefail

here="$(cd "$(dirname "$0")" && pwd)"
script="$here/../check-data-sources.sh"
work="$(mktemp -d)"

python3 -I "$here/fixture_server.py" > "$work/port" &
server_pid=$!
trap 'kill "$server_pid" 2>/dev/null; rm -rf "$work"' EXIT
for _ in $(seq 50); do [ -s "$work/port" ] && break; sleep 0.1; done
base="http://127.0.0.1:$(head -n1 "$work/port")"

failures=0

# Runs the check with the given source lines; sets $output and $status.
run_check() {
  printf '%s\n' "$@" > "$work/sources.tsv"
  output="$(RETRY_DELAY=0 "$script" "$work/sources.tsv" 2>&1)"
  status=$?
}

expect() {
  local name="$1" condition="$2"
  if eval "$condition"; then
    echo "ok   $name"
  else
    echo "FAIL $name"
    echo "     condition: $condition"
    echo "     status: $status"
    echo "$output" | sed 's/^/     | /'
    failures=$((failures + 1))
  fi
}

tab=$'\t'

run_check "Good GeoJSON${tab}geojson${tab}$base/geojson"
expect "a healthy GeoJSON source passes" \
  '[ "$status" -eq 0 ] && grep -Eq "^PASS +Good GeoJSON" <<<"$output"'

run_check "Missing${tab}geojson${tab}$base/missing" "Good GeoJSON${tab}geojson${tab}$base/geojson"
expect "an HTTP error fails the run but later sources are still checked" \
  '[ "$status" -ne 0 ] && grep -Eq "^FAIL +Missing +HTTP 404" <<<"$output" && grep -Eq "^PASS +Good GeoJSON" <<<"$output"'

run_check "No CORS${tab}geojson${tab}$base/no-cors"
expect "a source without Access-Control-Allow-Origin fails" \
  '[ "$status" -ne 0 ] && grep -Eq "^FAIL +No CORS +.*Access-Control-Allow-Origin" <<<"$output"'

run_check "Other origin${tab}geojson${tab}$base/other-origin"
expect "a source that only allows another origin fails" \
  '[ "$status" -ne 0 ] && grep -Eq "^FAIL +Other origin +.*https://kort.example.dk" <<<"$output"'

run_check "HTML page${tab}geojson${tab}$base/html" "Plain JSON${tab}geojson${tab}$base/json"
expect "a GeoJSON source that returns HTML or non-GeoJSON JSON fails" \
  '[ "$status" -ne 0 ] && grep -Eq "^FAIL +HTML page +.*not GeoJSON" <<<"$output" && grep -Eq "^FAIL +Plain JSON +.*not GeoJSON" <<<"$output"'

run_check "Plain JSON${tab}json${tab}$base/json"
expect "a JSON source that returns JSON passes" \
  '[ "$status" -eq 0 ] && grep -Eq "^PASS +Plain JSON" <<<"$output"'

run_check "HTML page${tab}json${tab}$base/html"
expect "a JSON source that returns HTML fails" \
  '[ "$status" -ne 0 ] && grep -Eq "^FAIL +HTML page +.*not JSON" <<<"$output"'

run_check "Typo${tab}geojsn${tab}$base/geojson"
expect "an unknown kind fails" \
  '[ "$status" -ne 0 ] && grep -Eq "^FAIL +Typo +.*unknown kind geojsn" <<<"$output"'

run_check "Overpass${tab}json${tab}$base/overpass${tab}data=[out:json];out;"
expect "a source with a body is checked with POST" \
  '[ "$status" -eq 0 ] && grep -Eq "^PASS +Overpass" <<<"$output"'

run_check "Style${tab}style${tab}$base/style"
expect "a map style source that returns a style passes" \
  '[ "$status" -eq 0 ] && grep -Eq "^PASS +Style" <<<"$output"'

run_check "Not a style${tab}style${tab}$base/json"
expect "a map style source that returns other JSON fails" \
  '[ "$status" -ne 0 ] && grep -Eq "^FAIL +Not a style +.*not a map style" <<<"$output"'

run_check "Tiles${tab}tile${tab}$base/tilejson"
expect "a tile source whose first tile loads passes" \
  '[ "$status" -eq 0 ] && grep -Eq "^PASS +Tiles" <<<"$output"'

run_check "Broken tiles${tab}tile${tab}$base/tilejson-broken"
expect "a tile source whose tiles are missing fails" \
  '[ "$status" -ne 0 ] && grep -Eq "^FAIL +Broken tiles +.*tile .*HTTP 404" <<<"$output"'

run_check "Not TileJSON${tab}tile${tab}$base/json"
expect "a tile source that returns other JSON fails" \
  '[ "$status" -ne 0 ] && grep -Eq "^FAIL +Not TileJSON +.*not TileJSON" <<<"$output"'

run_check "Busy once${tab}geojson${tab}$base/busy-once"
expect "a source that is briefly busy passes on retry" \
  '[ "$status" -eq 0 ] && grep -Eq "^PASS +Busy once" <<<"$output"'

run_check "Busy${tab}geojson${tab}$base/busy"
expect "a source that stays busy fails" \
  '[ "$status" -ne 0 ] && grep -Eq "^FAIL +Busy +HTTP 503" <<<"$output"'

[ "$failures" -eq 0 ] && echo "All tests passed" || { echo "$failures test(s) failed"; exit 1; }
