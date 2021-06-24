import time

class Samples:
    # Generator
    def __init__(self, sampleList=[]):
        start_timer = time.perf_counter()
        self.samples = {}
        for sample in sampleList:
            self.add_sample(sample)
        self.number = len(sampleList)
        stop_timer = time.perf_counter()
        print(f'Initiated Samples object with {self.number} samples in {stop_timer-start_timer:0.4f} seconds')

    # Class methods
    def add_sample(self, sample):
        self.samples[sample.get_name()] = sample
        self.number =+ 1 
    
    def add_samples(self, sampleList):
        for sample in sampleList:
            self.add_sample(sample)
        self.number = len(sampleList)

    def get_sample(self, name):
        return self.samples[name]
    
    def get_samples(self):
        return self.samples

    def get_names(self):
        return self.samples.keys()

    def get_size(self):
        return self.number

