import argparse
import math
import pkg_resources
import re
import mmcv
import numpy as np

from pathlib import Path
from PIL import Image
from mmcv import Config, DictAction
from mmcv.runner import load_checkpoint
from mmcv.utils import to_2tuple
from torch.nn import BatchNorm1d, BatchNorm2d, GroupNorm, LayerNorm
from torchvision.transforms import Compose

from openmixup import digit_version
from openmixup.datasets.registry import PIPELINES
from openmixup.models import build_model
from openmixup.utils import build_from_cfg

try:
    from pytorch_grad_cam import (EigenCAM, EigenGradCAM, GradCAM,
                                  GradCAMPlusPlus, LayerCAM, XGradCAM)
    from pytorch_grad_cam.activations_and_gradients import \
        ActivationsAndGradients
    from pytorch_grad_cam.utils.image import show_cam_on_image
except ImportError:
    raise ImportError('Please run `pip install "grad-cam>=1.3.6"` to install '
                      '3rd party package pytorch_grad_cam.')

# set of transforms, which just change data format, not change the pictures
FORMAT_TRANSFORMS_SET = {'ToTensor', 'Normalize',}

# Supported grad-cam type map
METHOD_MAP = {
    'gradcam': GradCAM,
    'gradcam++': GradCAMPlusPlus,
    'xgradcam': XGradCAM,
    'eigencam': EigenCAM,
    'eigengradcam': EigenGradCAM,
    'layercam': LayerCAM,
}


def parse_args():
    parser = argparse.ArgumentParser(description='Visualize CAM')
    parser.add_argument('-img', default='/home/jinxin/桌面/openmixup/SUMix_vis/n02123045_12779.JPEG', help='Image file')
    parser.add_argument('-config', default='/home/jinxin/桌面/openmixup/configs/classification/imagenet/mixups/basic/r18_mixups_CE_none_4xb64.py', help='Config file')
    parser.add_argument('-checkpoint', default='/home/jinxin/桌面/openmixup/work_dirs/imagenet1k_r18/r18_cutmix_a0_2_CE_none_4xb64_cos_ep100.pth',
                        help='Checkpoint file')
    parser.add_argument(
        '--target-layers',
        default=[],
        nargs='+',
        type=str,
        help='The target layers to get CAM, if not set, the tool will '
        'specify the norm layer in the last block. Backbones '
        'implemented by users are recommended to manually specify'
        ' target layers in commmad statement.')
    parser.add_argument(
        '--preview-model',
        default=False,
        action='store_true',
        help='To preview all the model layers')
    parser.add_argument(
        '--method',
        default='gradcam++',
        help='Type of method to use, supports '
        f'{", ".join(list(METHOD_MAP.keys()))}.')
    parser.add_argument(
        '--target-category',
        default=[281],
        nargs='+',
        type=int,
        help='The target category to get CAM, default to use result '
        'get from given model.')
    parser.add_argument(
        '--eigen-smooth',
        default=False,
        action='store_true',
        help='Reduce noise by taking the first principle componenet of '
        '``cam_weights*activations``')
    parser.add_argument(
        '--aug-smooth',
        default=False,
        action='store_true',
        help='Wether to use test time augmentation, default not to use')
    parser.add_argument(
        '--save-path',
        type=Path,
        default='tools/vis_cutmix_281_wo.png',
        help='The path to save visualize cam image, default not to save.')
    parser.add_argument('--device', default='cpu', help='Device to use cpu')
    parser.add_argument(
        '--vit-like',
        action='store_true',
        help='Whether the network is a ViT-like network.')
    parser.add_argument(
        '--num-extra-tokens',
        type=int,
        help='The number of extra tokens in ViT-like backbones. Defaults to'
        ' use num_extra_tokens of the backbone.')
    parser.add_argument(
        '--cfg-options',
        nargs='+',
        action=DictAction,
        help='override some settings in the used config, the key-value pair '
        'in xxx=yyy format will be merged into config file. If the value to '
        'be overwritten is a list, it should be like key="[a,b]" or key=a,b '
        'It also allows nested list/tuple values, e.g. key="[(a,b),(c,d)]" '
        'Note that the quotation marks are necessary and that no white space '
        'is allowed.')
    args = parser.parse_args()
    if args.method.lower() not in METHOD_MAP.keys():
        raise ValueError(f'invalid CAM type {args.method},'
                         f' supports {", ".join(list(METHOD_MAP.keys()))}.')

    return args


