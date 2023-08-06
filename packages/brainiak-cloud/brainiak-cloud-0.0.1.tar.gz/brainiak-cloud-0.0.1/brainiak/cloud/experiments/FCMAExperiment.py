import sys
import time
import math
import numpy as np
import nibabel as nib
from scipy.stats.mstats import zscore
from sklearn.externals import joblib
from brainiak.fcma.classifier import Classifier

from subprocess import check_output

from .Experiment import Experiment

class FCMAExperiment(Experiment):
    def __init__(self, opts):
        super(FCMAExperiment, self).__init__(opts)

        self.epoch = np.load(opts.get('epoch'))
        self.mask = nib.load(opts.get('mask')).get_data()

        self.tr_count = 0
        self.numTRs = opts.get('numTRs')
        self.windowSize = opts.get('windowSize')

        self.num_voxels = len(np.where(self.mask > 0)[0])

        self.raw_data = np.zeros((self.numTRs, self.num_voxels),
                                 np.float32,
                                 order='C')
        self.current_epoch = -1

        time1 = time.time()
        self.model = joblib.load(opts.get('model'))
        assert isinstance(self.model, Classifier), \
            'the loaded classifier is incorrect'
        time2 = time.time()
        self.logger.info('model loading done, takes: %.2f s' %
                         (time2 - time1)
                         )

        self.logger.debug('%d voxels per brain in the classifier, '
                          '%d training samples involved' %
                          (self.model.num_voxels_, self.model.num_samples_)
                          )

        self.logger.info('FCMAExperiment initialized, '
                         'ready to perform the real-time classification'
                         )
    def _prepare_data(self, start_tr, end_tr):
        # normalize the data
        data = np.copy(self.raw_data[start_tr: end_tr + 1])
        data = zscore(data, axis=0, ddof=0)
        # if zscore fails (standard deviation is zero),
        # set all values to be zero
        data = np.nan_to_num(data)
        data = data / math.sqrt(data.shape[0])
        return data

    def process(self, filepath):
        # TODO: fix this awfulness once we hear back on why dcm2niix is naming
        #       things oddly
        # Convert DICOM file to NIfTI
        output = check_output(['dcm2niix', '-s', 'y', '-f', '%n_%s', filepath])
        raw_nii_path = output.decode('ascii').split('\n')[1]
        raw_nii_path = raw_nii_path[raw_nii_path.find('/'):raw_nii_path.find('(')].strip() + '.nii'

        tmp_path = raw_nii_path.replace('.nii', '_%d.nii' % (self.tr_count + 1))
        output = check_output(['mv', raw_nii_path, tmp_path])
        raw_nii_path = tmp_path
        self.logger.info('Converted dcm to nii: ' + raw_nii_path)

        # Process NIfTI file
        processed_nii_path = raw_nii_path.replace('.nii', '_processed.nii.gz')
        output = check_output(['fsl5.0-flirt', '-in', raw_nii_path,
                               '-ref', self.opts.get('template'),
                               '-applyxfm', '-init',
                               self.opts.get('registration'),
                               '-out', processed_nii_path])
        self.logger.info('Processed nii: ' + processed_nii_path)

        # Read in processed data
        data = nib.load(processed_nii_path).get_data()

        # Apply mask and accumulate data
        self.raw_data[self.tr_count, :] = np.copy(data[self.mask > 0])

        # Compute correlation if needed
        if self.current_epoch == -1:
            if self.epoch[self.tr_count] == 1:
                self.current_epoch = self.tr_count
        elif self.epoch[self.tr_count] == 0:
            self.current_epoch = -1
        elif self.tr_count - self.current_epoch + 1 >= self.windowSize:
            if not self.opts.get('fixedWindow'):
                data = self._prepare_data(self.current_epoch,
                                          self.tr_count)
                # predict, calling BrainIAK
                y_pred = self.model.predict([data])
                confidence = self.model.decision_function([data])
                self.logger.info(
                            'predicted: %d with confidence %.2f, growing window, window size: %d' %
                            (y_pred[0], abs(confidence), self.tr_count + 1 - self.current_epoch)
                           )
            else:
                data = self._prepare_data(self.tr_count - self.windowSize + 1,
                                          self.tr_count)
                # predict, calling BrainIAK
                y_pred = self.model.predict([data])
                confidence = self.model.decision_function([data])
                self.logger.info(
                            'predicted: %d with confidence %.2f, sliding window, window size: %d' %
                            (y_pred[0], abs(confidence), self.windowSize)
                           )
        self.tr_count += 1
        if self.tr_count == self.numTRs:
            self.logger.info('Experiment complete!')
            sys.exit(1)

        return
