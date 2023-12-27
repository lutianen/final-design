#!/bin/bash

# !!! Select right project prefix and data dir
# ArchLinux (My PC)
# PROJECT_PREFIX=/home/tianen/doc/_XiDian/___FinalDesign/FinalDesign/final-design
# DATA_DIR=/home/tianen/doc/MachineLearningData/
# Ubuntu Server
PROJECT_PREFIX=/home/lutianen/final-design
DATA_DIR=/home/lutianen/data/

DIST_TYPE=${1}

# !!! Set dist type: [abs, l1, gcc, knn]
# RUN Command
# nohup ./scripts/train_resnet_cifar.sh abs > resnet_cifar10.out &

# 10 30 50 70 90 100
for i in 0.1 0.033 0.02 0.014 0.011 0.01
do
    echo ${i}
    echo ${DIST_TYPE1}
    python ${PROJECT_PREFIX}/train_cifar.py \
        --data_path ${DATA_DIR} \
        --dataset CIFAR \
        --arch resnet_cifar \
        --cfg resnet56 \
        --num_batches_per_step 2 \
        --train_batch_size 256 \
        --eval_batch_size 100 \
        --num_epochs 200 \
        --job_dir ${PROJECT_PREFIX}/experiments/ \
        --momentum 0.9 \
        --lr 0.1 \
        --lr_type step \
        --lr_decay_step 50 100 150 \
        --weight_decay 5e-3 \
        --cr ${i} \
        --gpus 2 \
        --dist_type ${DIST_TYPE}\
        --warmup_epochs 0
done
