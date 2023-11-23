#!/bin/bash
hubble_path=/home/disk3/lxb/workspace/hugegraph_deploy/hubble
package_path=/home/disk3/lxb/workspace/hugegraph_package

### 判断 hubble_path 中是否有tar包，并获取md5值
if [ -f ${hubble_path}/hugegraph-hubble-*.*.*.tar.gz ]; then
    echo "-----------------------hubble_path have tar"
    md5_old_cmd=$(md5sum ${hubble_path}/hugegraph-hubble-*.*.*.tar.gz)
    array_old=(${md5_old_cmd// / })
    md5_old=${array_old[0]}
    tar_old_path=${array_old[1]}
else
    echo "----------------  md5_old is null"
    md5_old='null'
    tar_old_path='null'
fi
### 获取package_path下的md5
md5_cmd=$(md5sum ${package_path}/hugegraph-hubble-*.*.*.tar.gz)
array=(${md5_cmd// / })
md5=${array[0]}
tar_new_path=${array[1]}

### 判断md5是否相等,相等就退出停止部署
if [ $md5 = $md5_old ]; then
    echo "----------------- md5 is equal md5_old; exit"
    exit 0
else
    rm -f ${hubble_path}/hugegraph-hubble-*.*.*.tar.gz
    cp ${package_path}/hugegraph-hubble-*.*.*.tar.gz ${hubble_path}/
fi

### 停止程序,重新部署,修改配置,并重新启动
if [ -d ${hubble_path}/hugegraph-hubble-3.5.0/hugegraph-hubble-* ]; then
    echo "------------------------  stop hubble"
    ${hubble_path}/hugegraph-hubble-3.5.0/hugegraph-hubble-*/bin/stop-hubble.sh
fi
rm -rf ${hubble_path}/hugegraph-hubble-3.5.0/hugegraph-hubble-*
ls ${hubble_path}/hugegraph-hubble-3.5.0/
tar xzvf $tar_new_path -C ${hubble_path}/hugegraph-hubble-3.5.0/
ls ${hubble_path}/hugegraph-hubble-3.5.0/

rm -f ${hubble_path}/hugegraph-hubble-3.5.0/hugegraph-hubble-*/conf/hugegraph-hubble.properties
cp ${hubble_path}/hugegraph-hubble-3.5.0/hugegraph-hubble.properties ${hubble_path}/hugegraph-hubble-3.5.0/hugegraph-hubble-*/conf/
${hubble_path}/hugegraph-hubble-3.5.0/hugegraph-hubble-*/bin/start-hubble.sh
