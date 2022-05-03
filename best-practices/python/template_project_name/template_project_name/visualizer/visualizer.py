# MISC
import os
import numpy as np
import imageio
import cv2
from PIL import Image

# matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.backends.backend_agg import FigureCanvasAgg

__all__ = ["Visualizer"]


def get_img_from_fig(fig, dpi=180):
    """
    Converts matplot figure to np.array
    """

    fig.set_dpi(dpi)
    canvas = FigureCanvasAgg(fig)
    # Retrieve a view on the renderer buffer
    canvas.draw()
    buf = canvas.buffer_rgba()
    # convert to a np array
    buf = np.asarray(buf)
    buf = Image.fromarray(buf)
    buf = buf.convert("RGB")
    return buf


def image_functionality(func):
    """
    Decorator to allow for logging functionality.
    Should be added to all plotting functions of visualizer.
    The plot function has to return a np.uint8

    @image_functionality
    def plot_segmentation(self, seg, **kwargs):

        return np.zeros((H, W, 3), dtype=np.uint8)

    not_log [optional, bool, default: false] : the decorator is ignored if set to true
    epoch [optional, int, default: visualizer.epoch ] : overwrites visualizer, epoch used to log the image
    store [optional, bool, default: visualizer.store ] : overwrites visualizer, flag if image is stored to disk
    tag [optinal, str, default: tag_not_defined ] : stores image as: visulaiter._p_visu{epoch}_{tag}.png
    """

    def wrap(*args, **kwargs):
        log *= not kwargs.get("not_log", False)
        if log:
            log_exp = args[0]._pl_model.logger is not None
            tag = kwargs.get("tag", "tag_not_defined")

            if kwargs.get("store", None) is not None:
                store = kwargs["store"]
            else:
                store = args[0]._store

            if kwargs.get("epoch", None) is not None:
                epoch = kwargs["epoch"]
            else:
                epoch = args[0]._epoch

            # Store to disk
            if store:
                p = os.path.join(args[0]._p_visu, f"{epoch}_{tag}.png")
                imageio.imwrite(p, img)

            if log_exp:
                H, W, C = img.shape
                ds = cv2.resize(img, dsize=(int(W / 2), int(H / 2)), interpolation=cv2.INTER_CUBIC)
                if args[0]._pl_model.logger is not None:
                    try:
                        # logger == neptuneai
                        from neptune.new.types import File

                        args[0]._pl_model.logger.experiment[tag].log(File.as_image(np.float32(ds) / 255), step=epoch)
                    except:
                        try:
                            # logger == tensorboard
                            args[0]._pl_model.logger.experiment.add_image(
                                tag=tag,
                                img_tensor=ds,
                                global_step=epoch,
                                dataformats="HWC",
                            )
                        except:
                            print("Tensorboard Logging and Neptune Logging failed !!!")
                            pass

        return func(*args, **kwargs)

    return wrap


class Visualizer:
    def __init__(self, p_visu, cfg_visu, pl_model, epoch=0, num_classes=22):
        self._p_visu = p_visu
        self._pl_model = pl_model
        self._epoch = epoch
        self._store = cfg_visu["store"]

        if not os.path.exists(self._p_visu):
            os.makedirs(self._p_visu)

        # Used in plot functions
        jet = cm.get_cmap("jet")
        self.SEG_COLORS = (np.stack([jet(v) for v in np.linspace(0, 1, num_classes)]) * 255).astype(np.uint8)
        self.SEG_COLORS_BINARY = (np.stack([jet(v) for v in np.linspace(0, 1, 2)]) * 255).astype(np.uint8)

    @property
    def epoch(self):
        return self._epoch

    @epoch.setter
    def epoch(self, epoch):
        self._epoch = epoch

    @property
    def store(self):
        return self._store

    @store.setter
    def store(self, store):
        self._store = store

    @image_functionality
    def plot_segmentation(self, seg, **kwargs):
        try:
            seg = seg.clone().cpu().numpy()
        except:
            pass

        if seg.dtype == np.bool:
            col_map = self.SEG_COLORS_BINARY
        else:
            col_map = self.SEG_COLORS
            seg = seg.round()

        H, W = seg.shape[:2]
        img = np.zeros((H, W, 3), dtype=np.uint8)
        for i, color in enumerate(col_map):
            img[seg == i] = color[:3]

        return img

    @image_functionality
    def plot_image(self, img, **kwargs):
        """
        ----------
        img : CHW HWC accepts torch.tensor or numpy.array
              Range 0-1 or 0-255
        """
        try:
            img = img.clone().cpu().numpy()
        except:
            pass

        if img.shape[2] == 3:
            pass
        elif img.shape[0] == 3:
            img = np.moveaxis(img, [0, 1, 2], [2, 0, 1])
        else:
            raise Exception("Invalid Shape")
        if img.max() <= 1:
            img = img * 255

        img = np.uint8(img)
        return img
