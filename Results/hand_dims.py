import dims as d
import csv
import pdb

class HandDims:
    def __init__(self, hand_name, grasp_label):
        self.hand_name = hand_name
        self.width_max = -1
        self.width_min = -1
        self.abs_max_span = -1
        self.grasp_type = grasp_label
        self.max_dims = dict(distal=None, mid=None, base=None) # I want to make this a dictionary that returns Dims objects for each measurement
        self.min_dims = dict(distal=None, mid=None, base=None)
        self.int_dims = [None]
        # dict(distal=None, mid=None, base=None)... and mid returns a list of Dims objects if there are multiple

        # useful for plotting
        self.max_span_val = -1
        self.max_depth_val = -1

        self.read_csv_measurements(hand_name, grasp_label)

    def _check_max_vals(self, values, list_len):
        even_iterator = range(0, list_len, 2)
        odd_iterator = range(1, list_len, 2)

        for vs in [float(values[j]) for j in even_iterator]:
            if self.max_span_val < vs:
                self.max_span_val = vs

        for vd in [float(values[j]) for j in odd_iterator]:
            if self.max_depth_val < vd:
                self.max_depth_val = vd


    def read_csv_measurements(self, hand_name, dims_type): # TODO: right now, assumes one mid measurement!
        file_loc = f"{hand_name}/{hand_name}_{dims_type}_dims.csv"
        #print(file_loc)

        with open(file_loc, newline='') as csvfile:
            dims_reader = csv.reader(csvfile, delimiter=',', quotechar='|')

            # saving here, need to access outside between for loops
            int_objs = None
            int_iterator = None
            num_int_vals = None

            for i, row in enumerate(dims_reader):
                print(i)
                if i == 0: # distal measurements
                    num_vals = len(row) # 0 1 2 3 4 5 num_vals-2, num_vals-1
                    self.max_dims["distal"] = d.Dims("max", "distal",
                                                        span_val = float(row[0]), 
                                                        depth_val = float(row[1]))
                    self.min_dims["distal"] = d.Dims("min", "distal",
                                                        span_val = float(row[num_vals-2]), 
                                                        depth_val = float(row[num_vals-1]))

                    int_iterator = range(2, num_vals-2, 2)
                    num_int_vals = len(list(int_iterator))

                    int_placeholder = dict(distal=None, mid=None, base=None)
                    int_objs = [int_placeholder for j in int_iterator]

                    for j, k in enumerate(int_iterator):  # make a temporary list of int dims, then make that self.int_dims at the end?
                        dim = d.Dims("max", "distal",
                                        span_val = float(row[k]), 
                                        depth_val = float(row[k+1]))
                        
                        int_objs[j]["distal"] = dim

                    self._check_max_vals(row, num_vals)

                if i == 1:
                    self.max_dims["mid"] = d.Dims("max", "mid",
                                                    span_val = float(row[0]), 
                                                    depth_val = float(row[1]))
                    self.min_dims["mid"] = d.Dims("min", "mid",
                                                    span_val = float(row[num_vals-2]), 
                                                    depth_val = float(row[num_vals-1]))

                    for j, k in enumerate(int_iterator): 
                        dim = d.Dims("max", "mid",
                                        span_val = float(row[k]), 
                                        depth_val = float(row[k+1]))
                        
                        int_objs[j]["mid"] = dim

                    self._check_max_vals(row, num_vals)

                if i == 2:
                    self.max_dims["base"] = d.Dims("max", "base",
                                                    span_val = float(row[0]), 
                                                    depth_val = float(row[1]))
                    self.min_dims["base"] = d.Dims("min", "base",
                                                    span_val = float(row[num_vals-2]), 
                                                    depth_val = float(row[num_vals-1]))

                    for j, k in enumerate(int_iterator): 
                        dim = d.Dims("max", "base",
                                        span_val = float(row[k]), 
                                        depth_val = float(row[k+1]))
                        
                        int_objs[j]["base"] = dim

                    self._check_max_vals(row, num_vals)
                    
                elif i == 3:
                    # TODO: need to test this logic
                    vals = len(row)
                    if vals > 0:  # I do it like this so these rows can be optional
                        self.width_max = float(row[0])
                    if vals > 1:
                        self.width_min = float(row[1])

                elif i == 4:
                    vals = len(row)
                    if vals > 0:
                        self.abs_max_span = float(row[0])
                    if vals > 1:
                        abs_max_depth = float(row[1])  # TODO: for right now, we don't do anything with this value

                else:
                    continue  # if there are more rows, we want to just ignore them... for now



    def get_span(self, depth, actuation_perc):
        pass

    def span_depth_pair(self, loc, actuation_perc):
        pass

    def obj_fit(self, obj_dims, depth_pos):
        pass

    def obj_assess(self, obj_dims):
        pass

    def check_mid(self):
        pass

    def save_dims(self):
        pass

    def add_int_measurement(self, loc, dist, base, mids, wipe_ints=False):
        pass

    def edit_max(self, new_val):
        pass

    def edit_min(self, new_val):
        pass