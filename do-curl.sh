
curlReq="curl http://127.0.0.1:9001/metrics"

while :
do
    $curlReq
    sleep 3
done
