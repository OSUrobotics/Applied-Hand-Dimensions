# hand dimensions plotting, John Morrow
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Ellipse
import csv
import pdb

# hand example - Barrett hand
# bh_pow_max = [(20.8, 3.5), (21.5, 1.5), (9.5, 1.2)]
# bh_pow_int = [(9.9,7.2), (13.5, 5.6), (9.5, 1.2)]
# bh_pow_min = [(0, 5.9), (5.0, 5.1), (9.5, 1.2)]
#
# bh_prec_max = [(26.5, 2.7), (21.5, 1.5), (9.5, 1.2)]
# bh_prec_int = [(16.7, 8.7), (13.5, 5.6), (9.5, 1.2)]
# bh_prec_min = [(0, 9), (5.0, 5.1), (9.5, 1.2)]
# bh_prec_abs_max = (30.8, 1.2)


def mirror_measurements(line):
    """
    Handles mirroring measurements for span, depth sets
    """
    mirrored_line = []

    for (x, y) in line:
        mirrored_line.append((-1 * x, y))

    return mirrored_line


def mirror_measurement(pt):
    return [pt[0] * -1, pt[1]]  # x, y


def rel_size_assessment(obj_size, max_val, min_val, rel_thresholds):
    #print(f"{obj_size} | {min_val}->{max_val} | {rel_thresholds}")

    if max_val == min_val:
        if obj_size > max_val:
            return "tL"
        elif obj_size < min_val:
            return "tS"
        else:  # there's a problem
            return "-1"

    perc_size = (obj_size - min_val) / (max_val - min_val)
    #print(f"{perc_size}")

    if perc_size < 0:
        return "tS"
    elif perc_size > 1:
        return "tL"
    elif perc_size < (rel_thresholds[0]/100.):
        return "S"
    elif perc_size > (rel_thresholds[1]/100.):
        return "L"
    elif perc_size < (rel_thresholds[1]/100.) and perc_size > (rel_thresholds[0]/100.):
        return "M"
    else: # there's a problem
        return "-1"


def plot_single_hand(hand_name, dim_type, fig_size=10,
                     inf_width=True, halve_measurements=True, distal_measurement="midpoint",
                     show_plot=True, save_plot=False):
    dims = HandDims(hand_name, dim_type, inf_width=inf_width,
                    halve_measurements=halve_measurements, distal_measurement=distal_measurement)

    # TODO: make sure aspect ratio looks nicely
    dims.plot_dims(fig_size=fig_size, show_plot=show_plot, save_plot=save_plot)


def save_multiple_hand_dims(hand_names, dim_types):
    for h in hand_names:
        for d in dim_types:
            plot_single_hand(h, d, show_plot=False, save_plot=True)


def plots_both_types(hand_name, fig_size=20,
                     inf_width=True, halve_measurements=True, distal_measurement="midpoint",
                     save_plot=False, show_plot=True):
    # TODO: make sure aspect ratio looks nicely with 
    # fig = plt.figure(figsize=(0.75*fig_size, 0.25*fig_size)) # TODO: comes out weird with the two plots
    fig = plt.figure(figsize=(16, 8))
    width_inf = True  # TODO: fix here!

    dims = HandDims(hand_name, "precision", inf_width=inf_width,
                    halve_measurements=halve_measurements, distal_measurement=distal_measurement)
    # max_list, int_list, min_list, (max_w, min_w), absmax = read_csv_measurements(hand, "precision")
    ax1 = fig.add_subplot(1,2,1)
    dims.plot_dims(subplot_fig=fig, subplot_ax=ax1, tick_font_size=16, show_plot=False, save_plot=False)

    dims2 = HandDims(hand_name, "power", inf_width=inf_width,
                    halve_measurements=halve_measurements, distal_measurement=distal_measurement)
    # max_list, int_list, min_list, (max_w, min_w), absmax = read_csv_measurements(hand, "power")
    ax2 = fig.add_subplot(1,2,2, sharey=ax1)
    plt.setp(ax2.get_yticklabels(), visible=False)
    dims2.plot_dims(subplot_fig=fig, subplot_ax=ax2, tick_font_size=16, show_plot=False, save_plot=False)

    # overwrite the titling from the make_dimension_plot
    fig.suptitle(f"{hand_name.capitalize()} Measurements, Power and Precision", fontweight='bold', fontsize=16)
    ax1.set_title("Precision Measurements (cm)")
    ax2.set_title("Power Measurements (cm)")

    # if distal_measurement_point is not None:
    #     subtitle = f"* Distal measurement at {distal_measurement_point} of link."
    #     ax.text(0.1, -0.25, subtitle, transform=ax.transAxes, fontsize=10)

    if save_plot:
        plt.savefig(f"both_dimensions_{hand_name}.jpg", format='jpg')
        # name -> tuple: subj, hand  names
        print("Figure saved.")
        print(" ")

    if show_plot:
        plt.show()


