# -*- coding: utf-8 -*-
# Copyright © 2017 Apple Inc. All rights reserved.
#
# Use of this source code is governed by a BSD-3-clause license that can
# be found in the LICENSE.txt file or at https://opensource.org/licenses/BSD-3-Clause
from __future__ import print_function as _
from __future__ import division as _
from __future__ import absolute_import as _
import turicreate as _tc
import re as _re
import os as _os
from turicreate.toolkits._model import CustomModel as _CustomModel
from turicreate.toolkits._model import PythonProxy as _PythonProxy
from turicreate.toolkits._internal_utils import _toolkit_repr_print
import operator as _operator
import turicreate as _turicreate
import logging as _logging

def _BOW_FEATURE_EXTRACTOR(sf):
    """
    Return an SFrame containing a bag of words representation of each column.
    """
    if isinstance(sf, dict):
        out = _tc.SArray([sf]).unpack('')
    elif isinstance(sf, _tc.SFrame):
        out = sf.__copy__()
    else:
        raise ValueError("Unrecognized input to feature extractor.")
    for f in _get_str_columns(out):
        out[f] = _tc.text_analytics.count_words(out[f])
    return out

def create(dataset, target, features=None, method='auto', validation_set=None):
    """
    Create a model that trains a classifier to classify sentences from a
    collection of documents. The model is a
    :class:`~turicreate.logistic_classifier.LogisticClassifier` model trained
    using a bag-of-words representation of the text dataset.

    Parameters
    ----------
    dataset: SFrame
      Contains one column that contains the text dataset of interest.  This can be
      unstructured text dataset, such as that appearing in forums, user-generated
      reviews, and so on.

    target: str
      The column name containing class labels for each document.

    features: list[str], optional
      The column names of interest containing text dataset. Each provided column
      must be str type. Defaults to using all columns of type str.

    method: str, optional
      Method to use for feature engineering and modeling. Currently only
      bag-of-words and logistic classifier ('bow-logistic') is available.

    validation_set : SFrame, optional
      A dataset for monitoring the model's generalization performance.

    Returns
    -------
    out : :class:`~SentenceClassifier`

    Examples
    --------
    >>> import turicreate as tc
    >>> dataset = tc.SFrame({'rating': [1, 5], 'text': ['hate it', 'love it']})

    >>> m = tc.sentence_classifier.create(dataset, 'rating', features=['text'])
    >>> m.predict(dataset)

    You may also evaluate predictions against known sentence scores.

    >>> metrics = m.evaluate(dataset)
    """
    logger = _logging.getLogger(__name__)

    # Validate method.
    if method == 'auto':
        method = 'bow-logistic'
    if method not in ['bow-logistic']:
        raise ValueError("Unsupported method provided.")

    # Validate dataset
    if features is None:
        features = dataset.column_names()

    # Remove target column from list of feature columns.
    features = [f for f in features if f != target]

    # Process training set using the default feature extractor.
    train = dataset
    feature_extractor = _BOW_FEATURE_EXTRACTOR
    train = feature_extractor(train)

    # Check for a validation set.
    kwargs = {}
    if validation_set is not None:
        validation_set = feature_extractor(validation_set)
        kwargs['validation_set'] = validation_set

    m = _tc.logistic_classifier.create(train,
                                       target=target,
                                       features=features,
                                       l2_penalty=.2,
                                       **kwargs)
    num_examples = len(dataset)
    model = SentenceClassifier()
    model.__proxy__.update(
        {'target':   target,
         'features': features,
         'method':   method,
         'num_examples': num_examples,
         'num_features': len(features),
         'classifier': m})
    return model

