# Reference: https://github.com/cod3licious/textcatvis

import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer


def cleaner(text, to_lower=True, norm_num=False, char_to_strip=' ', non_alphanumeric_exceptions=","):
    # if the to_lower flag is true, convert the text to lowercase
    text = text.lower() if to_lower else text
    # Removes unwanted http hyper links in text
    text = re.sub(r"http(s)?://\S*", " ", text)
    # In some cases, one may want to normalize numbers for better visualization
    text = re.sub(r"[0-9]", "1", text) if norm_num else text
    # remove non-alpha numeric characters [!, $, #, or %] and normalize whitespace
    text = re.sub(r"[^A-Za-z0-9-" + non_alphanumeric_exceptions + "]", " ", text)
    # replace leftover unwanted white space
    text = re.sub(r"\s+", " ", text)
    # remove trailing or leading white spaces
    text = text.strip(char_to_strip)
    return text


def relevance_wt_transformer(raw_txt, wts_as_dict):
    # normalize score by absolute max value
    if isinstance(wts_as_dict, dict):
        max_wt = np.max(np.abs(list(wts_as_dict.values())))
        wts_as_dict = {word: wts_as_dict[word]/max_wt for word in wts_as_dict}
        # transform dict into list of tuples (word, relevance_wts)
        # TODO look into removing the below occurring side effect
        relevance_wts = []
        for word in raw_txt.split():
            # Clean up the raw word for irregularities
            word_cleaned = cleaner(word)
            if word_cleaned in wts_as_dict:
                relevance_wts.append((word, wts_as_dict[word_cleaned]))
            else:
                relevance_wts.append((word, None))
    else:
        raise Exception('relevance wts currently needs to be as dict')
    return relevance_wts


def vectorize_as_tf_idf(data, **kwargs):
    # Converting raw document to tf-idf feature matrix
    tfidf_vec = TfidfVectorizer(sublinear_tf=kwargs['sublinear_tf'], max_df=kwargs['max_df'],
                    stop_words=kwargs['stop_words'])
    X = tfidf_vec.fit_transform(data)
    return tfidf_vec, X


def get_feature_names(vectorizer_inst):
    return vectorizer_inst.get_feature_names()


def top_k_tfidf_features(each_row, features, top_k=25):
    """ Computes top 'k' tf-idf values in a row.

    Parameters
    __________
    each_row:
    features:
    top_k:

    Returns
    _______
    df : pandas.DataFrame

    """
    top_k_index = np.argsort(each_row)[::-1][:top_k]
    top_features = [(features[i], each_row[i]) for i in top_k_index]
    df = pd.DataFrame(top_features)
    df.columns = ['features', 'tf_idf']
    return df


def topk_tfidf_features_in_doc(data, features, top_k=25):
    """ Compute top tf-idf features for each document in the corpus

    Returns
    _______
    pandas.DataFrame with columns 'features', 'tf_idf'
    """
    row = np.squeeze(data.toarray())
    return top_k_tfidf_features(row, features, top_k)


# Lamda for converting data-frame to a dictionary
dataframe_to_dict = lambda key_column_name, value_column_name, df: df.set_index(key_column_name).to_dict()[value_column_name]


def _topk_tfidf_features_overall(data, feature_list, min_tfidf=0.1, summarizer_type='mean', top_n=25):
    """
    """
    d = data.toarray()
    d[d < min_tfidf] = 0
    summarizer_default = lambda x: np.sum(x, axis=0)
    summarizer_mean = lambda x: np.mean(x, axis=0)
    summarizer_median = lambda x: np.median(x, axis=0)
    choice_dict = {
        'sum': summarizer_default,
        'mean': summarizer_mean,
        'median': summarizer_median
    }
    select_type = lambda choice_type: choice_dict[choice_type]
    tfidf_summarized = select_type(summarizer_type)(d)
    return top_k_tfidf_features(tfidf_summarized, feature_list, top_n)


def topk_tfidf_features_by_class(X, y, feature_names, class_index, summarizer_type='mean', min_tfidf=0.1, top_n=25):
    """
    """
    labels = np.unique(y)
    ids_by_class = list(map(lambda label: np.where(y==label), labels))
    feature_df = _topk_tfidf_features_overall(X[ids_by_class[class_index]], feature_names, min_tfidf,
                                              summarizer_type, top_n)
    feature_df.label = ids_by_class[class_index]
    return feature_df


def _single_layer_lrp(feature_coef_df, bias, features_by_class, top_k):
    # Reference:
    # Franziska Horn, Leila Arras, Grégoire Montavon, Klaus-Robert Müller, Wojciech Samek. 2017
    # Exploring text datasets by visualizing relevant words (https://arxiv.org/abs/1707.05261)

    merged_df = pd.merge(feature_coef_df, features_by_class, on='features')
    merged_df['coef_wts'] = merged_df['coef_wts'].astype('float64')
    merged_df['tf_idf'] = merged_df['tf_idf'].astype('float64')
    merged_df['coef_tfidf_wts'] = merged_df['coef_wts']*merged_df['tf_idf'] + float(bias)

    top_feature_df = merged_df.nlargest(top_k, 'coef_tfidf_wts')[['features', 'coef_tfidf_wts']]
    top_feature_df_dict = dataframe_to_dict('features', 'coef_tfidf_wts', top_feature_df)
    return top_feature_df_dict, top_feature_df, merged_df


def _based_on_learned_estimator(feature_coef_df, bias, top_k):
    feature_coef_df['coef_wts'] = feature_coef_df['coef_wts'].astype('float64')
    feature_coef_df['coef_wts_intercept'] = feature_coef_df['coef_wts'] + float(bias)
    top_feature_df = feature_coef_df.nlargest(top_k, 'coef_wts_intercept')
    top_feature_df_dict = dataframe_to_dict(top_feature_df, 'features', 'coef_wts_intercept')
    return top_feature_df_dict, top_feature_df, feature_coef_df


def understand_estimator(estimator, class_label_index, features_by_class, feature_names,
                         no_of_features, top_k, relevance_type='default'):
    # Currently, support for sklearn based estimator
    # TODO: extend it for estimator from other frameworks - MLLib, H20, vw
    if ('coef_' in estimator.__dict__) is False:
        raise KeyError('the estimator does not support coef, try using LIME for local interpretation')

    # Currently, support for sklearn based estimator
    # TODO: extend it for estimator from other frameworks - MLLib, H20, vw
    coef_list = list(np.squeeze(estimator.coef_[class_label_index]))
    feature_coef_df = pd.DataFrame(np.column_stack([feature_names, coef_list]),
                                   columns=['features', 'coef_wts'])
    bias = estimator.intercept_[class_label_index]/no_of_features

    if relevance_type == 'default':
        top_feature_df_dict, top_feature_df, feature_coef_df = _based_on_learned_estimator(feature_coef_df, bias, top_k)
    elif relevance_type == 'SLRP':
        top_feature_df_dict, top_feature_df, feature_coef_df = _single_layer_lrp(feature_coef_df, bias,
                                                                                 features_by_class, top_k)
    return top_feature_df_dict, top_feature_df, feature_coef_df