def build_reshape_transform(model, args):
    """Build reshape_transform for `cam.activations_and_grads`, which is
    necessary for ViT-like networks."""
    # ViT_based_Transformers have an additional clstoken in features
    if not args.vit_like:

        def check_shape(tensor):
            assert len(tensor.size()) != 3, \
                (f"The input feature's shape is {tensor.size()}, and it seems "
                 'to have been flattened or from a vit-like network. '
                 "Please use `--vit-like` if it's from a vit-like network.")
            return tensor

        return check_shape

    if args.num_extra_tokens is not None:
        num_extra_tokens = args.num_extra_tokens
    elif hasattr(model.backbone, 'num_extra_tokens'):
        num_extra_tokens = model.backbone.num_extra_tokens
    else:
        num_extra_tokens = 1

    def _reshape_transform(tensor):
        """reshape_transform helper."""
        assert len(tensor.size()) == 3, \
            (f"The input feature's shape is {tensor.size()}, "
             'and the feature seems not from a vit-like network?')
        tensor = tensor[:, num_extra_tokens:, :]
        # get heat_map_height and heat_map_width, preset input is a square
        heat_map_area = tensor.size()[1]
        height, width = to_2tuple(int(math.sqrt(heat_map_area)))
        assert height * height == heat_map_area, \
            (f"The input feature's length ({heat_map_area+num_extra_tokens}) "
             f'minus num-extra-tokens ({num_extra_tokens}) is {heat_map_area},'
             ' which is not a perfect square number. Please check if you used '
             'a wrong num-extra-tokens.')
        result = tensor.reshape(tensor.size(0), height, width, tensor.size(2))

        # Bring the channels to the first dimension, like in CNNs.
        result = result.transpose(2, 3).transpose(1, 2)
        return result

    return _reshape_transform


def apply_transforms(img_path, pipeline_cfg):
    """Apply transforms pipeline and get formatted data."""

    def split_pipeline_cfg(pipeline_cfg):
        """to split the transfoms into image_transforms and
        format_transforms."""
        image_transforms_cfg, format_transforms_cfg = [], []
        for transform in pipeline_cfg:
            if transform['type'] in FORMAT_TRANSFORMS_SET:
                format_transforms_cfg.append(transform)
            else:
                image_transforms_cfg.append(transform)
        return image_transforms_cfg, format_transforms_cfg

    image_transforms, format_transforms = split_pipeline_cfg(pipeline_cfg)
    image_transforms = Compose([
        build_from_cfg(p, PIPELINES) for p in image_transforms])
    format_transforms = Compose([
        build_from_cfg(p, PIPELINES) for p in format_transforms])

    img = Image.open(img_path)
    img = img.convert('RGB')
    img = image_transforms(img)
    format_img = format_transforms(img)

    return (format_img, img)


class MMActivationsAndGradients(ActivationsAndGradients):
    """Activations and gradients manager for mmcls models."""

    def __call__(self, x):
        self.gradients = []
        self.activations = []
        results = self.model(x, mode='test')
        # print(results["head0"])
        # results["head0"] = results["head0"] + 0.5 * results["head1"]
        # assert len(results) == 1
        return list(results.values())[0]

def init_cam(method, model, target_layers, use_cuda, reshape_transform):
    """Construct the CAM object once, In order to be compatible with mmcls,
    here we modify the ActivationsAndGradients object."""

    GradCAM_Class = METHOD_MAP[method.lower()]
    cam = GradCAM_Class(
        model=model, target_layers=target_layers, use_cuda=use_cuda)
    # Release the original hooks in ActivationsAndGradients to use
    # MMActivationsAndGradients.
    cam.activations_and_grads.release()
    cam.activations_and_grads = MMActivationsAndGradients(
        cam.model, cam.target_layers, reshape_transform)

    return cam


def get_layer(layer_str, model):
    """get model layer from given str."""
    cur_layer = model
    layer_names = layer_str.strip().split('.')

    def get_children_by_name(model, name):
        try:
            return getattr(model, name)
        except AttributeError as e:
            raise AttributeError(
                e.args[0] +
                '. Please use `--preview-model` to check keys at first.')

    def get_children_by_eval(model, name):
        try:
            return eval(f'model{name}', {}, {'model': model})
        except (AttributeError, IndexError) as e:
            raise AttributeError(
                e.args[0] +
                '. Please use `--preview-model` to check keys at first.')

    for layer_name in layer_names:
        match_res = re.match('(?P<name>.+?)(?P<indices>(\\[.+\\])+)',
                             layer_name)
        if match_res:
            layer_name = match_res.groupdict()['name']
            indices = match_res.groupdict()['indices']
            cur_layer = get_children_by_name(cur_layer, layer_name)
            cur_layer = get_children_by_eval(cur_layer, indices)
        else:
            cur_layer = get_children_by_name(cur_layer, layer_name)

    return cur_layer


