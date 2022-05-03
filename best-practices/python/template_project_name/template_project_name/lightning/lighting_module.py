from template_project_name.network import DeepLabV3
from template_project_name.visualizer import Visualizer

import pytorch_lightning as pl
import torch
import torch.nn.functional as F
import os 
from torchmetrics import Accuracy

class LightningNet(pl.LightningModule):
    def __init__(self, exp, env):
        super().__init__()
        self._model = DeepLabV3(exp["model"])
        
        self._visualizer = Visualizer(os.path.join(exp["general"]["name"], "visu"), exp["visualizer"]["store"], self)

        self._acc = {"val": Accuracy(), "test": Accuracy(), "train" : Accuracy()}
        self._visu_count = {"val": 0, "test": 0, "train" : 0}

        self._exp = exp
        self._env = env
        self._mode = "train"
        
    def forward(self, image: torch.Tensor) -> torch.Tensor:
        return self._model(image)

    def visu(self, image, target, pred):
        if self._visu_count[self._mode] < self.exp["visualizer"]["store_n"][self._mode]:
            self._visualizer.plot_image(image, tag=f"{self._mode}_image")
            self._visualizer.plot_segmentation(pred, tag=f"{self._mode}_pred")
            self._visualizer.plot_segmentation(target, tag=f"{self._mode}_target")
            self._visu_count[self._mode] += 1
            
    # TRAINING
    def on_train_epoch_start(self):
        self._mode = "train"
        self._visu_count[self._mode] = 0

    def training_step(self, batch, batch_idx: int) -> torch.Tensor:
        image, target = batch
        output = self(image)
        
        preds = output.argmax(dim=2, keepdim=True)
        self._acc[self._mode](preds, target)
        self.log(f'{self._mode}_acc_step', self.accuracy)
        loss = F.mse_loss(output, target)
        return loss
    
    def training_epoch_end(self, outputs):
        # log epoch metric
        self.log(f'{self._mode}_acc_epoch', self.acc[self._mode])

    # VALIDATION
    def on_validation_epoch_start(self):
        self._mode = "val"
        self._visu_count[self._mode] = 0
        
    def validation_step(self, batch, batch_idx: int) -> None:
        # LAZY implementation of validation and test by calling the training method
        # Usually you want to have a different behaviour
        return self.training_step(batch, batch_idx)

    def validation_epoch_end(self, outputs):
        self.training_epoch_end(outputs)

    # TESTING 
    def on_test_epoch_start(self):
        self._mode = "test"
        self._visu_count[self._mode] = 0
        
    def test_step(self, batch, batch_idx: int) -> None:
        return self.training_step(batch, batch_idx)

    def test_epoch_end(self, outputs):
        self.training_epoch_end(outputs)

    def configure_optimizers(self) -> torch.optim.Optimizer:
        return torch.optim.Adam(self._model.parameters(), lr=self._exp["optimizer"]["lr"])
