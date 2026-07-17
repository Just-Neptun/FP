import csv

class DataWriter:
    def __init__(
        self,
        loc: str,
        cols: list[str],
        metadata: str | None = None
    ):
        self.cols = cols
        self.loc = loc
        self.metadata = str(metadata)
        self.write_metadata()
        self.write({key: key for key in self.cols})

    def write(self, row: dict):
        if not (self.cols == list(row.keys())):
            raise ValueError(f"Tried to write an invalid row: {row}.\nExpected keys: {self.cols}")
        with open(self.loc, 'a', newline='') as file:
            writer = csv.DictWriter(file, self.cols, delimiter=',')
            writer.writerow(row)

    def write_metadata(self):
        with open(self.loc, 'a', newline='') as file:
            file.write(self.metadata + "\n")

    def reset(self, confirm: bool):
        if not confirm:
            raise RuntimeError()
        with open(self.loc, 'w', newline='') as file:
            file.write("")
        self.write_metadata()
        self.write(self.cols)