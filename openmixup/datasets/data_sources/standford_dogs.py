import os
from PIL.Image import Image
from scipy.io import loadmat
from torch.utils.data import Dataset


class Stanford_Dogs(Dataset):
    '''
    Stanford_Dog Dataset for image retrieval
    '''
    def __init__(self,
                 root,
                 split,
                 return_label=True,
                 ):
        assert split in ['train', 'test']
        self.root = root
        self.split = split
        self.return_label = return_label

        if self.split == 'train':
            self.images = [image[0][0] for image in loadmat(os.path.join(root, 'train_list.mat'))['file_list']]
            self.labels = [(int(image[0]) - 1) for image in loadmat(os.path.join(root, 'train_list.mat'))['labels']]
            assert len(self.images) == len(self.labels) == 12000
        else:
            self.images = [image[0][0] for image in loadmat(os.path.join(root, 'test_list.mat'))['file_list']]
            self.labels = [(int(image[0]) - 1) for image in loadmat(os.path.join(root, 'test_list.mat'))['labels']]
            assert len(self.images) == len(self.labels) == 8580

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        imagename = self.images[idx]
        label = self.labels[idx]
        image = Image.open(os.path.join(self.root, 'Images', imagename)).convert('RGB')

        return image, label