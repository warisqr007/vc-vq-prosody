#!/usr/bin/env python
# coding: utf-8
import sys
import torch
import argparse
import numpy as np
from utils.load_yaml import HpsYaml

# For reproducibility, comment these may speed up training
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# Arguments
parser = argparse.ArgumentParser(description=
        'Training PPG2Mel VC model.')
parser.add_argument('--config', default='/mnt/data1/waris/repo/vc-vq-prosody/conf/transformer_vc_vq_prosody.yaml',
                    type=str, help='Path to experiment config, e.g., config/vc.yaml')
parser.add_argument('--name', default='debug', type=str, help='Name for logging.')
parser.add_argument('--logdir', default='log/', type=str,
                    help='Logging path.', required=False)
parser.add_argument('--ckpdir', default='ckpt/debug/', type=str,
                    help='Checkpoint path.', required=False)
parser.add_argument('--outdir', default='result/', type=str,
                    help='Decode output path.', required=False)
parser.add_argument('--load', default=None, type=str,
                    help='Load pre-trained model (for training only)', required=False)
parser.add_argument('--warm_start', action='store_true',
                    help='Load model weights only, ignore specified layers.')
parser.add_argument('--seed', default=2, type=int,
                    help='Random seed for reproducable results.', required=False)
parser.add_argument('--njobs', default=8, type=int,
                    help='Number of threads for dataloader/decoding.', required=False)
parser.add_argument('--cpu', action='store_true', help='Disable GPU training.')
parser.add_argument('--no-pin', action='store_true',
                    help='Disable pin-memory for dataloader')
parser.add_argument('--test', action='store_true', help='Test the model.')
parser.add_argument('--no-msg', action='store_true', help='Hide all messages.')
parser.add_argument('--finetune', action='store_true', help='Finetune model')
parser.add_argument('--oneshotvc', action='store_true', help='Oneshot VC model')
parser.add_argument('--ownarc', action='store_true', help='Oneshot VC model')
parser.add_argument('--bilstm', action='store_true', help='BiLSTM VC model')
parser.add_argument('--lsa', action='store_true', help='Use location-sensitive attention (LSA)')
parser.add_argument('--transvc', action='store_true', help='BiLSTM VC model')
parser.add_argument('--transvcspdloss', action='store_true', help='BiLSTM VC model')
parser.add_argument('--transvcspdlossmel', action='store_true', help='BiLSTM VC model')
parser.add_argument('--transvcsplinpconc', action='store_true', help='Transformer VC model')


# ###
# paras = {
#     'config' : '/mnt/data1/waris/repo/vc-vq-prosody/conf/transformer_vc_vq_prosody.yaml',
#     'name': 'transformer-vc-vq-dr',
#     'logdir': 'log/',
#     'ckpdir' : 'ckpt/',
#     'outdir':'result/',
#     'load':None,
#     'warm_start':True,
#     'seed': 2,
#     'njobs':8,
#     'cpu':True,
#     'no-pin':True,
#     'test':True,
#     'no-msg':True,
#     'finetune':'',
# }
# ###

paras = parser.parse_args()
setattr(paras, 'gpu', not paras.cpu)
setattr(paras, 'pin_memory', not paras.no_pin)
setattr(paras, 'verbose', not paras.no_msg)
# Make the config dict dot visitable
config = HpsYaml(paras.config) # yaml.load(open(paras.config, 'r'), Loader=yaml.FullLoader)

np.random.seed(paras.seed)
torch.manual_seed(paras.seed)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(paras.seed)
# For debug use
# torch.autograd.set_detect_anomaly(True)

# Hack to preserve GPU ram just in case OOM later on server
# if paras.gpu and paras.reserve_gpu > 0:
    # buff = torch.randn(int(paras.reserve_gpu*1e9//4)).cuda()
    # del buff


from bin.train_ppg2mel_own_arctic_transformer_speaker_loss_from_inpconct import Solver
mode = "train"
solver = Solver(config, paras, mode)
solver.load_data()
solver.set_model()
solver.exec()
print(">>> Oneshot VC train finished!")
sys.exit(0)
