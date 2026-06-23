from torch import nn


class Neural_Network(nn.Module):
    def __init__(self):
        super().__init__()
        # ----- input -----
        # batch *  3 * 64 * 64
        # ----- conv_layers -----
        # nn.Conv2d:
        # batch * 32 * 64 * 64
        # nn.Conv2d:
        # batch * 64 * 64 * 64
        # ----- classifier -----
        # flatten:
        # batch * (64 * 64 * 64)
        # linear:
        # batch * 128
        # linear:
        # batch *   4
        self.conv_layers = nn.Sequential(
            nn.Conv2d(
                in_channels=3,
                out_channels=32,
                kernel_size=3,
                stride=1,
                padding=1
            ),
            nn.ReLU(),
            nn.MaxPool2d(
                kernel_size=2,
                stride=2
            ),
            nn.Conv2d(
                in_channels=32,
                out_channels=64,
                kernel_size=3,
                stride=1,
                padding=1
            ),
            nn.ReLU(),
            nn.MaxPool2d(
                kernel_size=2,
                stride=2
            )
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(64 * 64 * 64, 128),
            nn.ReLU(),
            nn.Linear(128, 4)
        )

    def forward(self, x):
        x = self.conv_layers(x)
        x = self.classifier(x)
        return x
