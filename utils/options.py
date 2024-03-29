import argparse

# !!! Select right project prefix and data dir
# ArchLinux (My PC)
# PROJECT_PREFIX=/home/tianen/doc/_XiDian/___FinalDesign/code/final-design-tianen
# DATA_DIR=/home/tianen/doc/MachineLearningData/
# Ubuntu Server
PROJECT_PREFIX = "/home/lutianen/code/final-design"
DATA_DIR = "/home/lutianen/data/"

parser = argparse.ArgumentParser(description='final-design-tianen')

parser.add_argument(
    '--data_path',
    type=str,
    default=DATA_DIR,
    help='The dictionary where the input is stored. default:/home/lutianen/data/',
)

parser.add_argument(
    '--dataset',
    type=str,
    default='CIFAR',
    help='Select dataset to train. default:CIFAR',
)

parser.add_argument(
    '--arch',
    type=str,
    default='resnet',
    help='Architecture of model. default:resnet'
)

parser.add_argument(
    '--cfg',
    type=str,
    default='resnet56',
    help='Detail architecuture of model. default:resnet56'
)

parser.add_argument(
    '--pretrain_model',
    type=str,
    default=None,
    help='Path to the pretrain model . default:None'
)

parser.add_argument(
    '--num_batches_per_step',
    type=int,
    default=1,
    help="num of batches per step"
)

parser.add_argument(
    '--train_batch_size',
    type=int,
    default=256,
    help='Batch size for training. default:256'
)

parser.add_argument(
    '--eval_batch_size',
    type=int,
    default=100,
    help='Batch size for validation. default:100'
)

parser.add_argument(
    '--num_epochs',
    type=int,
    default=160,
    help='The num of epochs to train. default:160'
)

parser.add_argument(
    '--resume',
    type=str,
    default=None,
    help='Continue training from last epoch, keep all traning configurations as before.'
)

parser.add_argument(
    '--job_dir',
    type=str,
    default='experiments/',
    help='The directory where the summaries will be stored. default:./experiments'
)

parser.add_argument(
    '--momentum',
    type=float,
    default=0.9,
    help='Momentum for MomentumOptimizer. default:0.9')

parser.add_argument(
    '--lr',
    type=float,
    default=1e-2,
    help='Learning rate for train. default:1e-2'
)

parser.add_argument(
    '--lr_type',
    default='step', 
    type=str, 
    help='lr scheduler (step/exp/cos/step3/fixed)'
)

parser.add_argument(
    '--lr_decay_step',
    type=int,
    nargs='+',
    default=[50, 100],
    help='the iterval of learn rate. default:50, 100'
)

parser.add_argument(
    '--weight_decay',
    type=float,
    default=5e-3,
    help='The weight decay of loss. default:5e-3'
)

parser.add_argument(
    '--cr',
    type=float,
    default=0.5,
    help='Prune target of the parameters. default:50%'
)

parser.add_argument(
    '--gpus',
    type=int,
    nargs='+',
    default=[0],
    help='Select gpu_id to use. default:[0]',
)

parser.add_argument(
    "--dist_type",
    type=str,
    default="abs",
    choices=["base_line", "abs", "gcc", "l1", "knn", "random"],
    help="distance type of importance",
)

parser.add_argument(
    '--eval',
    type=bool,
    default=False,
    help='Evaluate the model. default:False',
)

parser.add_argument(
    '--bands',
    type=int,
    default=0,
    help='The num of bands of input data for HTD. default:0',
)

parser.add_argument(
    '--hidden_dim',
    type=int,
    default=50,
    help='The hidden dim of model for HTD. default:50',
)

parser.add_argument(
    '--warmup_epochs',
    type=int,
    default=5,
    help='Warmup epochs. default:5',
)

parser.add_argument(
    '--warmup_coeff',
    type=int,
    nargs="*",
    default=[1, 1, 1, 1, 1],
    help='Warmup coeff. default:[1, 1, 1, 1, 1]',
)
