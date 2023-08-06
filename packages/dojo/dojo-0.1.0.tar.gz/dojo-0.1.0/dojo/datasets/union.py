from dojo import Dataset
from dojo.transforms.union import Union


class UnionDataset(Dataset):

    def process(self, inputs):
        return Union(*inputs)
