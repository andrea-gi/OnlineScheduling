class Job:
    def __init__(self, i, a, d, f):
        self.i = i
        self.a = a
        self.d = d
        self.f = f

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Job):
            return self.a == other.a and self.d == other.d and self.f == other.f
        return False

    