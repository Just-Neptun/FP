from torch import nn


class Neural_Network(nn.Module):
    def __init__(self):
        super().__init__()
        # ----- input -----
        # batch *  3 * 64 * 64
        self.conv_layers = nn.Sequential(
            nn.Conv2d(
                in_channels=3,
                out_channels=32,
                kernel_size=3,
                stride=1,
                padding=1
            ),
            nn.ReLU(),
            # batch * 32 * 64 * 64
            nn.MaxPool2d(
                kernel_size=2,
                stride=2
            ),
            # batch * 32 * 32 * 32
            nn.Conv2d(
                in_channels=32,
                out_channels=64,
                kernel_size=3,
                stride=1,
                padding=1
            ),
            nn.ReLU(),
            # batch * 64 * 32 * 32
            nn.MaxPool2d(
                kernel_size=2,
                stride=2
            )
            # batch * 64 * 16 * 16
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            # batch * (64 * 16 * 16)
            nn.Linear(64 * 16 * 16, 128),
            # batch * 128
            nn.ReLU(),
            nn.Linear(128, 4)
            # batch * 4
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.classifier(x)
        return x