def save_hands_plots(hand_names):
    for h in hand_names:
        plots_both_types(h, show_plot=False, save_plot=True)


def obj_rel_sizes(hand_names, dim_type, obj_span):
    for h in hand_names:
        print(h)
        d = HandDims(h, dim_type)
        print(d.size_object(obj_span))
        print(" ")

def mult_obj_rel_sizes(hand_names, obj_spans, dim_type):
    with open('obj_rel_sizes.csv', 'w') as f:
        writer = csv.writer(f)

        for o in obj_spans:
            print(o)
            row_to_write = []
            for h in hand_names:
                hd = HandDims(h, dim_type)
                d, m, b = hd.size_object(o)
                row_to_write.append(d)
                row_to_write.append(m)
                row_to_write.append(b)
            
            writer.writerow(row_to_write)


class HandDims:
    def __init__(self, hand_name, dims_type, inf_width=False, halve_measurements=True, distal_measurement=None):
        self.max_vals, self.int_vals, self.min_vals = None, None, None
        self.widths, self.abs_max, self.max_span, self.max_depth =  (None, None), None, None, None

        self.read_csv_measurements(hand_name, dims_type)

        self.hand = hand_name
        self.dim_type = dims_type

        self.inf_width = inf_width
        self.halve = halve_measurements
        self.distal_dim_point = distal_measurement

        # pass

    def get_dim_pair(self, hand_conf, level, unhalve_measurement=False):
        conf_dict = {
            "max": self.max_vals,
            "int": self.int_vals,
            "min": self.min_vals
        }

        level_dict = {
            "distal": 0,
            "mid": 1,
            "base": 2
        }

        # get level, as int or as string
        # selected_level = level
        selected_level = level_dict[level]

        # get hand conf, as string
        selected_conf = conf_dict[hand_conf]

        # return the span-depth pair
        if unhalve_measurement:
            return selected_conf[selected_level]*2
        else:
            return selected_conf[selected_level]

    def read_csv_measurements(self, hand_name, dims_type):
        file_loc = f"{hand_name}/{hand_name}_{dims_type}_dims.csv"

        max_vals = []
        int_vals = []
        min_vals = []

        max_span = 0
        max_depth = 0

        max_width = None
        min_width = None

        abs_max = None

        # dictionary to map row num to value reading, using variables to make it clearer what is what
        vals_dict = {0: max_vals, 1: int_vals, 2: min_vals}

        with open(file_loc, newline='') as csvfile:
            dims_reader = csv.reader(csvfile, delimiter=',', quotechar='|')

            for i, row in enumerate(dims_reader):
                # every two measurements is a span-depth pair
                if i in [0, 1, 2]:  # TODO: I should probably break this up better
                    vals_dict[i].append((float(row[0]), float(row[1])))
                    vals_dict[i].append((float(row[2]), float(row[3])))
                    vals_dict[i].append((float(row[4]), float(row[5])))
                    # print(vals_dict[i])

                    for vs in [float(row[0]), float(row[2]), float(row[4])]:
                        if max_span < vs:
                            max_span = vs

                    for vd in [float(row[1]), float(row[3]), float(row[5])]:
                        if max_depth < vd:
                            max_depth = vd

                elif i == 3:
                    # TODO: need to test this logic
                    vals = len(row)
                    if vals > 0:  # I do it like this so these rows can be optional
                        max_width = float(row[0])
                    if vals > 1:
                        min_width = float(row[1])

                elif i == 4:
                    vals = len(row)
                    if vals > 0:
                        abs_max = float(row[0])
                    if vals > 1:
                        abs_max_depth = float(row[1])  # TODO: for right now, we don't do anything

                else:
                    continue  # if there are more rows, we want to just ignore them

        self.max_vals = vals_dict[0]
        self.int_vals = vals_dict[1]
        self.min_vals = vals_dict[2]

        self.max_span = max_span
        self.max_depth = max_depth

        # pdb.set_trace()
        self.widths = (max_width, min_width)
        self.abs_max = (abs_max, abs_max_depth)
        # return max_vals, int_vals, min_vals, (max_width, min_width), abs_max

    def shade_region(self, up_dims, down_dims, shade_color, mirrored_shading=True):
        """
        Fills in region between two set of dimensions. Assumes symmetrical hand, however there is an option to only shade one side
        """
        up_spans = [up_dims[0][0], up_dims[1][0], up_dims[2][0]]
        up_depths = [up_dims[0][1], up_dims[1][1], up_dims[2][1]]

        down_spans = [down_dims[0][0], down_dims[1][0], down_dims[2][0]]
        down_depths = [down_dims[0][1], down_dims[1][1], down_dims[2][1]]
        rev_down_spans = list(reversed(down_spans))
        rev_down_depths = list(reversed(down_depths))

        poly_spans = up_spans + rev_down_spans
        poly_depths = up_depths + rev_down_depths

        poly = []
        for ax, ay in zip(poly_spans, poly_depths):
            pt = [ax, ay]
            poly.append(pt)

        polyg = plt.Polygon(poly, color=shade_color, alpha=0.2)
        plt.gca().add_patch(polyg)

        if mirrored_shading:
            opp_poly_spans = [x * -1 for x in poly_spans]

            opp_poly = []
            for ax, ay in zip(opp_poly_spans, poly_depths):
                pt = [ax, ay]
                opp_poly.append(pt)

            opp_polyg = plt.Polygon(opp_poly, color=shade_color, alpha=0.2)
            plt.gca().add_patch(opp_polyg)

    def plot_pt_markers(self, max_list, mid_list, min_list, ax):
        """
        Make scatter points at intermediate pts to make 'joints'. Does not work for multiple intermediate links
        """
        # [test[i] for i in [0,2]]
        max_pts = [max_list[i] for i in [0, 2]]
        mid_pts = [mid_list[i] for i in [0, 2]]
        min_pts = [min_list[i] for i in [0, 2]]

        marker_pts = max_pts + mid_pts + min_pts + \
                     mirror_measurements(max_pts) + mirror_measurements(mid_pts) + mirror_measurements(min_pts)
        for (x, y) in marker_pts:
            ax.scatter(x, y, edgecolor="black", c="grey", s=100, zorder=100)

        plus_pts = [max_list[1]] + [mid_list[1]] + [min_list[1]] + \
                   [mirror_measurement(max_list[1])] + [mirror_measurement(mid_list[1])] + [
                       mirror_measurement(min_list[1])]
        # need the extra brackets to enforce pts being grouped together

        for (x, y) in plus_pts:
            ax.scatter(x, y, marker="P", edgecolor="black", c="xkcd:light grey", s=125, zorder=101)

    def draw_palm(self, ax):
        # get the base coordinates (getting all of them just in case the proximal-palm joint moves)
        max_palm = self.get_dim_pair("max", "base")
        int_palm = self.get_dim_pair("int", "base")
        min_palm = self.get_dim_pair("min", "base")

        for (x,y) in [max_palm, int_palm, min_palm]:
            # plot the line representing the palm
            if self.halve:
                ax.plot([-0.5 * x, 0.5 * x], [0, 0], linewidth=7, color="black")
            else:
                ax.plot([-1 * x, 1 * x], [0, 0], linewidth=7, color="black")

    def plot_dims(self, subplot_fig=None, subplot_ax=None,
                  fig_size=10, fig_size_ratio=None, show_width=True,
                  plt_xlims=None, plt_ylims=None, tick_font_size=16, 
                  show_legend=True, show_plot=True, save_plot=False):

        if fig_size_ratio is None:
            fig_size_ratio = [1.25, 0.45]

        if show_width:
            widths = [self.widths[0], self.widths[1], True]
        else:
            widths = None

        if subplot_ax is not None and subplot_fig is not None:
            fig = subplot_fig
            ax = subplot_ax
        else:
            fig = plt.figure(figsize=(fig_size_ratio[0]*fig_size, fig_size_ratio[1]*fig_size))
            ax = fig.add_subplot()

        self._make_dimension_plot(fig=fig, ax=ax,
                            shade_distal=True, shade_proximal=True, y_offset=True,
                            width_vals=widths,
                            plt_xlims=plt_xlims, plt_ylims=plt_ylims, tick_font_size=tick_font_size,
                            show_legend=show_legend,
                            show_plot=show_plot,
                            save_plot=save_plot
                            )

        return fig, ax

    def _make_dimension_plot(self, fig, ax, width_vals=None,
                            shade_distal=True, shade_proximal=False,
                            plt_xlims=None, plt_ylims=None, tick_font_size=16,
                            y_offset=False,
                            show_legend=True, save_plot=False, show_plot=True):

        # used https://coolors.co/
        colors = ["#494276", "#61589D", "#847CB6"]
        # colors = ["#619F60", "#60619F", "#9F6061"]
        dot_line_colors = ["xkcd:blue grey", "xkcd:blue grey", "xkcd:blue grey"]  # ["#55B748", "#4855B7", "#B74855"]
        labels = ["max", "int", "min"]

        # since we are showing the whole space (with two fingers) we need to provide half the span value to each side
        if self.halve:
            max_dims = [(x * 0.5, y) for (x, y) in self.max_vals]
            int_dims = [(x * 0.5, y) for (x, y) in self.int_vals]
            min_dims = [(x * 0.5, y) for (x, y) in self.min_vals]
        else:
            max_dims = self.max_vals
            int_dims = self.int_vals
            min_dims = self.min_vals

        val_sets = [max_dims, int_dims, min_dims]

        self.plot_pt_markers(max_dims, int_dims, min_dims, ax=ax)

        # draw lines of measurements
        for vals, cs, ls in zip(val_sets, colors, labels):
            spans = [vals[0][0], vals[1][0], vals[2][0]]
            depths = [vals[0][1], vals[1][1], vals[2][1]]
            ax.plot(spans, depths, color=cs, label=ls, linewidth=3)

            opp_spans = [-1 * vals[0][0], -1 * vals[1][0], -1 * vals[2][0]]
            ax.plot(opp_spans, depths, color=cs, linewidth=3)

        # draw lines between similar levels of measurement (at distal (max), int, min)
        for (a, b), (c, d), (e, f), cs in zip(max_dims, int_dims, min_dims, dot_line_colors):
            sim_spans = [a, c, e]  # TODO: might have to play around with this one
            sim_depths = [b, d, f]
            ax.plot(sim_spans, sim_depths, linestyle="dotted", alpha=0.7, color=cs)

            opp_sim_spans = [-1 * e, -1 * c, -1 * a]
            opp_sim_depths = list(reversed(sim_depths))
            ax.plot(opp_sim_spans, opp_sim_depths, linestyle="dotted", alpha=0.7, color=cs)

        # TODO: region shading only works currently for 2 link fingers
        # shade the region between the distal and the intermediate points
        if shade_distal:
            dist_pts = [max_dims[0], int_dims[0], min_dims[0]]
            int_pts = [max_dims[1], int_dims[1], min_dims[1]]  # TODO: make it not plot between the distal links
            self.shade_region(dist_pts, int_pts, shade_color="xkcd:light green")

        # shade the region between the proximal and the intermediate points
        if shade_proximal:
            int_pts = [max_dims[1], int_dims[1], min_dims[1]]
            min_pts = [max_dims[2], int_dims[2], min_dims[2]]  # see min_dims, need to make it draw not between min_dims
            self.shade_region(int_pts, min_pts, shade_color="xkcd:pale green")

        # draw absolute max span value if given
        if self.abs_max is not None:
            if not self.halve:
                ax.axvline(self.abs_max[0], linestyle="-.", color="black", alpha=0.7, label="abs_max")
                ax.axvline(-1 * self.abs_max[0], linestyle="-.", color="black", alpha=0.7)
            else:
                ax.axvline(0.5 * self.abs_max[0], linestyle="-.", color="black", alpha=0.7, label="abs_max")
                ax.axvline(-0.5 * self.abs_max[0], linestyle="-.", color="black", alpha=0.7)

        # plot an indication that there is a difference between the base of the finger and the base of the palm
        if y_offset:
            # if non-zero value, draw lines from proximal base point downwards to signify more space
            # we will assume that y_offset is a float value
            bot_values = [max_dims[-1], int_dims[-1], min_dims[-1]]

            for (x, y) in bot_values:
                ax.plot([x, x], [0, y], linewidth=7, color="black")

                # draw the opposite side as well
                ax.plot([-1 * x, -1 * x], [0, y], linewidth=7, color="black")

        self.draw_palm(ax=ax)

        title = f"{self.hand.capitalize()}, {self.dim_type} grasp dimensions (cm)"

        # TODO: still using the widths as parameter, not the object -> turn into show_widths
        if width_vals is None or None in self.widths:
            ax.set_title(title, fontsize=18, fontweight='bold', pad=10) #fontweight='bold', fontsize=20)
        else:
            fig.suptitle(title, fontweight='bold', fontsize=20)

            if width_vals[2]:  # width_vals[2] is a boolean which indicates whether max width value is capped or can theoretically go on forever
                width_modifier = "+"
            else:
                width_modifier = ""

            widths = f"Width: {width_vals[1]} - {width_vals[0]}{width_modifier} cm"
            ax.set_title(widths, fontsize=tick_font_size)

        if self.distal_dim_point is not None:
            subtitle = f"* Distal measurement at {self.distal_dim_point} of link."
            ax.text(0.1, -0.15, subtitle, transform=ax.transAxes, fontsize=tick_font_size)

        if plt_xlims is not None:
            plt.xlim(plt_xlims) # [-12, 12])
        if plt_ylims is not None:
            plt.ylim(plt_ylims) # [0, 8])

        plt.yticks(fontsize=tick_font_size)
        plt.xticks(fontsize=tick_font_size)

        if show_legend:
            plt.legend(title="Finger Configs", title_fontsize=12, fontsize=12)  # TODO: maybe set alpha to 1 for legend?

        ax.set_aspect('equal', adjustable='box')

        if save_plot:
            plt.savefig(f"{self.dim_type}_dimensions_{self.hand}.jpg", format='jpg')
            # name -> tuple: subj, hand  names
            print("Figure saved.")
            print(" ")

        if show_plot:
            plt.show()

    def size_object(self, object_span, custom_thresholds=None):
        """
        Returns how big the object is within the ranges defined at each measurement point: distal, mid, min
        custom labeling refers to the upper limit of small, medium, ... (upper of large is 100)
        """
        if custom_thresholds is None:
            thresholds = [33, 66]
        else:
            thresholds = custom_thresholds

        # get distal assessment
        dist_max = self.get_dim_pair("max", "distal", unhalve_measurement=True)[0]
        dist_min = self.get_dim_pair("min", "distal", unhalve_measurement=True)[0]
        dist_rel_size = rel_size_assessment(object_span, dist_max, dist_min, rel_thresholds=thresholds)
        #print(dist_rel_size)

        # get mid assessment
        mid_max = self.get_dim_pair("max", "mid", unhalve_measurement=True)[0]
        mid_min = self.get_dim_pair("min", "mid", unhalve_measurement=True)[0]
        mid_rel_size = rel_size_assessment(object_span, mid_max, mid_min, rel_thresholds=thresholds)
        #print(mid_rel_size)

        # get min assessment
        min_max = self.get_dim_pair("max", "base", unhalve_measurement=True)[0]
        min_min = self.get_dim_pair("min", "base", unhalve_measurement=True)[0]
        min_rel_size = rel_size_assessment(object_span, min_max, min_min, rel_thresholds=thresholds)
        #print(min_rel_size)

        return dist_rel_size, mid_rel_size, min_rel_size

    def plot_object(self, plot_fig, plot_ax, plot_depth, span_adjust,
                    object_span, object_depth, obj_angle=0,
                    obj_name=None, obj_shape="rectangle",
                    show_plot=True, save_plot=False):
        # TODO: add ability to add the object's name into the plot title

        if obj_shape == "circle":
            circ_depth = plot_depth * (self.max_depth - self.get_dim_pair("min", "base")[1])
            circ_bot = circ_depth + object_span/2.0
            shape = Circle((0, circ_bot), object_span/2.0,
                           edgecolor='xkcd:burnt orange',
                           facecolor='none',
                           lw=2
                           )

        elif obj_shape == "ellipse":
            ell_depth = plot_depth * (self.max_depth - self.get_dim_pair("min", "base")[1])
            ell_bot = ell_depth + object_depth/2.0
            shape = Ellipse((0, ell_bot), object_span, object_depth,
                            edgecolor='xkcd:burnt orange',
                           facecolor='none',
                           lw=2
                           )

        else:
            rect_depth = plot_depth * (self.max_depth - self.get_dim_pair("min", "base")[1])
            rect_bot = rect_depth + self.get_dim_pair("min", "base")[1]  # start at the base link depth, go from there

            rect_left = -0.5 * object_span + span_adjust  # -1 object_span centers rectangle, span adjust shifts it around

            shape = Rectangle((rect_left, rect_bot), object_span, object_depth,
                                    angle=obj_angle,
                                    edgecolor='xkcd:burnt orange',
                                    facecolor='none',
                                    lw=2
                                    )

        plot_ax.add_patch(shape)

        obj_plot_title = f"{self.hand.capitalize()}, {self.dim_type} dims, {obj_name}"
        if None in self.widths:
            ax.set_title(obj_plot_title)
        else:
            plot_fig.suptitle(obj_plot_title, fontweight='bold', fontsize=16)

        if save_plot:
            if obj_name is None:
                plt.savefig(f"{self.dim_type}_dims_{self.hand}_w_obj.jpg", format='jpg')
            else:
                plt.savefig(f"{self.dim_type}_dims_{self.hand}_w_{obj_name}.jpg", format='jpg')
            # name -> tuple: subj, hand  names
            print("Figure saved.")
            print(" ")

        if show_plot:
            plt.show()


