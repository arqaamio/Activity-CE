#!/bin/bash

set +ex

#@--- Function to setup the cluster ---@#
set_up_cluster_dev_env() {

    if [[ $GITHUB_REF == "refs/heads/develop" ]]
    then

        #@--- Initialize terraform ---@#
        echo " ----- inititalize the backend --------- "
        terraform init -backend-config "bucket=$BACKEND_BUCKET_DEV_ENV" \
            -backend-config "key=$STATE_FILE_DEV_ENV" \
            -backend-config "access_key=$SPACES_ACCESS_KEY" \
            -backend-config "secret_key=$SPACES_SECRET_KEY"

        #@--- Run terraform command to plan infrastructure ---@#
        echo "----- show plan -------------------"
        terraform plan -lock=false  -var "cluster_name=$CLUSTER_NAME_DEV_ENV" \
            -var "cluster_region=$CLUSTER_REGION" \
            -var "kubernetes_version=$K8S_VERSION" \
            -var "node_type=$NODE_TYPE" \
            -var "max_node_number=$MAX_NODE_NUM" \
            -var "min_node_number=$MIN_NODE_NUM" \
            -var "digital_ocean_token=$SERVICE_ACCESS_TOKEN" \
            -var "db_size=$DB_SIZE" \
            -var "postgres_version=$PG_VERSION" \
            -var "db_name=$DB_NAME_DEV_ENV" \
            -var "tags=$PROJECT_NAME"

        #@--- Apply the changes ---@#
        echo "+++++ Apply infrastructure ++++++++++"
        terraform apply -lock=false -auto-approve -var "cluster_name=$CLUSTER_NAME_DEV_ENV" \
            -var "cluster_region=$CLUSTER_REGION" \
            -var "kubernetes_version=$K8S_VERSION" \
            -var "node_type=$NODE_TYPE" \
            -var "max_node_number=$MAX_NODE_NUM" \
            -var "min_node_number=$MIN_NODE_NUM" \
            -var "digital_ocean_token=$SERVICE_ACCESS_TOKEN" \
            -var "db_size=$DB_SIZE" \
            -var "postgres_version=$PG_VERSION" \
            -var "db_name=$DB_NAME_DEV_ENV" \
            -var "tags=$PROJECT_NAME" \
            || echo "Resources exist"
    fi
}

#@--- Function to setup production cluster ---@#
set_up_cluster_prod() {
    if [[ $GITHUB_EVENT_NAME == "release" ]];
    then

        #@--- Initialize terraform ---@#
        echo " ----- inititalize the backend --------- "
        terraform init -lock=false -backend-config "bucket=$BACKEND_BUCKET_PROD" \
            -backend-config "key=$STATE_FILE_PROD" \
            -backend-config "access_key=$SPACES_ACCESS_KEY" \
            -backend-config "secret_key=$SPACES_SECRET_KEY"

        #@--- Run terraform command to plan infrastructure ---@#
        echo "----- show plan -------------------"
        terraform plan -lock=false -target=digitalocean_kubernetes_cluster.cluster \
             -var "cluster_name=$CLUSTER_NAME_PROD" \
            -var "cluster_region=$CLUSTER_REGION" \
            -var "kubernetes_version=$K8S_VERSION_PROD" \
            -var "node_type=$NODE_TYPE" \
            -var "max_node_number=$MAX_NODE_NUM" \
            -var "min_node_number=$MIN_NODE_NUM" \
            -var "digital_ocean_token=$SERVICE_ACCESS_TOKEN" \
            -var "db_size=$DB_SIZE" \
            -var "postgres_version=$PG_VERSION" \
            -var "db_name=$DB_NAME_PROD" \
            -var "tags=$PROJECT_NAME"

        #@--- Apply the changes ---@#
        echo "+++++ Apply infrastructure ++++++++++"
        terraform apply -lock=false -auto-approve -target=digitalocean_kubernetes_cluster.cluster \
            -var "cluster_name=$CLUSTER_NAME_PROD" \
            -var "cluster_region=$CLUSTER_REGION" \
            -var "kubernetes_version=$K8S_VERSION_PROD" \
            -var "node_type=$NODE_TYPE" \
            -var "max_node_number=$MAX_NODE_NUM" \
            -var "min_node_number=$MIN_NODE_NUM" \
            -var "digital_ocean_token=$SERVICE_ACCESS_TOKEN" \
            -var "db_size=$DB_SIZE" \
            -var "postgres_version=$PG_VERSION" \
            -var "db_name=$DB_NAME_PROD" \
            -var "tags=$PROJECT_NAME" \
            || echo "Resources exist"
    fi
}

main() {
    cd infrastructure

    set_up_cluster_dev_env
    set_up_cluster_prod
}

main
