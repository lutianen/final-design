#!/bin/bash

# !!! Select right project prefix and data dir
# ArchLinux (My PC)
# PROJECT_PREFIX=/home/tianen/doc/_XiDian/___FinalDesign/FinalDesign/final_design
# DATA_DIR=/home/tianen/doc/MachineLearningData/
# Ubuntu Server
PROJECT_PREFIX=/home/lutianen/final-design
DATA_DIR=/home/lutianen/data/

# nohup ./scripts/train_vgg_cifar_wm5o.sh > train_vgg_cifar_wm5o.out &

# 10 30 50 70 90 100
for i in 0.1 0.033 0.02 0.014 0.011 0.01
do
    echo ${i}
    python ${PROJECT_PREFIX}/train_cifar.py \
            --data_path ${DATA_DIR} \
            --dataset CIFAR \
            --arch vgg_cifar \
            --cfg vgg16 \
            --pretrain_model ${PROJECT_PREFIX}/pretrain_model/vgg16_cifar10.pt \
            --num_batches_per_step 3 \
            --train_batch_size 128 \
            --eval_batch_size 100 \
            --num_epochs 200 \
            --job_dir ${PROJECT_PREFIX}/experiments/ \
            --momentum 0.9 \
            --lr 0.01 \
            --lr_type step \
            --lr_decay_step 50 100 150 \
            --weight_decay 5e-3 \
            --cr ${i} \
            --gpus 1 \
            --dist_type gcc \
            --warmup_epochs 5 \
            --warmup_coeff 1 1 1 1 1
done
