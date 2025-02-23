import torch
from src.base.models.model import Model as GenericModel
import os
import sys
import numpy as np

from src.base.models.PeSTo.src.dataset import collate_batch_features
from src.base.models.PeSTo.src.data_encoding import encode_structure, encode_features, extract_topology


class PeSTO(GenericModel, torch.nn.Module):
    def __init__(self, model_path: str = 'src/base/models/PeSTO/model/save/i_v4_1_2021-09-07_11-21', device: str = 'cpu'):
        self.model_path = model_path
        self.device = torch.device(device)
        self.model_checkpoint_path = os.path.join(model_path, 'model_ckpt.pt')

        # add module to path
        if model_path not in sys.path:
            sys.path.insert(0, model_path)
            
        # load functions
        from config import config_model, config_data
        from data_handler import Dataset
        from model import Model

        self.model = Model(config_model)
        self.model.load_state_dict(torch.load(self.model_checkpoint_path, map_location=torch.device("cpu")))
        self.model = self.model.eval().to(self.device)


    def forward(self, structure) -> np.array:
        # structure := concatenate_chains(subunits)

        X, M = encode_structure(structure)
        q = encode_features(structure)[0]
        ids_topk, _, _, _, _ = extract_topology(X, 64)
        X, ids_topk, q, M = collate_batch_features([[X, ids_topk, q, M]])
        z = self.model(X.to(self.device), ids_topk.to(self.device), q.to(self.device), M.float().to(self.device))
        outputs = []
        for i in range(z.shape[1]):
            p = torch.sigmoid(z[:,i])
            outputs.append(p.cpu().numpy())
        return np.array(outputs)
