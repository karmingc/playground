#!/bin/bash
URL=${1}
PORT=${2:-443}

now=$(date +%s)
notAfterString=$(echo q | openssl s_client -servername "${URL}" "${URL}:${PORT}" 2>/dev/null | openssl x509 -noout -enddate | awk -F"=" '{ print $2; }')
if [[ "$(uname)" == "Darwin" ]] ; then
  echo "its darwin"
  notAfter=$(date -d "${notAfterString}" +%s)
else
  notAfter=$(date -d "${notAfterString}" +%s)
fi

secondsLeft=$(($notAfter-$now))

data="
{
    \"resourceMetrics\": [
      {
        \"resource\": {
          \"attributes\": [
            {
              \"key\": \"service.name\",
              \"value\": {
                \"stringValue\": \"${URL}\"
              }
            }
          ]
        },
        \"scopeMetrics\": [
          {
            \"metrics\": [
              {
                \"name\": \"tls.server.not_after.time_left\",
                \"unit\": \"s\",
                \"description\": \"\",
                \"gauge\": {
                  \"dataPoints\": [
                    {
                      \"asInt\": ${secondsLeft},
                      \"timeUnixNano\": ${now}000000000
                    }
                  ]
                }
              }
            ]
          }
        ]
      }
    ]
  }
"
curl -X POST -H "Content-Type: application/json" -d "${data}" -i localhost:4318/v1/metrics
