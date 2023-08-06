import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import LabelEncoder
from torch.autograd import Variable
import torch.optim as optim
import torch.nn.functional as F
import random

from torch.utils.data import Dataset, DataLoader

from languageflow.transformer.word_vector import WordVectorTransformer

USE_CUDA = torch.cuda.is_available()
USE_CUDA = False

FloatTensor = torch.cuda.FloatTensor if USE_CUDA else torch.FloatTensor
LongTensor = torch.cuda.LongTensor if USE_CUDA else torch.LongTensor
ByteTensor = torch.cuda.ByteTensor if USE_CUDA else torch.ByteTensor


class TextCNN(nn.Module):
    def __init__(self, vocab_size, embedding_dim, output_size, n_kernel=100,
                 kernel_sizes=[3, 4, 5], dropout=0.5):
        super(TextCNN, self).__init__()

        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.convs = nn.ModuleList(
            [nn.Conv2d(1, n_kernel, (k, embedding_dim)) for k in
             kernel_sizes])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(len(kernel_sizes) * n_kernel, output_size)

    def init_weights(self, pretrained_word_vectors, is_static=False):
        self.embedding.weight = nn.Parameter(
            torch.from_numpy(pretrained_word_vectors).float())
        if is_static:
            self.embedding.weight.requires_grad = False

    def forward(self, x, is_training=False):
        # (B,1,T,D)
        x = self.embedding(x).unsqueeze(1)
        # [(N,Co,W), ...]*len(Ks)
        x = [F.relu(conv(x)).squeeze(3) for conv in self.convs]
        x = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in
             x]  # [(N,Co), ...]*len(Ks)

        concated = torch.cat(x, 1)

        if is_training:
            concated = self.dropout(concated)  # (N,len(Ks)*Co)
        y = self.fc(concated)
        # y = F.softmax(y)
        return y


class CategorizedDataset(Dataset):
    def __getitem__(self, index):
        return self.X[index], self.y[index]

    def __len__(self):
        return len(y)

    def __init__(self, X, y):
        self.X = X
        self.y = y


class KimCNNClassifier():
    def fit(self, X, y):
        ####################
        # Data Loader
        ####################
        word_vector_transformer = WordVectorTransformer(padding='max')
        X = word_vector_transformer.fit_transform(X)
        X = LongTensor(X)
        self.word_vector_transformer = word_vector_transformer

        y_transformer = LabelEncoder()
        y = y_transformer.fit_transform(y)
        y = torch.from_numpy(y)
        self.y_transformer = y_transformer

        dataset = CategorizedDataset(X, y)
        dataloader = DataLoader(dataset, batch_size=2, shuffle=True,
                                num_workers=4)

        ####################
        # Model
        ####################
        BATCH_SIZE = 50
        KERNEL_SIZES = [3, 4, 5]
        KERNEL_DIM = 100
        model = TextCNN(
            vocab_size=word_vector_transformer.get_vocab_size(),
            embedding_dim=5,
            output_size=3)
        if USE_CUDA:
            model = model.cuda()

        ####################
        # Train
        ####################
        EPOCH = 50
        LR = 0.001

        loss_function = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=LR)

        for epoch in range(EPOCH):
            losses = []
            for i, data in enumerate(dataloader):
                X, y = data
                X, y = Variable(X), Variable(y)

                optimizer.zero_grad()
                model.train()
                output = model(X)

                loss = loss_function(output, y)
                losses.append(loss.data.tolist()[0])
                loss.backward()

                optimizer.step()

                if i % 100 == 0:
                    print("[%d/%d] mean_loss : %0.2f" % (
                        epoch, EPOCH, np.mean(losses)))
                    losses = []
        self.model = model

    def predict(self, X):
        x = self.word_vector_transformer.transform(X)
        x = Variable(LongTensor(x))
        y = self.model(x)
        y = torch.max(y, 1)[1].data.numpy()
        y = self.y_transformer.inverse_transform(y)
        return y


X = [
    "đồ ăn tốt",
    "món ăn thực sự rất ngon",
    "ngon thật",
    "giá rẻ",
    # NEGATIVE
    "chán cực kì",
    "phục vụ chán quá",
    "đồ uống chán lắm",
    "vệ sinh bẩn",
    "phục vụ còn quá kém",
    # NEUTRAL
    "cũng bình thường"
]
y = ["POSITIVE", "POSITIVE", "POSITIVE", "POSITIVE",
     "NEGATIVE", "NEGATIVE", "NEGATIVE", "NEGATIVE", "NEGATIVE",
     "NEUTRAL"]

estimator = KimCNNClassifier()
estimator.fit(X, y)

X_test = [
    "chán",
    "tốt quá",
    "vệ sinh",
    "vệ sinh bẩn",
    "bẩn",
    "tôi thấy thái độ của nhân viên không tốt",
    "quán này rẻ nè"
]
y_pred = estimator.predict(X_test)
print("Test results")
for i, x in enumerate(X_test):
    print("{} -> {}".format(x, y_pred[i]))

print(estimator.predict(X))
