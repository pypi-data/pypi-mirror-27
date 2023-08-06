"""
:Authors: Tal Peretz
:Date: 11/24/2016
:TL;DR: this module is responsible for categorical and numerical columns transformations
"""

from collections import defaultdict

import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler


class TrainTransformations:
    col_to_scaler, col_to_encoder, col_to_width_edges, col_to_depth_edges = ({} for _ in range(4))

    def __init__(self, col_to_scaler, col_to_encoder, col_to_width_edges, col_to_depth_edges):
        self.col_to_scaler = col_to_scaler
        self.col_to_encoder = col_to_encoder
        self.col_to_width_edges = col_to_width_edges
        self.col_to_depth_edges = col_to_depth_edges


def _calc_optimal_num_of_bins(col):
    """
    given a collection of numerical values returns the optimal num of bins according to Freedman-Diaconis rule
    :param col: collection of numerical values
    :return: optimal num of bins according to Freedman-Diaconis rule
    """
    iqr = np.subtract(*np.percentile(col, [75, 25]))
    h = int(np.ceil((2 * iqr) / (len(col) ** (1 / 3)))) + 1
    optimal_n = int(np.round((max(col) - min(col)) / h))
    return optimal_n


def _pct_rank_qcut(series, n, edges=None):
    if edges is None:
        edges = pd.Series([float(i) / n for i in range(n + 1)])
    return series.rank(pct=1).apply(lambda x: (edges >= x).argmax()), edges


def _encode_categorical_columns(encode_df, expand_fit_df=None, col_to_encoder=None):
    """
    given a pandas dataframe with categorical attributes returns encoded dataframe, dictionary mapping column to encoder
    :param encode_df: pandas dataframe with categorical attributes
    :param expand_fit_df: optional dataframe to expand encode_df labels
    :param col_to_encoder: dictionary mapping each column to a transformer used when you want prefitted transformers
    :return: encoded dataframe, dictionary mapping column to encoder
    """
    # if there's another df passed we'll take it's labels into consideration
    #  so label encoder won't get tackled with new observations
    if expand_fit_df is not None:
        assert set(encode_df.columns).issubset(expand_fit_df.columns)
        encode_df = encode_df.apply(
            lambda col: col.cat.add_categories(
                set(expand_fit_df[col.name].cat.categories).difference(col.cat.categories)))
    if not col_to_encoder:
        col_to_encoder = defaultdict(LabelEncoder)
        encode_df.apply(
            lambda col: col_to_encoder[col.name].fit(col.cat.as_ordered().cat.categories))
    label_encoded_df = encode_df.apply(
        lambda col: col_to_encoder[col.name].transform(col.cat.as_ordered().sort_values().values))

    label_encoded_df.columns = ['ordered_%s' % col for col in label_encoded_df.columns]
    return label_encoded_df, col_to_encoder


def _transform_categorical_columns(train_categorical_df, test_categorical_df=None, col_to_encoder=None):
    """
    given a categorical dataframe returns transformed categorical dataframe based on col_to_encoder transformations
    :param train_categorical_df: pandas dataframe with categorical attributes
    :param test_categorical_df: pandas dataframe with categorical attributes
    :param col_to_encoder: dictionary mapping each column to a transformer
    :return: transformed categorical dataframe
    """
    # assume there's an order - encode according to sort values
    label_encoded_df, col_to_encoder = _encode_categorical_columns(encode_df=train_categorical_df,
                                                                   expand_fit_df=test_categorical_df,
                                                                   col_to_encoder=col_to_encoder)

    # assume there is no order - dummify categorical data
    dummiefied_categorical_df = pd.get_dummies(train_categorical_df,
                                               prefix=train_categorical_df.columns.tolist())
    dummiefied_categorical_df = dummiefied_categorical_df.apply(lambda col: col.astype('category'))
    return label_encoded_df, dummiefied_categorical_df, col_to_encoder


def _transform_numerical_columns(train_numerical_df, col_to_scaler=defaultdict(MinMaxScaler)):
    """
    given a numerical dataframe returns transformed numerical dataframe based on col_to_scaler transformations
    :param train_numerical_df: pandas dataframe with numerical attributes
    :param col_to_scaler: dictionary mapping each column to a transformer
    :return: transformed numerical dataframe
    """
    transformed_numerical_df = train_numerical_df.apply(
        lambda col: col_to_scaler[col.name].fit_transform(col))
    transformed_numerical_df = pd.DataFrame(data=transformed_numerical_df, index=train_numerical_df.index,
                                            columns=train_numerical_df.columns)
    return transformed_numerical_df, col_to_scaler


