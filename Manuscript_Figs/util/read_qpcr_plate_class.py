import numpy as np
import pandas as pd

#well labels has [[(rows, cols)], [(rows,cols)]] for each rep
class qpcr_plate():
    def __init__(self, plate_data, well_labels, exclude_wells = None, fluorophore = "VIC", rep_thresh = 1):
        self.data_tech_reps = {}
        self.data = {}
        self.dCt_pc = {}
        self.tech_rep_match_mask = {}
        self.detected = {}
        self.rep_thresh = rep_thresh
        
        for label, vals in well_labels.items():
            n_tech_reps = len(vals)
            for rep in range(n_tech_reps):
                label_data = plate_data.loc[vals[rep]]
                if exclude_wells is not None:
                    label_data.drop(exclude_wells, errors = 'ignore', inplace = True)
                    
                label_data = pd.DataFrame(label_data.loc[label_data.Fluor == fluorophore].reset_index().Cq)
                all_reps = label_data.copy() if rep == 0 else pd.concat((all_reps, label_data), axis=1, ignore_index = True) #Assumes that tech reps were passed in same order
            
            self.data_tech_reps[label] = all_reps
            self._get_avg_Ct(label)
            self._get_tech_rep_mask(label)
            
        if 'pc' in self.data.keys():
            for label, vals in self.data.items():
                self._get_dCt(label)
    
    def _get_avg_Ct(self, label):
        #has_non_nans = (np.sum(np.sum(~np.isnan(self.data_tech_reps[label]))) > 0)
        #not_empty = self.data_tech_reps[label].shape[0]
        self.data[label] = np.nanmean(self.data_tech_reps[label], axis=1) #if (has_non_nans and not_empty) else np.nan
        return
    
    def _get_tech_rep_mask(self, label):
        self.tech_rep_match_mask[label] = (np.nanstd(self.data_tech_reps[label], axis=1) <= self.rep_thresh)
        return
    
    def _get_dCt(self, left_key, right_key = 'pc'):
        self.dCt_pc[left_key] = self.data[left_key] - self.data[right_key]
        return
    
    def get_detection_mask(self, ntc):
        for label, vals in self.data.items():
            self.detected[label] = (vals < ntc)
        return
        
    def get_d_or_ddCt(self, left_key, right_key, is_ddCt = True):
        isec_mask = np.logical_and(
                            np.logical_and(self.tech_rep_match_mask[left_key], self.tech_rep_match_mask[right_key]),
                            np.logical_and(self.detected[left_key], self.detected[right_key])
                    )
        out = self.dCt_pc[left_key][isec_mask] - self.dCt_pc[right_key][isec_mask] if is_ddCt else self.data[left_key][isec_mask] - self.data[right_key][isec_mask]
        return out
    
    def get_plotting_df(self, keys_labels_included_dict, only_detected = True, is_dCt = True):
        i = 0
        for key, label_i in keys_labels_included_dict.items():
            mask = np.logical_and(self.tech_rep_match_mask[key], self.detected[key]) if only_detected else np.repeat(True, self.tech_rep_match_mask[key].shape[0])
            tech_reps_match = self.dCt_pc[key][mask] if is_dCt else self.data[key][mask]
            label_tech_reps_match = np.repeat(label_i, len(tech_reps_match))

            d = tech_reps_match.copy() if i == 0 else np.concatenate((d, tech_reps_match), axis=0)
            label = label_tech_reps_match.copy() if i == 0 else np.concatenate((label, label_tech_reps_match), axis=0)
            i += 1
        return pd.DataFrame(data = {'val' : d, 'step' : label})