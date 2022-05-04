from torchvision.datasets import Cityscapes as TVCityscapes
import torch
import torchvision
import numpy as np
from torchvision.transforms.functional import InterpolationMode


class Cityscapes(torch.utils.data.Dataset):
    def __init__(self, root, split, target_type):
        super(Cityscapes, self).__init__()

        self.dataset_default = TVCityscapes(root=root, split=split, target_type=target_type)

        self.resize_image = torchvision.transforms.Resize(size=(240, 320), interpolation=InterpolationMode.BILINEAR)
        self.resize_label = torchvision.transforms.Resize(size=(240, 320), interpolation=InterpolationMode.NEAREST)

        self.normalize = torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

        self.pil_to_torch = torchvision.transforms.ToTensor()

    def __len__(self):
        return len(self.dataset_default)

    def __getitem__(self, index):
        # convert to torch tensor
        el = self.dataset_default[index]
        ori_image = self.resize_image(self.pil_to_torch(el[0]))  # CxHxW , float32

        image = self.normalize(ori_image.clone())
        label = self.resize_label(torch.from_numpy(np.array(el[1])).type(torch.long)[None])  # 1xHxW, int32

        return (image, label, ori_image)
