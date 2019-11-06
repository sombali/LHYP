from con_reader import CONreaderVM
from dicom_reader import DCMreaderVM
import numpy as np
import pickle
import os
from dicom_readers import DCMreaderSALE, DCMreaderLA, DCMreader


class PatientData:

    def __init__(self, path):

        folder_names = ['la', 'lale', 'sa', 'sale']

        self.data = {}

        for folder_name in folder_names:
            self.data[folder_name] = []

        print(path)
        for folder_name in folder_names:
            image_folder =  path + '/' + folder_name
            print(image_folder)

            if folder_name is 'sale':

                drSALE = DCMreaderSALE(image_folder)
                self.data[folder_name] = drSALE.get_images()

            elif folder_name is 'la':

                drLA = DCMreaderLA(image_folder)
                self.data[folder_name] = drLA.get_images()

            elif folder_name is 'sa':
                image_folder = path + '/' + folder_name + '/images'
                drSA = DCMreaderVM(image_folder)
                con_file = path + '/' + folder_name + '/contours.con'
                try:
                    cr = CONreaderVM(con_file)
                    contours = cr.get_hierarchical_contours()
                except:
                    continue

                for slc in contours:
                    max_frame = None
                    max_area = 0
                    for frm in contours[slc]:
                        for mode in contours[slc][frm]:
                            if mode == 'ln':
                                x_coordinates = np.transpose(contours[slc][frm][mode])[0]
                                y_coordinates = np.transpose(contours[slc][frm][mode])[1]
                                actual_area = poly_area(x_coordinates, y_coordinates)

                                if actual_area > max_area:
                                    max_area = actual_area
                                    max_frame = frm

                    cntrs = []
                    rgbs = []
                    if max_frame is not None:

                        try:
                            image = drSA.get_image(slc, max_frame)
                        except:
                            continue

                        for mode in contours[slc][max_frame]:
                            if mode == 'ln':
                                rgb = [1, 0, 0]
                            elif mode == 'lp':
                                rgb = [0, 1, 0]
                            else:
                                rgb = None
                            if rgb is not None:
                                cntrs.append(contours[slc][max_frame][mode])
                                rgbs.append(rgb)
                        if len(cntrs) > 0:
                            self.data[folder_name].append(image)
                            self.data[folder_name].append(cntrs)

            else:
                dr = DCMreader(image_folder)
                self.data[folder_name] = dr.images

        print('------------')

        for folder_name in folder_names:
            print('####' + folder_name)
            print(len(self.data[folder_name]))


def poly_area(x, y):
    return 0.5 * np.abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))


record_path = '/Users/somogyibalazs/school/lhyp/records/hypertrophy'

files = os.listdir(record_path)

patient_files = []

for file in files:
    print(file)
    if file[0] is not '.':
        patient_files.append(file)
    else:
        continue

for patient in patient_files:
    path_for_patient = record_path + '/' + patient
    pd = PatientData(path_for_patient)
    with open(patient + '.pickle', 'wb') as handle:
        pickle.dump(pd.data, handle)
"""

elso = '/Users/somogyibalazs/school/lhyp/records/hypertrophy/17071635AMR801'
pd = PatientData(elso)
with open('17071635AMR801' + '.pickle', 'wb') as handle:
    pickle.dump(pd.data, handle)
"""