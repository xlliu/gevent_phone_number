
ps -ef | grep 'python' | grep -v "grep" | awk '{print $2}' > server.pid

kill -9 `cat server.pid`
