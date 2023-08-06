""" 
:Authors: Tal Peretz
:Date: 10/14/2016
:TL;DR: this module is responsible for univariate and bi-variate analysis
"""

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from pyds import constants

sns.set_style("whitegrid")


def describe(X, y=None, **kwargs):
    """
    given a pandas pandas DataFrame returns a pandas DataFrame describing basic statistics about numeric columns
    :param y: [pandas Series] target column
    :param pipeline_results: class: 'PipelineResults'
    :param X: [pandas DataFrame] predictor columns
    :return: pandas DataFrame describing basic statistics about numeric columns
    """
    assert (isinstance(X, pd.DataFrame)) and (not X.empty), 'X should be a valid pandas DataFrame'
    df = X.copy()
    numerical_cols = X.select_dtypes(include=[np.number]).columns
    categorical_cols = X.select_dtypes(include=['category']).columns
    num_description, cat_description = None, None
    if y is not None:
        assert (isinstance(y, pd.Series)) and (not y.empty), 'y should be a valid pandas Series'
        df[y.name] = y
    if len(numerical_cols) > 0:
        num_description = df[numerical_cols].describe(**kwargs)
    if len(categorical_cols) > 0:
        cat_description = df[categorical_cols].describe(**kwargs)
    return num_description, cat_description


def dist_plot(X, y=None, **kwargs):
    """
    given a pandas DataFrame plots a histogram for each numeric columns
    if a by=column keyword is passed splits the groups according to other column
    :param X: [pandas DataFrame] predictor columns
    :param pipeline_results: class: 'PipelineResults'
    :param y: [pandas Series] target column
    :param kwargs: passed to pandas.Series.hist
    """
    assert (isinstance(X, pd.DataFrame)) and (not X.empty), 'X should be a valid pandas DataFrame'
    numerical_figures, categorical_figures = [], []
    df = X.copy()
    if y is not None:
        assert (isinstance(y, pd.Series)) and (not y.empty), 'y should be a valid pandas Series'
        df[y.name] = y
    numerical_cols = X.select_dtypes(include=[np.number]).columns
    categorical_cols = X.select_dtypes(include=['category']).columns

    # numerical columns histogram plotting
    for i, col in enumerate(numerical_cols):
        numerical_figures.append(plt.figure(i))
        sns.distplot(df[col], **kwargs)
        plt.suptitle(str(col) + ' Distribution', fontsize=20)

    # categorical columns histogram plotting
    for i, col in enumerate(categorical_cols):
        categorical_figures.append(plt.figure(i))
        df[col].value_counts().dropna().plot(kind='bar', **kwargs)
        plt.suptitle(str(col) + ' Distribution', fontsize=20)
    return numerical_figures, categorical_figures


def box_plot(X, y=None):
    """
    given a pandas DataFrame plots a boxplot for each numeric columns
    if a by=column keyword is passed splits the groups according to other column
    :param y: [pandas Series] target column
    :param pipeline_results: class: 'PipelineResults'
    :param X: [pandas DataFrame] predictor columns
    :param kwargs: passed to pandas.Series.hist
    """
    assert (isinstance(X, pd.DataFrame)) and (not X.empty), 'X should be a valid pandas DataFrame'
    df = X.copy()
    if y is not None:
        assert (isinstance(y, pd.Series)) and (not y.empty), 'y should be a valid pandas Series'
        df[y.name] = y
    numerical_figure, categorical_figure = None, None
    numerical_cols = df.select_dtypes(include=[np.number]).columns
    categorical_cols = df.select_dtypes(include=['category']).columns
    if len(numerical_cols) > 0:
        numerical_figure = plt.figure()
        sns.boxplot(data=df[numerical_cols], color="c")
        sns.stripplot(data=df[numerical_cols], jitter=True, size=3, color=".3", linewidth=0)
        plt.suptitle('Raw Numerical Features', fontsize=20)
    if len(categorical_cols) > 0:
        categorical_figure = plt.figure()
        sns.boxplot(data=df[categorical_cols], color="c")
        sns.stripplot(data=df[categorical_cols], jitter=True, size=3, color=".3", linewidth=0)
        plt.suptitle('Raw Categorical Features', fontsize=20)
    return numerical_figure, categorical_figure


def scatter_plot(X, y=None, figure_title='Raw Features Scatter Matrix', **kwargs):
    """
    given a pandas DataFrame without categorical data plots scatterplot of the data for each
    reducer in ml.reduce_dimensions()
    :param figure_title: str, title for the pyplot figure
    :param y: [pandas Series] target column
    :param X: [pandas DataFrame] predictor columns without categorical data
    :param kwargs: passed to pandas.Series.plot
    """
    assert (isinstance(X, pd.DataFrame)) and (not X.empty), 'X should be a valid pandas DataFrame'
    if X.shape[1] > 5:
        return None
    df = X.copy()
    if y is not None:
        assert (isinstance(y, pd.Series)) and (not y.empty), 'y should be a valid pandas Series'
        df[y.name] = y
        scatter_mat = sns.pairplot(df, hue=y.name, diag_kind="kde", diag_kws=dict(shade=True), **kwargs)
    else:
        scatter_mat = sns.pairplot(df, diag_kind="kde", diag_kws=dict(shade=True), **kwargs)
    plt.suptitle(figure_title, fontsize=20)
    return scatter_mat


def contingency_table(X, y=None):
    """
    given a pandas DataFrame and target_column
    returns a list of contingency tables per categorical column
    :param y: [pandas Series] target column
    :param pipeline_results: class: 'PipelineResults'
    :param X: [pandas DataFrame] predictor columns
    :return: list of contingency tables per categorical column
    """
    assert (isinstance(X, pd.DataFrame)) and (not X.empty), 'X should be a valid pandas DataFrame'
    df = X.copy()
    contingency_tables = []
    categorical_cols = df.select_dtypes(include=['category']).columns
    cross_col = "count"
    if y is not None:
        cross_col = y
        if y.name in categorical_cols:
            categorical_cols.remove(y.name)
    if len(categorical_cols) > 1:
        for col in categorical_cols:
            contingency_tables.append(
                pd.crosstab(df[col].values, cross_col, margins=True, normalize=True))
    elif len(categorical_cols) == 1:
        contingency_tables.append(pd.crosstab(df[categorical_cols], cross_col, margins=True, normalize=True))
    return contingency_tables


def correlations(X, y=None):
    """
    given a pandas DataFrame returns correlation matrix and figure representing the correlations
    :param y: [pandas Series] target column
    :param X: [pandas DataFrame] predictor columns
    :param size: matplotlib figure size
    :return: correlation matrix and figure representing the correlations
    """
    assert (isinstance(X, pd.DataFrame)) and (not X.empty), 'X should be a valid pandas DataFrame'
    numerical_cols = X.select_dtypes(include=[np.number]).columns
    if len(numerical_cols) == 0:
        return None, None
    df = X.copy()
    if y is not None:
        df[y.name] = y
    corr = df.corr()
    fig = sns.clustermap(corr, linewidths=.5, figsize=constants.FIGURE_SIZE)
    plt.suptitle('Raw Features Correlation', fontsize=20)
    return corr, fig
