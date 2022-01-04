

class Dims:
    def __init__(self, finger_conf_label, dim_loc_label, span_val=-1, depth_val=-1):
        self.conf = finger_conf_label
        self.loc = dim_loc_label
        self.span = span_val
        self.depth = depth_val

    def get_dims(self):
        return (self.span, self.depth)