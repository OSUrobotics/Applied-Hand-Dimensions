# hand dimensions plotting, John Morrow
import matplotlib.pyplot as plt
import csv

# hand example - Barrett hand
bh_pow_max = [(20.8, 3.5), (21.5, 1.5), (9.5, 1.2)]
bh_pow_int = [(9.9,7.2), (13.5, 5.6), (9.5, 1.2)]
bh_pow_min = [(0, 5.9), (5.0, 5.1), (9.5, 1.2)]

bh_prec_max = [(26.5, 2.7), (21.5, 1.5), (9.5, 1.2)]
bh_prec_int = [(16.7, 8.7), (13.5, 5.6), (9.5, 1.2)]
bh_prec_min = [(0, 9), (5.0, 5.1), (9.5, 1.2)]
bh_prec_abs_max = (30.8, 1.2)


def read_csv_measurements(hand_name, dims_type):
    file_loc = f"{hand_name.capitalize()}/{hand_name}_{dims_type}_dims.csv"

    max_vals = []
    int_vals = []
    min_vals = []
    
    max_width = None
    min_width = None

    abs_max = None

    # dictionary to map row num to value reading, using variables to make it clearer what is what
    vals_dict = {0: max_vals, 1: int_vals, 2: min_vals}

    with open(file_loc, newline='') as csvfile:
        dims_reader = csv.reader(csvfile, delimiter=',', quotechar='|')

        for i, row in enumerate(dims_reader):
            # every two measurements is a span-depth pair
            if i in [0, 1, 2]:
                vals_dict[i].append((row[0], row[1]))
                vals_dict[i].append((row[2], row[3]))
                vals_dict[i].append((row[4], row[5]))
            else:
                # TODO: pull out extra info like width, absolute max?
                pass

            print(vals_dict[i])

    max_vals = vals_dict[0]
    int_vals = vals_dict[1]
    min_vals = vals_dict[2]
    return max_vals, int_vals, min_vals, (max_width, min_width), abs_max
        

def mirror_measurements(line):
    """
    Handles mirroring measurements for span, depth sets
    """
    mirrored_line = []

    for (x,y) in line:
        mirrored_line.append((-1*x, y))

    return mirrored_line


def shade_region(up_dims, down_dims, shade_color, mirrored_shading=True):
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
        opp_poly_spans = [x*-1 for x in poly_spans]

        opp_poly = []
        for ax, ay in zip(opp_poly_spans, poly_depths):
            pt = [ax, ay]
            opp_poly.append(pt)

        opp_polyg = plt.Polygon(opp_poly, color=shade_color, alpha=0.2)
        plt.gca().add_patch(opp_polyg)


def plot_joints(max, mid, min, ax):
    """
    Make scatter points at intermediate pts to make 'joints'. Does not work for multiple intermediate links
    """
    jt_pts = max[1:] + mid[1:] + min[1:] + \
        mirror_measurements(max[1:]) + mirror_measurements(mid[1:]) + mirror_measurements(min[1:])
    for (x, y) in jt_pts:
        ax.scatter(x,y, edgecolor="black", c="grey", s=100, zorder=100)


