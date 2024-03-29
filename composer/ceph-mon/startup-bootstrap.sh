#!/bin/bash
set -e
# set -x

echo ">>>> PREPARING AND BOOTSTRAPING THIS MONITOR FOR A NEW CLUSTER..."

if [ ! -f $MONITOR_DATA_PATH/initialized ]; then
    echo ">>> Creating new cluster..."
    mkdir -p $MONITOR_DATA_PATH

    echo "Generating cluster keys..."
    echo ""
    #http://docs.ceph.com/docs/master/rados/configuration/auth-config-ref/
    ceph-authtool --create-keyring /etc/ceph/keyring --gen-key -n mon. --cap mon 'allow *'
    ceph-authtool /etc/ceph/keyring --gen-key -n client.admin --set-uid=0 --cap mon 'allow *' --cap osd 'allow *' --cap mds 'allow *' --cap mgr 'allow *'

    if [ ! "${ETCD_URL}" == "" ]; then
        echo "Sending keys to ETCD..."
        while true; do
            etcdctl --endpoints $ETCD_URL ls / && break
            echo "Retrying to connect to etcd at $ETCD_URL..."
            sleep 1
        done
        set +e
        etcdctl --endpoints $ETCD_URL mkdir $CLUSTER_NAME
        set -e
        KEYRING=$(cat /etc/ceph/keyring | base64)
        echo "Keyring file:"
        echo "===="
        cat /etc/ceph/keyring
        echo "===="
        echo ""
        echo "Keyring in base64:"
        echo "===="
        echo "$KEYRING"
        echo "===="
        etcdctl --endpoints $ETCD_URL set "/$CLUSTER_NAME/keyring" "${KEYRING}"
    fi

    echo "Creating CRUSH map..."
    if [ "$FS_ID" == "" ]; then
        export FS_ID=$(uuidgen)
        echo "FS_ID=$FS_ID"
    fi
    monmaptool --create --add $MONITOR_NAME ${MONITOR_ADVERTISE_ADDRESS} --clobber --fsid ${FS_ID} /tmp/monmap
    ceph-mon --mkfs --mon-data $MONITOR_DATA_PATH --monmap /tmp/monmap --debug_mon $LOG_LEVEL --id $MONITOR_NAME --cluster $CLUSTER_NAME --keyring /etc/ceph/keyring

    touch $MONITOR_DATA_PATH/initialized
else
    echo ">>> Monitor already initialized before. Reusing state."
fi

echo "KEYRING:"
cat /etc/ceph/keyring
echo ""
echo "Starting Ceph Monitor $CLUSTER_NAME-$MONITOR_NAME..."
ceph-mon -d --debug_mon $LOG_LEVEL --mon-data $MONITOR_DATA_PATH --id $MONITOR_NAME --cluster $CLUSTER_NAME --keyring /etc/ceph/keyring
