
import configparser
import getpass
import time
import uuid
import random
from classes.Sample import Sample
from classes.Samples import Samples
from pybis import Openbis
from typing import Optional, Sequence
import datetime

def openSession(credentialsFile):
    global o

    config = configparser.ConfigParser()
    config.read('credentials.txt')

    # Setup URI and database to use
    url = config.get('OpenBIS', 'url')
    username = config.get('OpenBIS', 'username')
    password = config.get('OpenBIS', 'password')

    # Open session
    # TODO: Check for open session token in ~/.pybis/<url>.token
    start_timer = time.perf_counter()
    print('Initiate OpenBIS connection.')

    o = Openbis(url, verify_certificates=False)
    if password is None:
        password = getpass.getpass()
    o.login(username, password, save_token=True)

    stop_timer = time.perf_counter()
    print(f'Initiated OpenBIS connection in {stop_timer-start_timer:0.4f} seconds')
    print(f"Session is active: {o.is_session_active()} and token is {o.token}")

def getSamples():
    # Get samples
    start_timer = time.perf_counter()
    start = 0
    batchsize = 500
    samples = Samples()
    while True:
        search = o.get_samples(
            collection ='/IMS/SARS/SC2',
            start_with = start,                     # start_with and count
            count      = start+batchsize,                  # enable paging
            props      = "*"
        )
        start = start+batchsize+1
        print(len(search.df))
        if  len(search.df) == 0:
            break
        samples.add_samples([Sample(sample.identifier, sample.permId, sample.type, sample.registrator, sample.registrationDate, sample.modifier, sample.modificationDate, sample.SAMPLE_TYPE, sample.SEQUENCING_LAB_ID, sample.SEQUENCING_METHOD, sample.PRIME_DIAGNOSTIC_LAB_ID, sample.SEQUENCE, sample.DATE_OF_SAMPLING, sample.SEQUENCING_LAB_SAMPLE_ID, sample.ID, sample.SEQUENCING_REASON, sample.PUBLICATION_STATUS) for sample in search.df.itertuples()])
        print('done')

    stop_timer = time.perf_counter()
    print(f'Loading samples took {stop_timer-start_timer:0.4f} seconds')

    return samples


def getSingleSample(code='') -> Optional[Sample]:
    try:
        sample = o.get_sample(code)
        return sample
    except ValueError:
        return None


def createRandomSample():

    sample = o.new_sample(
        type       = 'SEQUENCE',
        code = f"IMS-10001-COVR-{str(uuid.uuid4())}",
        experiment = '/IMS/SARS/SC2',
        props      = {
            "sequence": random.choice(["ATCTGTAAATTTTAGCTAATTGGTGTT", "ATCTGTAAATTTTAGATCTGTAAATTTTAGCTTTT", "AATTTGGGGGGGATTAGATGATGATAT"]),
            "date_of_sampling": random.choice(["2021-06-09", "2021-05-01", "2021-04-25", "2021-03-15"]),
            "sequencing_method": random.choice(["Illumina", "OXFORD_NANOPORE", "PACBIO_SMRT"]),
            "sequencing_reason": random.choice(["X","N","Y", "A"]),
            "suspected_variant_of_concern": random.choice(["B.1.1.7", "A.1", "B1.12", "B.1.351"]),
            "sample_type": random.choice(["s001", "s002", "s003"]),
            "publication_status": random.choice(["published", "in review", "unpublished"]),
            "sequencing_lab_sample_id": str(uuid.uuid1()),
            "sequencing_lab_upload_timestamp": random.choice(["2021-06-09 15:00:00 +0200", "2021-02-01 18:00:00 +0200"]),
            "desh_qc_passed": random.choice([True, False]),
            "desh_rejection_reason": random.choice(["not matching ID", "reason2"]),
            "desh_download_timestamp": random.choice(["2021-06-08 13:22:00 +0200", "2021-06-01 14:10:41 +0200"]),
            "duplicate_id": random.choice(["55", "", "NA"]),
            "pangolin_version": random.choice(["1.0", "2.3.4", "2.5.0"]),
            "pangolin_learn_version": random.choice(["1.1", "3.3.4", "2.0"]),
            "pangolin_synonyme": random.choice(["Syn1", "Syn2", "Syn3"]),
            "pangolin_variant_of_concern": random.choice(["B.1.617.2", "B.1.1.7", "A.1", "B1.12", "B.1.351"]),
            "authors": random.choice(["Capobianchi,M.R., Carletti,F., Lalle,E., Bordi,L., Marsella,P., Colavita,F., Matusali,G., Nicastri,E., Ippolito,G. and Castilletti,C.", "Author2", "Author3"]),
            "host_organism": random.choice(["9606", "10090"])
        }
    )
    return sample


def createBatchSamples(number=10):

    start_timer = time.perf_counter()

    trans = o.new_transaction()
    for i in range (0, number):
        sample = createRandomSample()
        trans.add(sample)

    trans.commit()
    stop_timer = time.perf_counter()
    now = datetime.datetime.now()
    print(f'[{now}] - Created {number} samples and took {stop_timer-start_timer:0.4f} seconds')


def createBatchSamplesWithChild(children: Sequence [Sample],
                                number: int=10):
    start_timer = time.perf_counter()

    trans = o.new_transaction()
    for i in range (0, number):
        sample = createRandomSample()
        # sample.set_children(children)
        sample.add_children(children)
        trans.add(sample)

    trans.commit()
    stop_timer = time.perf_counter()
    now = datetime.datetime.now()
    print(f'[{now}] - Created {number} samples with sample-children and took {stop_timer-start_timer:0.4f} seconds')


def createBatchSamplesWithCode(number: int=10):
    start_timer = time.perf_counter()

    trans = o.new_transaction()
    for i in range (0, number):
        sample = createRandomSample()
        sample.children = ["/IMS/SARS/HA-773", "/IMS/SARS/EPI-1"]
        trans.add(sample)

    trans.commit()
    stop_timer = time.perf_counter()
    now = datetime.datetime.now()
    print(f'[{now}] - Created {number} samples with code-children and took {stop_timer-start_timer:0.4f} seconds')




def closeSession():
    # Close session
    o.logout()
    print(f"Session is active: {o.is_session_active()}")