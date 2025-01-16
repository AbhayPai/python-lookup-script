# Lookup script

## Script for csv reports of file attributes
### with simple command
```
python3 ./file-lookup-csv/main.py ./folders ./file-lookup-csv/output.csv
```

### with no hang up command
```
nohup python3 ./file-lookup-csv/main.py ./folders output.csv > nohup.log 2>&1 &
```

## Script for csv reports of Total files & Total size.
### with simple command
```
python3 ./file-lookup-reports/main.py ./folders ./file-lookup-reports/output.csv
```

### with no hang up command
```
nohup python3 ./file-lookup-reports/main.py ./folders output.csv > nohup.log 2>&1 &
```

## Script for csv reports of file attributes & upload file in s3 bucket.
### with simple command
```
python3 ./file-lookup-csv-s3/main.py ./folders ./file-lookup-csv-s3/output.csv
```

### with no hang up command
```
nohup python3 ./file-lookup-csv-s3/main.py ./folders output.csv > nohup.log 2>&1 &
```


## Localstack for s3 bucket testing
```
docker-compose up -d
```
