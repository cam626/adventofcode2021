class Digit():
    def __init__(self, onWires):
        self.onWires = set(onWires)
        self.numSegmentsOn = len(onWires)
        self.digit = None

        if self.numSegmentsOn == 2:
            self.digit = 1
        elif self.numSegmentsOn == 3:
            self.digit = 7
        elif self.numSegmentsOn == 4:
            self.digit = 4
        elif self.numSegmentsOn == 7:
            self.digit = 8

    def __str__(self):
        return str(self.digit)

    def __repr__(self):
        return str(self.digit)