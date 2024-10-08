from .cifar import CIFAR10, CIFAR100, CIFAR_C
from .image_list import ImageList
from .imagenet import ImageNet
from .mnist import MNIST, FMNIST, KMNIST, USPS
from .cars import Cars
from .standford_dogs import Stanford_Dogs

__all__ = [
    'CIFAR10', 'CIFAR100', 'CIFAR_C',
    'ImageList', 'ImageNet',
    'MNIST', 'FMNIST', 'KMNIST', 'USPS',
    'Cars', 'Stanford_Dogs',
]