def discretize(numerical_df, col_to_width_edges=None, col_to_depth_edges=None, name_labels=False):
    """
    given a numerical dataframe returns equal width and equal depth labeled dataframes and their bins dict
    :param name_labels: boolean indicates whether to put string labels or int labels
    :param numerical_df: pandas DataFrame of numerical attributes
    :param col_to_width_edges: used when you want preset bins
    :param col_to_depth_edges: used when you want preset bins
    :return: equal_width_num_df, col_to_width_edges, equal_depth_num_df, col_to_depth_edges
    """
    assert (isinstance(numerical_df, pd.DataFrame)) and (not numerical_df.empty), \
        'numerical_df should be a valid pandas DataFrame'
    is_edges_recieved = True
    if (not col_to_width_edges) and (not col_to_depth_edges):
        col_to_width_edges, col_to_depth_edges = {}, {}
        is_edges_recieved = False
    equal_width_num_df, equal_depth_num_df = pd.DataFrame(), pd.DataFrame()
    for col_name, col in numerical_df.iteritems():
        num_of_bins = _calc_optimal_num_of_bins(col)
        if is_edges_recieved and (col_name in col_to_width_edges.keys()) and (col_name in col_to_depth_edges.keys()):
            equal_width_col = pd.cut(col, bins=col_to_width_edges[col_name]) if name_labels else pd.cut(col, bins=
            col_to_width_edges[col_name], labels=False)
            equal_width_col.name = 'equal_w_%s' % col_name
            equal_width_num_df.loc[:, equal_width_col.name] = equal_width_col
            equal_depth_col, _ = _pct_rank_qcut(col, num_of_bins, edges=col_to_depth_edges[col_name])
            equal_depth_col.name = 'equal_d_%s' % col_name
            equal_depth_num_df.loc[:, equal_depth_col.name] = equal_depth_col
        else:
            if num_of_bins > 1:
                equal_width_col, col_to_width_edges[col_name] = pd.cut(col, num_of_bins,
                                                                       retbins=True) if name_labels else pd.cut(col,
                                                                                                                num_of_bins,
                                                                                                                labels=False,
                                                                                                                retbins=True)
                equal_width_col.name = 'equal_w_%s' % col_name
                equal_width_num_df.loc[:, equal_width_col.name] = equal_width_col
                equal_depth_col, col_to_depth_edges[col_name] = _pct_rank_qcut(col, num_of_bins)
                equal_depth_col.name = 'equal_d_%s' % col_name
                equal_depth_num_df.loc[:, equal_depth_col.name] = equal_depth_col
    return equal_width_num_df, col_to_width_edges, equal_depth_num_df, col_to_depth_edges


def preprocess_train_columns(X_train, col_to_scaler=defaultdict(MinMaxScaler), X_test=None):
    """
    given a pandas DataFrame and a PipelineResults object
    returns a dataframe with columns ready for an ML model , categorical transformations list,
    numerical transformations list
    :param col_to_scaler: numerical scaler to apply on each of the numerical columns
    :param X_train: pandas DataFrame
    :param pipeline_results: class: 'PipelineResults'
    :return: dataframe with columns ready for an ML model, categorical transformations list,
    numerical transformations list
    """
    assert (isinstance(X_train, pd.DataFrame)) and (not X_train.empty), 'X_train should be a valid pandas DataFrame'
    col_to_width_edges, col_to_depth_edges = None, None
    numerical_cols = X_train.select_dtypes(include=[np.number]).columns
    categorical_cols = X_train.select_dtypes(include=['category']).columns
    is_numerical = len(numerical_cols) > 0
    is_categorical = len(categorical_cols) > 0
    label_encoded_df, dummiefied_categorical_df, scaled_numerical_df, col_to_encoder = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), {}

    if is_categorical:
        categorical_df = X_train.loc[:, categorical_cols]
        if X_test is not None:
            assert set(categorical_df.columns).issubset(X_test.columns)
            label_encoded_df, dummiefied_categorical_df, col_to_encoder = \
                _transform_categorical_columns(categorical_df, test_categorical_df=X_test.loc[:, categorical_cols])
        else:
            label_encoded_df, dummiefied_categorical_df, col_to_encoder = _transform_categorical_columns(categorical_df)

    # discretization of numerical columns
    if is_numerical:
        numerical_df = X_train.loc[:, numerical_cols]
        equal_width_num_df, col_to_width_edges, equal_depth_num_df, col_to_depth_edges = discretize(numerical_df)
        label_encoded_df = pd.concat([label_encoded_df, equal_width_num_df, equal_depth_num_df], axis=1)
        # add the encoded categorical columns to numerical columns
        numerical_df = pd.concat([X_train.loc[:, numerical_cols], label_encoded_df], axis=1)
        scaled_numerical_df, col_to_scaler = _transform_numerical_columns(numerical_df, col_to_scaler)
    transformed_df = pd.concat([scaled_numerical_df, dummiefied_categorical_df], axis=1)
    return transformed_df, TrainTransformations(col_to_scaler, col_to_encoder, col_to_width_edges, col_to_depth_edges)


