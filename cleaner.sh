awk -F "," '{gsub("\"", "", $6); print $6}' tweets/tweets.csv
