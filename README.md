# foofs: foo file system

Simple File System, uses on disk filesystem for blob storage

# API
## GET
get(key)

Param: key (key against which we retrieve value)

### GET Usage:
./getfoofs "key" 

## PUT 
put(key,value)

Params:
- key (key against which we store value)
- value (value stored against key)

### PUT Usage:
./putfoofs "key" "value"

## Hashing Function
- MD5 Hash

## DELETE 
delete(key)

Param: key (key against which we delete value)

### GET Usage:
./deletefoofs "key" 

## System Design
### Master Server (Not yet implemented)
By default, runs on localhost:8000
Keeps track of all of the keys in the server

### Volume Server
By default, runs on localhost:8001
Actually stores the values in memory

# References and Inspo:
https://github.com/seaweedfs/seaweedfs
https://github.com/geohot/minikeyvalue
https://www.educative.io/courses/grokking-modern-system-design-interview-for-engineers-managers/JQwV8kX3nlK

# Stretch Goals
1. Implement Master Server 
2. Implement Load Balancing and consistent hashing (See Dynamo Reference)
    - https://assets.amazon.science/ac/1d/eb50c4064c538c8ac440ce6a1d91/dynamo-amazons-highly-available-key-value-store.pdf
3. Docker Deployment
4. Multiple Instances of Servers (Distributed)