def preprocess_test_columns(X_test, train_transformations):
    """
    given a pandas dataframe this function returns it after passing through the same transformations as the train set
    :param X_test: pandas dataframe where we should apply what we've learned
    :param pipeline_results: class: 'PipelineResults'
    :return: dataframe transformed exactly the same way the train set have transformed
    """
    assert (isinstance(X_test, pd.DataFrame)) and (not X_test.empty), 'X_test should be a valid pandas DataFrame'
    numerical_cols = X_test.select_dtypes(include=[np.number]).columns
    categorical_cols = X_test.select_dtypes(include=['category']).columns
    is_numerical = len(numerical_cols) > 0
    is_categorical = len(categorical_cols) > 0
    label_encoded_df, dummiefied_categorical_df, scaled_numerical_df, col_to_encoder = \
        pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), {}

    if is_categorical:
        categorical_df = X_test.loc[:, categorical_cols]
        label_encoded_df, dummiefied_categorical_df, col_to_encoder = \
            _transform_categorical_columns(categorical_df, col_to_encoder=train_transformations.col_to_encoder)

    # discretization of numerical columns
    if is_numerical:
        numerical_df = X_test.loc[:, numerical_cols]
        equal_width_num_df, _, equal_depth_num_df, _ = discretize(numerical_df,
                                                                  col_to_width_edges=train_transformations.col_to_width_edges,
                                                                  col_to_depth_edges=train_transformations.col_to_depth_edges)
        # add the encoded categorical columns to numerical columns
        numerical_df = pd.concat([X_test.loc[:, numerical_cols], label_encoded_df], axis=1)
        scaled_numerical_df, scaler = _transform_numerical_columns(numerical_df,
                                                                   col_to_scaler=train_transformations.col_to_scaler)
    transformed_df = pd.concat([scaled_numerical_df, dummiefied_categorical_df], axis=1)
    return transformed_df


def preprocess_for_association_rules(X):
    """
    given a pandas DataFrame and a PipelineResults object
    returns a dataframe with columns ready for an ML model , categorical transformations list,
    numerical transformations list
    :param col_to_scaler: numerical scaler to apply on each of the numerical columns
    :param X: pandas DataFrame
    :param pipeline_results: class: 'PipelineResults'
    :return: dataframe with columns ready for an ML model, categorical transformations list,
    numerical transformations list
    """
    assert (isinstance(X, pd.DataFrame)) and (not X.empty), 'X_train should be a valid pandas DataFrame'
    numerical_cols = X.select_dtypes(include=[np.number]).columns
    categorical_cols = X.select_dtypes(include=['category']).columns
    is_numerical = len(numerical_cols) > 0
    is_categorical = len(categorical_cols) > 0
    dummiefied_categorical_df = pd.DataFrame()

    # discretization of numerical columns
    if is_numerical:
        numerical_df = X.loc[:, numerical_cols]
        equal_width_num_df, col_to_width_edges, equal_depth_num_df, col_to_depth_edges = discretize(numerical_df,
                                                                                                    name_labels=True)

    if is_categorical:
        categorical_df = pd.concat([X.loc[:, categorical_cols], equal_width_num_df], axis=1)
        # assume there is no order - dummify categorical data
        dummiefied_categorical_df = pd.get_dummies(categorical_df)  # , prefix=categorical_df.columns.tolist()
        dummiefied_categorical_df = dummiefied_categorical_df.apply(lambda col: col.astype('category'))
    return dummiefied_categorical_df


@DeprecationWarning
def inverse_transform_columns(transformed_df, cat_transformations, num_transformations, pipeline_results):
    """
    given dataframe with columns ready for an ML model, categorical transformations list and numerical
    transformations list, returns the original dataframe before the transformations
    :param transformed_df: dataframe with columns ready for an ML model
    :param cat_transformations: categorical transformations list
    :param num_transformations: numerical transformations list
    :param pipeline_results: class: 'PipelineResults'
    :return: original dataframe before the transformations
    """
    numerical_cols = pipeline_results.ingestion_results.numerical_cols
    categorical_cols = pipeline_results.ingestion_results.categorical_cols
    X_cat = transformed_df[categorical_cols].copy()
    X_num = transformed_df[numerical_cols].copy()

    for transformation in cat_transformations:
        X_cat = transformation.inverse_transform(X_cat)
    for transformation in num_transformations:
        X_num = transformation.inverse_transform(X_num)

    return pd.concat([X_cat, X_num], axis=1)
