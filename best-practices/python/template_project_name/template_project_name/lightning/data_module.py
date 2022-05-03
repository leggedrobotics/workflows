import pytorch_lightning as pl
from torchvision import datasets
from typing import Optional
from torch.utils.data import DataLoader

class CityscapesDataModule(pl.LightningDataModule):
    def __init__(self, env: dict, cfg_dm: dict):
        super().__init__()

        self.cfg_dm = cfg_dm
        self.env = env

    def setup(self, stage: Optional[str] = None) -> None:
        self.cityscapes_test = datasets.Cityscapes(
            root=self.env["cityscapes_root"], split="test", target_type="semantic"
        )
        self.cityscapes_train = datasets.Cityscapes(
            root=self.env["cityscapes_root"], split="train", target_type="semantic"
        )
        self.cityscapes_val = datasets.Cityscapes(root=self.env["cityscapes_root"], split="val", target_type="semantic")

    def train_dataloader(self) -> DataLoader:
        return DataLoader(self.cityscapes_train, batch_size=self.cfg_dm["batch_size"], shuffle=True, pin_memory=True)

    def val_dataloader(self) -> DataLoader:
        return DataLoader(self.cityscapes_val, batch_size=self.cfg_dm["batch_size"], shuffle=False, pin_memory=True)

    def test_dataloader(self) -> DataLoader:
        return DataLoader(self.cityscapes_test, batch_size=self.cfg_dm["batch_size"], shuffle=False, pin_memory=True)