def make_dimension_plot(plot_type, hand_name, max_dims, int_dims, min_dims, 
                    halve_measurements=False, abs_max=None, 
                    shade_distal=True, shade_proximal=False, 
                    fig_size=7, y_offset=False, distal_measurement_point=None,
                    save_plot=False, show_plot=True):
    # TODO: make sure aspect ratio looks nicely with 
    fig = plt.figure(figsize=(1.5*fig_size, fig_size))
    ax = fig.add_subplot()

    colors = ["#619F60", "#60619F", "#9F6061"]
    dot_line_colors = ["xkcd:blue grey", "xkcd:blue grey", "xkcd:blue grey"] #["#55B748", "#4855B7", "#B74855"]
    labels = ["max", "int", "min"]

    # since we are showing the whole space (with two fingers) we need to provide half the span value to each side
    if halve_measurements:
        max_dims = [(x*0.5, y) for (x, y) in max_dims]
        int_dims = [(x*0.5, y) for (x, y) in int_dims]
        min_dims = [(x*0.5, y) for (x, y) in min_dims]

    val_sets = [max_dims, int_dims, min_dims]

    plot_joints(max_dims, int_dims, min_dims, ax=ax)

    # draw lines of measurements
    for vals, cs, ls in zip(val_sets, colors, labels):
        spans = [vals[0][0], vals[1][0], vals[2][0]]
        depths = [vals[0][1], vals[1][1], vals[2][1]]
        ax.plot(spans, depths, color=cs, label=ls, linewidth=3)

        opp_spans = [-1*vals[0][0], -1*vals[1][0], -1*vals[2][0]]
        ax.plot(opp_spans, depths, color=cs, linewidth=3)

    # draw lines between similar levels of measurement (at distal (max), int, min)
    for (a, b), (c, d), (e, f), cs in zip(max_dims, int_dims, min_dims, dot_line_colors):
        sim_spans = [a, c, e] #, -1*e, -1*c, -1*a]  # TODO: might have to play around with this one
        sim_depths = [b, d, f] #, f, d, b]

        ax.plot(sim_spans, sim_depths, linestyle="dotted", alpha=0.7, color=cs)

        opp_sim_spans = [-1*e, -1*c, -1*a]
        opp_sim_depths = list(reversed(sim_depths))
        ax.plot(opp_sim_spans, opp_sim_depths, linestyle="dotted", alpha=0.7, color=cs)

    # TODO: region shading only works currently for 2 link fingers
    # shade the region between the distal and the intermediate points
    if shade_distal:
        dist_pts = [max_dims[0], int_dims[0], min_dims[0]]
        int_pts = [max_dims[1], int_dims[1], min_dims[1]]  # TODO: make it not plot between the distal links
        shade_region(dist_pts, int_pts, shade_color="xkcd:light green")

    # shade the region between the proximal and the intermediate points
    if shade_proximal:
        int_pts = [max_dims[1], int_dims[1], min_dims[1]]
        min_pts = [max_dims[2], int_dims[2], min_dims[2]]  # see min_dims, need to make it draw not between min_dims
        shade_region(int_pts, min_pts, shade_color="xkcd:cream")

    # draw absolute max span value if given
    if abs_max is not None:
        if not halve_measurements:
            ax.axvline(abs_max, linestyle="-.", color="black", alpha=0.7)
            ax.axvline(-1*abs_max, linestyle="-.", color="black", alpha=0.7)
        else:
            ax.axvline(0.5*abs_max, linestyle="-.", color="black", alpha=0.7)
            ax.axvline(-0.5*abs_max, linestyle="-.", color="black", alpha=0.7)

    # plot an indication that there is a difference between the base of the finger and the base of the palm
    if y_offset:
        # if non-zero value, draw lines from proximal base point downwards to signify more space
        # we will assume that y_offset is a float value
        bot_values = [max_dims[-1], int_dims[-1], min_dims[-1]]

        for (x, y) in bot_values:
            ax.plot([x, x], [0, y], linewidth=7, color="black")

            # draw the opposite side as well
            ax.plot([-1*x, -1*x], [0, y], linewidth=7, color="black")

    # TODO: add width measurements into the title
    if distal_measurement_point is not None:
        fig.suptitle(f"{hand_name.capitalize()}, {plot_type} grasp dimensions", fontweight='bold', fontsize=16)
        ax.set_title(f"Distal measurement at {distal_measurement_point} of link.")
    else:
        ax.set_title(f"{hand_name.capitalize()}, {plot_type} grasp dimensions", fontweight='bold', fontsize=16)

    plt.legend(title="Finger Configs")  # TODO: maybe set alpha to 1 for legend?

    if save_plot:
        plt.savefig(f"{plot_type}_dimensions_{hand_name}.jpg", format='jpg')
        # name -> tuple: subj, hand  names
        print("Figure saved.")
        print(" ")

    if show_plot:
        plt.show()


if __name__ == '__main__':
    dim_type = "power"
    hand = "barrett"

    # TODO: get out absolute max and width from csv
    max_list, int_list, min_list, _, _ = read_csv_measurements(hand, dim_type)

    make_dimension_plot(dim_type, hand, 
                        bh_pow_max, bh_pow_int, bh_pow_min, 
                        shade_distal=True, shade_proximal=True, 
                        halve_measurements=True, y_offset=True, 
                        distal_measurement_point="midpoint",
                        abs_max=bh_prec_abs_max[0])
