import pandas as pd
import numpy as np
from itertools import product, combinations
import scipy.stats
import statsmodels.api as sm
from statsmodels.formula.api import ols, mixedlm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats import multitest


def read_qpcr_data(plate_csv, sheet_name = "0"):
    data = pd.read_excel(plate_csv, sheet_name = sheet_name)
    rows_cols = [(data.Well[i][0], int(data.Well[i][1:])) for i in range(data.shape[0])]
    data = pd.concat((pd.DataFrame(data = rows_cols, columns = ["row", "col"]), data), axis=1).set_index(["row", "col"])
    return data

def get_well_list(row_str, col_range):
    return list(product(row_str, col_range))

def get_min_ntc_axs_plates(figdata):
    min_ntc = 999
    i = 0
    for key, plates in figdata.items():
        for plate in plates:
            if np.min(plate.data['ntc']) < min_ntc:
                min_ntc = plate.data['ntc']
            ntc = plate.data['ntc'] if i == 0 else np.concatenate((ntc, plate.data['ntc']))
            i += 1
    return np.floor(min_ntc), ntc

def update_detection_mask(figdata, ntc):
    for key, plates in figdata.items():
        updated = []
        for plate in plates:
            plate.get_detection_mask(ntc)           
            updated.append(plate)
        figdata[key] = updated
    return figdata

def read_data(csv_path, sep = ","):
    return pd.read_csv(csv_path, sep = sep)

def get_rna_conc_per_mL_plasma(bioanalyzer_table):
    return bioanalyzer_table.rna_pg_ul * bioanalyzer_table.total_vol_ul / bioanalyzer_table.total_plasma_vol_mL / 1000 #ng per mL

def get_n_processing_hours(time_table):
    return np.ceil(time_table.n_samples / time_table.n_samples_per_batch) * time_table.n_hours_per_batch

def multitest_corr(pvals, method = "bonferroni"):
    return multitest.multipletests(pvals, method = method)

def test_and_adj(test_combos, data, label_col, col_to_test, alternative, use_ttest = False, corr_method = "bonferroni"):
    pvals = {}
    for label_i, label_j in test_combos:
        x_data_mask = (data.loc[:, label_col] == label_i) if "Grouped" not in label_i else (data.loc[:, label_col].str.contains(label_i[len("Grouped "):]))
        y_data_mask = (data.loc[:, label_col] == label_j) if "Grouped" not in label_j else (data.loc[:, label_col].str.contains(label_j[len("Grouped "):]))
        
        x_data = data.loc[x_data_mask, col_to_test].to_numpy()
        y_data = data.loc[y_data_mask, col_to_test].to_numpy()

        #Order here matters - per source code: We interpret one-sided tests as asking whether y is 'test (greater or less)' than x
        #For ttest see https://stackoverflow.com/questions/15984221/how-to-perform-two-sample-one-tailed-t-test-with-numpy-scipy
        if use_ttest:
            tstat, twoside_pval = scipy.stats.ttest_ind(x_data, y_data, equal_var = False) 
            if alternative == 'less':
                tstat, twoside_pval = scipy.stats.ttest_ind(y_data, x_data, equal_var = False) #Flipped for less
            pval = twoside_pval
            if alternative != 'two-sided':
                pval = (twoside_pval / 2) if (tstat > 0) else (1 - (twoside_pval / 2)) #Get 1-sided pval from 2-sided
        else:
            pval = scipy.stats.mannwhitneyu(x = x_data, y = y_data, alternative = alternative).pvalue 
        
        pvals[(label_i, label_j)] = pval

    pvals_adj = multitest_corr(np.array(list(pvals.values())), method = corr_method)
    return pvals, pvals_adj

#Sum of Square types explained here - https://mcfromnz.wordpress.com/2011/03/02/anova-type-iiiiii-ss-explained/
def anova_test(data, formula, test = 'F', type = 2, robust = None):
    model = ols(formula, data = data).fit()
    print(model.summary())
    anova = sm.stats.anova_lm(model, test = test, typ = type, robust = robust)
    residuals = scipy.stats.shapiro(model.resid)
    return residuals, anova