class SentenceClassifier(_CustomModel):
    _PYTHON_SENTENCE_CLASSIFIER_MODEL_VERSION = 1

    def __init__(self, state=None):
        if state is None:
            state = {}

        self.__proxy__ = _PythonProxy(state)


    @classmethod
    def _native_name(cls):
        return "sentence_classifier"

    def _get_version(self):
        return self._PYTHON_SENTENCE_CLASSIFIER_MODEL_VERSION

    def _get_native_state(self):
        import copy
        retstate = copy.copy(self.__proxy__.state)
        retstate['classifier'] = retstate['classifier'].__proxy__
        return retstate

    @classmethod
    def _load_version(self, state, version):
        from turicreate.toolkits.classifier.logistic_classifier import LogisticClassifier
        state['classifier'] = LogisticClassifier(state['classifier'])
        state = _PythonProxy(state)
        return SentenceClassifier(state)

    def predict(self, dataset):
        """
        Return predictions for ``dataset``, using the trained model.

        Parameters
        ----------
        dataset : SFrame
            dataset of new observations. Must include columns with the same
            names as the features used for model training, but does not require
            a target column. Additional columns are ignored.

        Returns
        -------
        out : SArray
            An SArray with model predictions.

        See Also
        ----------
        create, evaluate, classify


        Examples
        --------
        >>> import turicreate as tc
        >>> dataset = tc.SFrame({'rating': [1, 5], 'text': ['hate it', 'love it']})
        >>> m = tc.sentence_classifier.create(dataset, 'rating', features=['text'])
        >>> m.predict(dataset)

        """
        m = self.__proxy__['classifier']
        f = _BOW_FEATURE_EXTRACTOR
        return m.predict(f(dataset))

    def classify(self, dataset):
        """
        Return a classification, for each example in the ``dataset``, using the
        trained model. The output SFrame contains predictions as both class
        labels as well as probabilities that the predicted value is the
        associated label.

        Parameters
        ----------
        dataset : SFrame
            dataset of new observations. Must include columns with the same
            names as the features used for model training, but does not require
            a target column. Additional columns are ignored.

        Returns
        -------
        out : SFrame
            An SFrame with model predictions i.e class labels and probabilities.

        See Also
        ----------
        create, evaluate, predict

        Examples
        --------
        >>> import turicreate as tc
        >>> dataset = tc.SFrame({'rating': [1, 5], 'text': ['hate it', 'love it']})
        >>> m = tc.sentence_classifier.create(dataset, 'rating', features=['text'])
        >>> output = m.classify(dataset)

        """
        m = self.__proxy__['classifier']
        f = _BOW_FEATURE_EXTRACTOR
        return m.classify(f(dataset))

    def __str__(self):
        """
        Return a string description of the model to the ``print`` method.

        Returns
        -------
        out : string
            A description of the NearestNeighborsModel.
        """
        return self.__repr__()

    def _get_summary_struct(self):

        dataset_fields = [('Number of examples', 'num_examples')]
        model_fields = [('Target column', 'target'),
                        ('Features',     'features'),
                        ('Method',       'method')]
        sections = [dataset_fields, model_fields]
        section_titles = ['dataset', 'Model']
        return sections, section_titles

    def __repr__(self):
        width = 32
        key_str = "{:<{}}: {}"
        (sections, section_titles) = self._get_summary_struct()
        out = _toolkit_repr_print(self, sections, section_titles, width=width)
        return out

    def evaluate(self, dataset, metric = 'auto', **kwargs):
        """
        Evaluate the model by making predictions of target values and comparing
        these to actual values.

        Parameters
        ----------
        dataset : SFrame
            An SFrame having the same feature columns as provided when creating
            the model.

        metric : str, optional
            Name of the evaluation metric.  Possible values are:

            - 'auto'             : Returns all available metrics.
            - 'accuracy'         : Classification accuracy (micro average).
            - 'auc'              : Area under the ROC curve (macro average)
            - 'precision'        : Precision score (macro average)
            - 'recall'           : Recall score (macro average)
            - 'f1_score'         : F1 score (macro average)
            - 'log_loss'         : Log loss
            - 'confusion_matrix' : An SFrame with counts of possible prediction/true label combinations.
            - 'roc_curve'        : An SFrame containing information needed for an ROC curve

            For more flexibility in calculating evaluation metrics, use the
            :class:`~turicreate.evaluation` module.

        Returns
        -------
        out : dict
            Dictionary of evaluation results where the key is the name of the
            evaluation metric (e.g. `accuracy`) and the value is the evaluation
            score.

        See Also
        ----------
        create, predict, classify

        """
        target = self.__proxy__['target']
        m = self.__proxy__['classifier']
        f = _BOW_FEATURE_EXTRACTOR
        test = f(dataset)
        return m.evaluate(test, **kwargs)

    def summary(self):
        """
        Get a summary for the underlying classifier.
        """
        return self.__proxy__['classifier'].summary()


def _get_str_columns(sf):
    """
    Returns a list of names of columns that are string type.
    """
    return [name for name in sf.column_names() if sf[name].dtype == str]