def show_cam_grad(grayscale_cam, src_img, title, out_path=None):
    """fuse src_img and grayscale_cam and show or save."""
    grayscale_cam = grayscale_cam[0, :]
    src_img = np.float32(src_img) / 255
    visualization_img = show_cam_on_image(
        src_img, grayscale_cam, use_rgb=False)

    if out_path:
        mmcv.imwrite(visualization_img, str(out_path))
    else:
        mmcv.imshow(visualization_img, win_name=title)


def get_default_traget_layers(model, args):
    """get default target layers from given model, here choose nrom type layer
    as default target layer."""
    norm_layers = []
    for m in model.backbone.modules():
        if isinstance(m, (BatchNorm2d, LayerNorm, GroupNorm, BatchNorm1d)):
            norm_layers.append(m)
    if len(norm_layers) == 0:
        raise ValueError(
            '`--target-layers` is empty. Please use `--preview-model`'
            ' to check keys at first and then specify `target-layers`.')
    # if the model is CNN model or Swin model, just use the last norm
    # layer as the target-layer, if the model is ViT model, the final
    # classification is done on the class token computed in the last
    # attention block, the output will not be affected by the 14x14
    # channels in the last layer. The gradient of the output with
    # respect to them, will be 0! here use the last 3rd norm layer.
    # means the first norm of the last decoder block.
    if args.vit_like:
        if args.num_extra_tokens:
            num_extra_tokens = args.num_extra_tokens
        elif hasattr(model.backbone, 'num_extra_tokens'):
            num_extra_tokens = model.backbone.num_extra_tokens
        else:
            raise AttributeError('Please set num_extra_tokens in backbone'
                                 " or using 'num-extra-tokens'")

        # if a vit-like backbone's num_extra_tokens bigger than 0, view it
        # as a VisionTransformer backbone, eg. DeiT, T2T-ViT.
        if num_extra_tokens >= 1:
            print('Automatically choose the last norm layer before the '
                  'final attention block as target_layer..')
            return [norm_layers[-3]]
    print('Automatically choose the last norm layer as target_layer.')
    target_layers = [norm_layers[-1]]
    return target_layers


def main():
    args = parse_args()
    cfg = Config.fromfile(args.config)
    if args.cfg_options is not None:
        cfg.merge_from_dict(args.cfg_options)

    # build the model from a config file and a checkpoint file
    model = build_model(cfg.model)
    if args.checkpoint is not None:
        # Mapping the weights to GPU may cause unexpected video memory leak
        # which refers to https://github.com/open-mmlab/mmdetection/pull/6405
        load_checkpoint(model, args.checkpoint, map_location='cpu')
    model.to(args.device)
    model.eval()

    if args.preview_model:
        print(model)
        print('\n Please remove `--preview-model` to get the CAM.')
        return

    # apply transform and perpare data
    format_img, src_img = apply_transforms(args.img, cfg.data.val.pipeline)

    # build target layers
    if args.target_layers:
        target_layers = [
            get_layer(layer, model) for layer in args.target_layers
        ]
    else:
        target_layers = get_default_traget_layers(model, args)

    # init a cam grad calculator
    use_cuda = ('cuda' in args.device)
    reshape_transform = build_reshape_transform(model, args)
    cam = init_cam(args.method, model, target_layers, use_cuda,
                   reshape_transform)

    # warp the target_category with ClassifierOutputTarget in grad_cam>=1.3.7,
    # to fix the bug in #654.
    targets = None
    if args.target_category:
        grad_cam_v = pkg_resources.get_distribution('grad_cam').version
        if digit_version(grad_cam_v) >= digit_version('1.3.7'):
            from pytorch_grad_cam.utils.model_targets import \
                ClassifierOutputTarget
            targets = [ClassifierOutputTarget(c) for c in args.target_category]
        else:
            targets = args.target_category

    # calculate cam grads and show|save the visualization image
    grayscale_cam = cam(
        format_img.unsqueeze(0),
        targets,
        eigen_smooth=args.eigen_smooth,
        aug_smooth=args.aug_smooth)
    show_cam_grad(
        grayscale_cam, src_img, title=args.method, out_path=args.save_path)


if __name__ == '__main__':
    main()
