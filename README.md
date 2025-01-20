# python_hyperloglog

The code implements HyperLogLog (HLL), a probabilistic data structure for efficiently estimating cardinality (count of unique elements) in large datasets. It provides methods to process lists of integers, longs, and strings, converting them to HLL format while maintaining accuracy with minimal memory usage. This is particularly useful for large-scale data processing where exact counting would be impractical.

* How many unique visitors came to our website last year

* How many users got to a certain level of our online game today

* How many different IP addresses did a slice of network traffic come from 

* How many unique visitors searched for a particular news event in a single day

* How many unique IoT devices started to report error codes after the code rollout 

https://cloud.google.com/blog/products/data-analytics/using-hll-speed-count-distinct-massive-datasets

converted from my scala implementation which is way faster


Akka HTTP Algebird example
This project demonstrates the Akka HTTP library. Simple Scala REST service wrapping Twitter Algebird HLL library to make an analytics query engine to provide Distinct Counts for millions of items using HyperLogLog Algorithm.
https://github.com/bigsnarfdude/akka-http-algebird/tree/master
