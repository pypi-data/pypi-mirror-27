import pickle
import fasttext
from numpy import array

# load pre-trained fasttext bin model
model = None
loaded_model_incall = None
loaded_model_outcall = None
loaded_model_movement = None
loaded_model_multi = None
loaded_model_risky = None


# load models
def load_fasttext_vec20_model(path):
    global model
    model = fasttext.load_model(path)


def load_model_incall(path):
    global loaded_model_incall
    loaded_model_incall = pickle.load(open(path, 'rb'))


def load_model_outcall(path):
    global loaded_model_outcall
    loaded_model_outcall = pickle.load(open(path, 'rb'))


def load_model_movement(path):
    global loaded_model_movement
    loaded_model_movement = pickle.load(open(path, 'rb'))


def load_model_multi(path):
    global loaded_model_multi
    loaded_model_multi = pickle.load(open(path, 'rb'))


def load_model_risky(path):
    global loaded_model_risky
    loaded_model_risky = pickle.load(open(path, 'rb'))


# indicator domain functions
def incall(text):
    text_vector = array(model[text])
    vector_array = text_vector.reshape(1, -1)  # it is a single sample
    dic = dict()
    dic['value'] = "incall"
    dic['score'] = float(loaded_model_incall.predict_proba(vector_array)[:, -1])
    return dic


def outcall(text):
    text_vector = array(model[text])
    vector_array = text_vector.reshape(1, -1)  # it is a single sample
    dic = dict()
    dic['value'] = "outcall"
    dic['score'] = float(loaded_model_outcall.predict_proba(vector_array)[:, -1])
    return dic


def movement(text):
    text_vector = array(model[text])
    vector_array = text_vector.reshape(1, -1)  # it is a single sample
    dic = dict()
    dic['value'] = "movement"
    dic['score'] = float(loaded_model_movement.predict_proba(vector_array)[:, -1])
    return dic


def multi(text):
    text_vector = array(model[text])
    vector_array = text_vector.reshape(1, -1)  # it is a single sample
    dic = dict()
    dic['value'] = "multi_girls"
    dic['score'] = float(loaded_model_multi.predict_proba(vector_array)[:, -1])
    return dic


def risky(text):
    text_vector = array(model[text])
    vector_array = text_vector.reshape(1, -1)  # it is a single sample
    dic = dict()
    dic['value'] = "risky_activity"
    dic['score'] = float(loaded_model_risky.predict_proba(vector_array)[:, -1])
    return dic


def indicators(text):
    result_lst = list()
    result_lst.append(incall(text))
    result_lst.append(outcall(text))
    result_lst.append(movement(text))
    result_lst.append(multi(text))
    result_lst.append(risky(text))
    return result_lst
