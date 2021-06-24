class Sample:
    # Generator
    def __init__(self, identifier, permId, ofType, registrator, registrationDate, modifier, modificationDate, SAMPLE_TYPE, SEQUENCING_LAB_ID, SEQUENCING_METHOD, PRIME_DIAGNOSTIC_LAB_ID, SEQUENCE, DATE_OF_SAMPLING, SEQUENCING_LAB_SAMPLE_ID, ID, SEQUENCING_REASON, PUBLICATION_STATUS):
        self.name = ID
        self.identifier = identifier
        self.permId = permId
        self.type = ofType
        self.registrator = registrator
        self.registrationDate = registrationDate
        self.modifier = modifier
        self.modificationDate = modificationDate
        self.SAMPLE_TYPE = SAMPLE_TYPE
        self.SEQUENCING_LAB_ID = SEQUENCING_LAB_ID
        self.SEQUENCING_METHOD = SEQUENCING_METHOD
        self.PRIME_DIAGNOSTIC_LAB_ID = PRIME_DIAGNOSTIC_LAB_ID
        self.SEQUENCE = SEQUENCE
        self.DATE_OF_SAMPLING = DATE_OF_SAMPLING
        self.SEQUENCING_LAB_SAMPLE_ID = SEQUENCING_LAB_SAMPLE_ID
        self.SEQUENCING_REASON = SEQUENCING_REASON
        self.PUBLICATION_STATUS = PUBLICATION_STATUS


    # Class methods
    def get_identifier(self):
        return self.identifier

    def get_name(self):
        return self.name

    def get_sequence(self):
        return self.SEQUENCE
