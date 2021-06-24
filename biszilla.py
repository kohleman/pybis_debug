#!/usr/bin/env python3

# Import
import argparse
from obis_connect import *

# Read command line arguments

def main():

    ###########
    # OpenBIS #
    ###########
    # Open session
    openSession('minimal/credentials.txt')

    # Get samples
    # samples = getSamples()
    # obis_IDs = samples.get_names()
    number = 10

    createBatchSamples(number=number)
    createBatchSamplesWithCode(number=number)
    child1 = getSingleSample(code = "/IMS/SARS/HA-773")
    child2 = getSingleSample(code = "/IMS/SARS/EPI-1")
    createBatchSamplesWithChild([child1, child2], number=number)
    closeSession()

    # print(f'Total number of IDs {len(obis_IDs)}')

if __name__ == "__main__":
    main()
