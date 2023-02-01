#!/bin/bash

. ./path.sh || exit 1;
export CUDA_VISIBLE_DEVICES=1


python main.py  --config /mnt/data1/waris/repo/vc-vq-prosody/conf/transformer_vc_vq_prosody.yaml \
                --name=transformer-vc-vq \
                --seed=2 \
                --transvcsplinpconc

