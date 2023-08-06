import pickle
import fasttext
from numpy import array


class DigIndicators(object):
    def __init__(self, fasttext_model_path, incall_model_path=None, outcall_model_path=None, movement_model_path=None,
                 multi_model_path=None, risky_model_path=None):
        # load pre-trained fasttext bin model
        self.model = fasttext.load_model(fasttext_model_path)
        self.loaded_model_incall = pickle.load(open(incall_model_path, 'rb')) if incall_model_path else None
        self.loaded_model_outcall = pickle.load(open(outcall_model_path, 'rb')) if outcall_model_path else None
        self.loaded_model_movement = pickle.load(open(movement_model_path, 'rb')) if movement_model_path else None
        self.loaded_model_multi = pickle.load(open(multi_model_path, 'rb')) if multi_model_path else None
        self.loaded_model_risky = pickle.load(open(risky_model_path, 'rb')) if risky_model_path else None

    # indicator domain functions
    def incall(self, text):
        if not self.loaded_model_incall:
            return None
        text_vector = array(self.model[text])
        vector_array = text_vector.reshape(1, -1)  # it is a single sample
        dic = dict()
        dic['value'] = "incall"
        dic['score'] = float(self.loaded_model_incall.predict_proba(vector_array)[:, -1])
        return dic

    def outcall(self, text):
        if not self.loaded_model_outcall:
            return None
        text_vector = array(self.model[text])
        vector_array = text_vector.reshape(1, -1)  # it is a single sample
        dic = dict()
        dic['value'] = "outcall"
        dic['score'] = float(self.loaded_model_outcall.predict_proba(vector_array)[:, -1])
        return dic

    def movement(self, text):
        if not self.loaded_model_movement:
            return None
        text_vector = array(self.model[text])
        vector_array = text_vector.reshape(1, -1)  # it is a single sample
        dic = dict()
        dic['value'] = "movement"
        dic['score'] = float(self.loaded_model_movement.predict_proba(vector_array)[:, -1])
        return dic

    def multi(self, text):
        if not self.loaded_model_multi:
            return None

        text_vector = array(self.model[text])
        vector_array = text_vector.reshape(1, -1)  # it is a single sample
        dic = dict()
        dic['value'] = "multi_girls"
        dic['score'] = float(self.loaded_model_multi.predict_proba(vector_array)[:, -1])
        return dic

    def risky(self, text):
        if not self.loaded_model_risky:
            return None
        text_vector = array(self.model[text])
        vector_array = text_vector.reshape(1, -1)  # it is a single sample
        dic = dict()
        dic['value'] = "risky_activity"
        dic['score'] = float(self.loaded_model_risky.predict_proba(vector_array)[:, -1])
        return dic

    def indicators(self, text):
        result_lst = list()
        incall_r = self.incall(text)
        if incall_r:
            result_lst.append(incall_r)
        outcall_r = self.outcall(text)
        if outcall_r:
            result_lst.append(outcall_r)
        movement_r = self.movement(text)
        if movement_r:
            result_lst.append(movement_r)
        multi_r = self.multi(text)
        if multi_r:
            result_lst.append(self.multi(text))
        risky_r = self.risky(text)
        if risky_r:
            result_lst.append(risky_r)
        return result_lst ifpython setup.py sdist upload -r pypi len(result_lst) > 0 else None
