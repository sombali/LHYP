from utils import get_logger
import pydicom as dicom
import os

logger = get_logger(__name__)


class DCMreaderSALE:

    def __init__(self, folder_name):
        '''
        Reads in the dcm files in a folder which corresponds to a patient.
        It follows carefully the physical slice locations and the frames in a hearth cycle.
        It does not matter if the location is getting higher or lower.
        '''
        self.broken = False
        self.images = []
        self.slice_locations = set()
        file_paths = []

        dcm_files = sorted(os.listdir(folder_name))
        dcm_files = [d for d in dcm_files if len(d.split('.')[-2]) < 4]
        if len(dcm_files) == 0:  # sometimes the order number is missing at the end
            dcm_files = sorted(os.listdir(folder_name))

        for file in dcm_files:

            if file.find('.dcm') != -1:
                try:
                    temp_ds = dicom.dcmread(os.path.join(folder_name, file))
                    if temp_ds.SliceLocation not in self.slice_locations:
                        self.slice_locations.add(temp_ds.SliceLocation)
                        self.images.append(temp_ds.pixel_array)
                        file_paths.append(os.path.join(folder_name, file))
                except:
                    self.broken = True
                    return

        self.num_images = len(self.images)

    def get_images(self):
        return self.images

    def get_slicelocations(self):
        return self.slice_locations


class DCMreader:

    def __init__(self, folder_name):
        '''
        Reads in the dcm files in a folder which corresponds to a patient.
        It follows carefully the physical slice locations and the frames in a hearth cycle.
        It does not matter if the location is getting higher or lower.
        '''
        self.broken = False
        self.images = []
        file_paths = []

        dcm_files = sorted(os.listdir(folder_name))
        dcm_files = [d for d in dcm_files if len(d.split('.')[-2]) < 4]
        if len(dcm_files) == 0:  # sometimes the order number is missing at the end
            dcm_files = sorted(os.listdir(folder_name))

        for file in dcm_files:

            if file.find('.dcm') != -1:
                try:
                    temp_ds = dicom.dcmread(os.path.join(folder_name, file))
                    self.images.append(temp_ds.pixel_array)
                    file_paths.append(os.path.join(folder_name, file))
                except:
                    self.broken = True
                    return

        self.num_images = len(self.images)

    def get_images(self):
        return self.images


class DCMreaderLA:

    def __init__(self, folder_name):
        '''
        Reads in the dcm files in a folder which corresponds to a patient.
        It follows carefully the physical slice locations and the frames in a hearth cycle.
        It does not matter if the location is getting higher or lower.
        '''
        self.broken = False
        self.images = []
        self.slice_number_mr = set()
        file_paths = []

        dcm_files = sorted(os.listdir(folder_name))
        dcm_files = [d for d in dcm_files if len(d.split('.')[-2]) < 4]
        if len(dcm_files) == 0:  # sometimes the order number is missing at the end
            dcm_files = sorted(os.listdir(folder_name))

        for file in dcm_files:

            if file.find('.dcm') != -1:
                try:
                    temp_ds = dicom.dcmread(os.path.join(folder_name, file), None, False, True)
                    SliceNumberMR = temp_ds["2001", "100a"]
                    if SliceNumberMR.value not in self.slice_number_mr:
                        self.slice_number_mr.add(SliceNumberMR.value)
                        self.images.append(temp_ds.pixel_array)
                        file_paths.append(os.path.join(folder_name, file))
                except:
                    self.broken = True
                    return

        self.num_images = len(self.images)

    def get_images(self):
        return self.images
