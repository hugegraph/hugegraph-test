#!/bin/bash
### 部署dashboard
dashboard_path=/home/disk3/lxb/workspace/hugegraph_deploy/dashboard
package_path=/home/disk3/lxb/workspace/hugegraph_package

### 判断 dashboard_path 中是否有tar包，并获取md5值
if [ -f ${dashboard_path}/hugegraph-dashboard-3.5.0.tar.gz ]; then
    echo "-----------------------dashboard_path have tar"
    md5_old_cmd=$(md5sum ${dashboard_path}/hugegraph-dashboard-3.5.0.tar.gz)
    array_old=(${md5_old_cmd// / })
    md5_old=${array_old[0]}
    tar_old_path=${array_old[1]}
else
    echo "----------------  md5_old is null"
    md5_old='null'
    tar_old_path='null'
fi
### 获取package_path下的md5
md5_cmd=$(md5sum ${package_path}/hugegraph-dashboard-3.5.0.tar.gz)
array=(${md5_cmd// / })
md5=${array[0]}
tar_new_path=${array[1]}

### 判断md5是否相等,相等就退出停止部署
if [ $md5 = $md5_old ]; then
    echo "----------------- md5 is equal md5_old; exit"
    exit 0
else
    rm -f ${dashboard_path}/hugegraph-dashboard-3.5.0.tar.gz
    cp ${package_path}/hugegraph-dashboard-3.5.0.tar.gz ${dashboard_path}/
fi

### 停止程序,重新部署,修改配置,并重新启动
if [ -d ${dashboard_path}/hugegraph-dashboard-3.5.0/bin ]; then
    echo "------------------------  stop dashboard"
    ${dashboard_path}/hugegraph-dashboard-3.5.0/bin/shutdown.sh
fi
rm -rf ${dashboard_path}/hugegraph-dashboard-3.5.0/*
ls ${dashboard_path}/hugegraph-dashboard-3.5.0/
tar xzvf $tar_new_path -C ${dashboard_path}/hugegraph-dashboard-3.5.0/
ls ${dashboard_path}/hugegraph-dashboard-3.5.0/

### 删除配置
rm -f ${dashboard_path}/hugegraph-dashboard-3.5.0/config/application-dev.properties
rm -f ${dashboard_path}/hugegraph-dashboard-3.5.0/config/application.properties
rm -rf ${dashboard_path}/hugegraph-dashboard-3.5.0/log
rm -rf ${dashboard_path}/hugegraph-dashboard-3.5.0/logs
rm -rf ${dashboard_path}/hugegraph-dashboard-3.5.0/db
## 更新配置
cp ${dashboard_path}/application-dev.properties ${dashboard_path}/hugegraph-dashboard-3.5.0/config/
cp ${dashboard_path}/application.properties ${dashboard_path}/hugegraph-dashboard-3.5.0/config/
cp -rf ${dashboard_path}/db ${dashboard_path}/hugegraph-dashboard-3.5.0/
### 启动dashboard
cd ${dashboard_path}/hugegraph-dashboard-3.5.0/ && ./bin/start.sh
