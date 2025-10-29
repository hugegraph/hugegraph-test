set -ex # see detailed output
kill -9 $(jps | grep hg | awk '{print $1}' )
kill -9 $(jps | grep HugeGraph | awk '{print $1}' )
rm -rf ../graph
rm -rf ./config/dataset
