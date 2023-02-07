#!/bin/bash

. ./path.sh || exit 1;
export CUDA_VISIBLE_DEVICES=1


# python main.py  --config /mnt/data1/waris/repo/vc-vq-prosody/conf/transformer_vc_vq_prosody.yaml \
#                 --name=transformer-vc-vq-dr \
#                 --seed=2 \
#                 --transvcsplinpconc



python main.py  --config /mnt/data1/waris/repo/vc-vq-prosody/conf/transformer_vc_vq_prosody_v2.yaml \
                --name=transformer-vc-vq-dr-v2 \
                --seed=2 \
                --transvcsplinpconc