if __name__ == '__main__':
    all_hands = ["barrett", "human", "jaco2", "mO_cylindrical", "mO_spherical", "mt42", "robotiq2f85"]
    focused_hands = ["barrett", "jaco2", "robotiq2f85"]

    obj_size = {"Apple": [7.36, 0, "circle"], 
                "Pitcher": [12.2, 0, "circle"], 
                "Pudding": [3.41, 8.77, "rectangle"],
                "Golfball": [3.9, 0, "circle"],
                "Lock_base": [5.3975, 2.86, "rectangle"],
                "Hammer": [3.4925, 2.54, "ellipse"],
                "Cheezits_bigside": [15.875, 6.0325, "rectangle"],
                "Cheezits_smallside": [6.0325, 15.875, "rectangle"],
                "Die": [1.5875, 1.5876, "rectangle"],
                "Apple2": [6.985, 6.6675, "ellipse"],
                "Sprayer_base": [9.525, 5.715, "rectangle"],
                "Sprayer_neck": [5.08, 3.4925, "rectangle"]
                }
    all_obj_spans = [obj_size[k][0] for k in obj_size.keys()]

    # options: barrett, human, jaco2, mO_cylindrical, mO_spherical, mt42, robotiq2f85
    hand = "barrett"
    # options: precision, power
    dim_type = "precision"
    # object dimension you want to test
    obj_name = "Cheezits_smallside"
    obj_dim = obj_size[obj_name][0]
    obj_dim_depth=obj_size[obj_name][1]
    obj_shape = obj_size[obj_name][2]
    obj_plot_depth = 0.02

    dims = HandDims(hand, dim_type, inf_width=True, halve_measurements=True, distal_measurement=None)
    dims.size_object(obj_dim)
    fig, ax = dims.plot_dims(plt_xlims=[-16, 16],
                           plt_ylims=[0, 12],
                           fig_size_ratio=[1, 0.45],
                           show_width=False,
                           show_legend=False,
                           tick_font_size=16, fig_size=8,
                           show_plot=True, save_plot=True)
    # dims.plot_object(fig, ax, 
    #                  plot_depth=obj_plot_depth, span_adjust=0,
    #                  object_span=obj_dim, object_depth=obj_dim_depth,
    #                  obj_name=obj_name, obj_shape=obj_shape,
    #                  obj_angle=0, show_plot=True, save_plot=False)

    # print( rel_size_assessment(3, 11, 5, [33, 66]) ) # tS
    # print( rel_size_assessment(6, 11, 5, [33, 66]) ) # S
    # print( rel_size_assessment(8, 11, 5, [33, 66]) ) # M
    # print( rel_size_assessment(10, 11, 5, [33, 66]) ) # L
    # print( rel_size_assessment(15, 11, 5, [33, 66]) ) # tL

    # plots_both_types(hand)

    #print(f"For object size: {obj_dim}")
    #obj_rel_sizes(all_hands, dim_type, obj_dim)

    #mult_obj_rel_sizes(focused_hands, all_obj_spans, dim_type)

    # save_hands_plots(all_hands)

    # TODO: build width inf into the csv file
