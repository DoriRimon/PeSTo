import os, sys
import argparse
from .logging_utils import logger
import os
import sys
import torch as pt


parser=argparse.ArgumentParser()
parser.add_argument("--data_path", help="Path to data")
parser.add_argument("--model_path", help="Path to model")
parser.add_argument("--device", help="cpu / cuda / cuda:<index>")
args=parser.parse_args()

logger.info('Bootstrapping', extra={'data_path': args.data_path,
                                    'model_path': args.model_path,
                                    'device': args.device})


model_filepath = os.path.join(args.model_path, 'model_ckpt.pt')

# add module to path
if args.model_path not in sys.path:
    sys.path.insert(0, args.model_path)


from .inference import load_model, create_dataset, inference_save_dataset
device = pt.device(args.device)

logger.info('Loading model')
model = load_model(model_filepath, device)

logger.info('Loading dataset')
dataset = create_dataset(args.data_path)

logger.info('Starting to inference PeSTO over dataset')
inference_save_dataset(dataset, model, device, verbose=True)
logger.info('Finished PeSTO extraction and saving successfuly')
