from __future__ import print_function
from clog.readers import NetCLogStreamReader, find_tail_host
from datetime import date

tail_host = find_tail_host()
print(tail_host)

reader = NetCLogStreamReader(port=3535, host=tail_host, localS3=True)

count = 0

with reader.read_date_range(
    'tmp_kafka_consumer_monitoring',
    date(2017, 12, 1),
    date(2017, 12, 2)
) as reader:
    for line in reader:
        print(line, end='')
        count += 1
        if count > 10:
            print("I've done enough")
            break

print("DONE")



