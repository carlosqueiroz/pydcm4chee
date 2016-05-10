# -*- coding: utf-8 -*-

from instance import Instance
from utils import get_from_nested_dict


class Series(object):
    
    def __repr__(self):
        return '<Series object. SeriesInstanceUID "{}">'.format(self.uid)

    def __init__(self, pacs, study, input_dict,
                 fetch_metadata=False, fetch_instances=False):
        self.pacs = pacs
        self.study = study
        self.attributes = input_dict
        self.uid = get_from_nested_dict(self.attributes ,['0020000E', 'Value', 0])
        self.retrieved = False  # whether or not the DICOM object has been retrieved from the PACS
        
        self.metadata = None
        if fetch_metadata:
            self.fetch_metadata()

        self.instances = None
        if fetch_instances:
            self.fetch_instances()

    def fetch_metadata(self):
        self.metadata = self.pacs._make_request(
            'studies/{}/series/{}/metadata'.format(self.study.uid, self.uid)
        )

    def fetch_instances(self):
        self.instances = []
        path = 'studies/{}/series/{}/instances'.format(self.study.uid, self.uid)
        for ins_dict in self.pacs._make_request(path):
            self.instances.append(Instance(pacs=self.pacs, series=self, input_dict=ins_dict))

    def retrieve_dicom(self):
        self.retrieved = True
        if self.instances is None:
            self.fetch_instances()
        for ins in self.instances:
            ins.retrieve_dicom()

    def get_dicom_objects(self):
        if self.retrieved is False:
            self.retrieve_dicom()
        for ins in self.instances:
            yield ins.get_dicom_objects()

    def save_dicom_to_disk(self, base_dir=None, study_dir=None, file_prefix=''):
        self.retrieved = True
        if self.instances is None:
            self.fetch_instances()
        for ins in self.instances:
            ins.save_dicom_to_disk(base_dir=base_dir, study_dir=study_dir, file_prefix=file_prefix)
