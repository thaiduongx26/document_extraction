import itertools
from operator import itemgetter
import simplejson
from pdfplumber.utils import objects_to_bbox, DEFAULT_X_TOLERANCE, to_list, cluster_objects, DEFAULT_Y_TOLERANCE, \
    decimalize
from decimal import *

def extract_words(page,
                  x_tolerance=DEFAULT_X_TOLERANCE,
                  y_tolerance=DEFAULT_Y_TOLERANCE,
                  keep_blank_chars=False
                  ):
    x_tolerance = decimalize(x_tolerance)
    y_tolerance = decimalize(y_tolerance)

    def process_word_chars(chars):
        x0, top, x1, bottom = objects_to_bbox(chars)
        return {
            "x0": x0,
            "x1": x1,
            "top": top,
            "bottom": bottom,
            "text": "".join(map(itemgetter("text"), chars)),
            "chars": chars
        }

    def make_set_clusters(doctop_cluster):
        new_clusters = []
        for c in doctop_cluster:
            new_cluster = [simplejson.dumps(c[i]) for i in range(len(c))]
            new_cluster = list(set(new_cluster))
            cluster_to_dict = []
            for i in range(len(new_cluster)):
                d = simplejson.loads(new_cluster[i])
                for k in d.keys():
                    if type(d[k]) == float:
                        d[k] = Decimal(str(d[k]))
                cluster_to_dict.append(d)
            new_clusters.append(cluster_to_dict)
        return new_clusters

    def check_two_chars(char1, char2):
        if abs(char1['x0'] - char2['x0']) < 1:
            return False
        return True

    def get_line_words(chars, tolerance=DEFAULT_X_TOLERANCE):
        get_text = itemgetter("text")
        chars_sorted = sorted(chars, key=itemgetter("x0"))
        new_chars_sorted = []
        for i in range(len(chars_sorted)):
            if i == 0 or check_two_chars(chars_sorted[i], chars_sorted[i-1]):
                new_chars_sorted.append(chars_sorted[i])            
        chars_sorted = new_chars_sorted
        words = []
        current_word = []

        for char in chars_sorted:
            if not keep_blank_chars and get_text(char).isspace():
                if len(current_word) > 0:
                    words.append(current_word)
                    current_word = []
                else:
                    pass
            elif len(current_word) == 0:
                current_word.append(char)
            else:
                last_char = current_word[-1]
                if char["x0"] > (last_char["x1"] + tolerance):
                    words.append(current_word)
                    current_word = []
                current_word.append(char)

        if len(current_word) > 0:
            words.append(current_word)
        processed_words = list(map(process_word_chars, words))
        return processed_words

    chars = to_list(page.chars)
    doctop_clusters = cluster_objects(chars, "doctop", y_tolerance)
    doctop_clusters = make_set_clusters(doctop_clusters)
    nested = [get_line_words(line_chars, tolerance=x_tolerance)
              for line_chars in doctop_clusters]
    # text = ''.join([nested[2][i]['x0'] for i in range(len(nested[2]))])
    # x0 = [nested[2][i]['x0'] for i in range(len(nested[2]))]
    # print(x0)
    # print(nested[2])
    # print(2 / 0)

    words = list(itertools.chain(*nested))
    return words
