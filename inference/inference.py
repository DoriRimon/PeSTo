import os
import sys
import torch as pt
from tqdm import tqdm
from glob import glob

sys.path.append('..')

from src.dataset import StructuresDataset, collate_batch_features
from src.data_encoding import encode_structure, encode_features, extract_topology
from src.structure import encode_bfactor, concatenate_chains, split_by_chain
from src.structure_io import save_pdb
from model import Model
from config import config_model


def load_model(model_filepath: str, device: pt.device) -> Model:
    model = Model(config_model)
    model.load_state_dict(pt.load(model_filepath, map_location=pt.device("cpu")))
    model = model.eval().to(device)
    return model


def create_dataset(data_path: str) -> StructuresDataset:
    # find pdb files and ignore already predicted oins
    pdb_filepaths = glob(os.path.join(data_path, "*.pdb"), recursive=True)
    pdb_filepaths = [fp for fp in pdb_filepaths if "_i" not in fp]

    # create dataset loader with preprocessing
    dataset = StructuresDataset(pdb_filepaths, with_preprocessing=True)
    return dataset


def inference_over_structure(model: Model, structure, device: pt.device):
    # encode structure and features
    X, M = encode_structure(structure)
    #q = pt.cat(encode_features(structure), dim=1)
    q = encode_features(structure)[0]

    # extract topology
    ids_topk, _, _, _, _ = extract_topology(X, 64)

    # pack data and setup sink (IMPORTANT)
    X, ids_topk, q, M = collate_batch_features([[X, ids_topk, q, M]])

    # run model
    z = model(X.to(device), ids_topk.to(device), q.to(device), M.float().to(device))

    return z


def inference_save_subunits(subunits, filepath, model: Model, device: pt.device):
    # concatenate all chains together
    structure = concatenate_chains(subunits)

    # inference pesto
    z = inference_over_structure(model, structure, device)
    
    # for all predictions
    for i in range(z.shape[1]):
        # prediction
        p = pt.sigmoid(z[:,i])

        # encode result
        structure = encode_bfactor(structure, p.cpu().numpy())

        # save results
        output_filepath = filepath[:-4]+'_i{}.pdb'.format(i)
        save_pdb(split_by_chain(structure), output_filepath)


def inference_save_dataset(dataset: StructuresDataset, model: Model, device: pt.device, verbose: bool):
    with pt.no_grad():
        t = tqdm(dataset, disable=(not verbose))
        for subunits, filepath in t:
            t.set_description_str(filepath)
            inference_save_subunits(subunits, filepath, model, device)
