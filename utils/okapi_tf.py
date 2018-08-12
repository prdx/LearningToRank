def calculate_okapi_tf(tf_wd = 0, len_d = 0, avg_len_d = 0):
    return tf_wd / (tf_wd + 0.5 + 1.5 * (len_d / avg_len_d))
