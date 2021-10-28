# hand dimensions plotting, John Morrow
import matplotlib.pyplot as plt
import csv
import pdb

# hand example - Barrett hand
bh_pow_max = [(20.8, 3.5), (21.5, 1.5), (9.5, 1.2)]
bh_pow_int = [(9.9,7.2), (13.5, 5.6), (9.5, 1.2)]
bh_pow_min = [(0, 5.9), (5.0, 5.1), (9.5, 1.2)]

bh_prec_max = [(26.5, 2.7), (21.5, 1.5), (9.5, 1.2)]
bh_prec_int = [(16.7, 8.7), (13.5, 5.6), (9.5, 1.2)]
bh_prec_min = [(0, 9), (5.0, 5.1), (9.5, 1.2)]
bh_prec_abs_max = (30.8, 1.2)


def read_csv_measurements(hand_name, dims_type):
    file_loc = f"{hand_name}/{hand_name}_{dims_type}_dims.csv"
    print(file_loc)

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
                vals_dict[i].append((float(row[0]), float(row[1]) ))
                vals_dict[i].append((float(row[2]), float(row[3]) ))
                vals_dict[i].append((float(row[4]), float(row[5]) ))
                # print(vals_dict[i])

            elif i == 3:
                # TODO: need to test this logic
                vals = len(row)
                if vals > 0:  # I do it like this so these rows can be optional
                    max_width = float(row[0])
                if vals > 1:
                    min_width = float(row[1])
            elif i==4:
                vals = len(row)
                if vals > 0:
                    abs_max = float(row[0])
                if vals > 1:
                    abs_max_depth = float(row[1])  # TODO: for right now, we don't do anything

            else:
                continue  # if there are more rows, we want to just ignore them

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


def mirror_measurement(pt):
    return [pt[0]*-1, pt[1]] # x, y


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


def plot_pt_markers(max_list, mid_list, min_list, ax):
    """
    Make scatter points at intermediate pts to make 'joints'. Does not work for multiple intermediate links
    """
    # [test[i] for i in [0,2]]
    max_pts = [max_list[i] for i in [0,2]]
    mid_pts = [mid_list[i] for i in [0,2]]
    min_pts = [min_list[i] for i in [0,2]]

    marker_pts = max_pts + mid_pts + min_pts + \
        mirror_measurements(max_pts) + mirror_measurements(mid_pts) + mirror_measurements(min_pts)
    for (x, y) in marker_pts:
        ax.scatter(x,y, edgecolor="black", c="grey", s=100, zorder=100)

    plus_pts = [max_list[1]] + [mid_list[1]] + [min_list[1]] + \
        [mirror_measurement(max_list[1])] + [mirror_measurement(mid_list[1])] + [mirror_measurement(min_list[1])]
        # need the extra brackets to enforce pts being grouped together

    for (x, y) in plus_pts:
        ax.scatter(x,y, marker="P", edgecolor="black", c="xkcd:light grey", s=125, zorder=101)


def make_dimension_plot(plot_type, hand_name, 
                    max_dims, int_dims, min_dims,
                    fig, ax,
                    halve_measurements=False, abs_max=None, width_vals=None, 
                    shade_distal=True, shade_proximal=False, 
                    fig_size=7, y_offset=False, distal_measurement_point=None,
                    save_plot=False, show_plot=True):

    # used https://coolors.co/
    colors = ["#494276", "#61589D", "#847CB6"]
    #colors = ["#619F60", "#60619F", "#9F6061"]
    dot_line_colors = ["xkcd:blue grey", "xkcd:blue grey", "xkcd:blue grey"] #["#55B748", "#4855B7", "#B74855"]
    labels = ["max", "int", "min"]

    # since we are showing the whole space (with two fingers) we need to provide half the span value to each side
    if halve_measurements:
        max_dims = [(x*0.5, y) for (x, y) in max_dims]
        int_dims = [(x*0.5, y) for (x, y) in int_dims]
        min_dims = [(x*0.5, y) for (x, y) in min_dims]

    val_sets = [max_dims, int_dims, min_dims]

    plot_pt_markers(max_dims, int_dims, min_dims, ax=ax)

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
        shade_region(int_pts, min_pts, shade_color="xkcd:pale green")


    # draw absolute max span value if given
    if abs_max is not None:
        if not halve_measurements:
            ax.axvline(abs_max, linestyle="-.", color="black", alpha=0.7, label="abs_max")
            ax.axvline(-1*abs_max, linestyle="-.", color="black", alpha=0.7)
        else:
            ax.axvline(0.5*abs_max, linestyle="-.", color="black", alpha=0.7, label="abs_max")
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


    title = f"{hand_name.capitalize()}, {plot_type} grasp dimensions"
    if width_vals is not None:
        fig.suptitle(title, fontweight='bold', fontsize=16)

        if width_vals[2]:  # width_vals[2] is a boolean which indicates whether max width value is capped or can theoretically go on forever
            width_modifier = "+"
        else:
            width_modifier = ""

        widths = f"Width: {width_vals[1]} - {width_vals[0]}{width_modifier} cm"
        ax.set_title(widths)
    else:
        ax.set_title(title)


    if distal_measurement_point is not None:
        subtitle = f"* Distal measurement at {distal_measurement_point} of link."
        ax.text(0.1, -0.15, subtitle, transform=ax.transAxes, fontsize=10)


    plt.legend(title="Finger Configs")  # TODO: maybe set alpha to 1 for legend?
    ax.set_aspect('equal', adjustable='box')

    if save_plot:
        plt.savefig(f"{plot_type}_dimensions_{hand_name}.jpg", format='jpg')
        # name -> tuple: subj, hand  names
        print("Figure saved.")
        print(" ")


    if show_plot:
        plt.show()


def plot_single_hand(hand_name, dim_type, fig_size=7, show_plot=True, save_plot=False):
    max_list, int_list, min_list, (max_w, min_w), absmax = read_csv_measurements(hand, dim_type)

    # TODO: make sure aspect ratio looks nicely with 
    fig = plt.figure(figsize=(1.5*fig_size, 0.6*fig_size))
    ax = fig.add_subplot()

    make_dimension_plot(dim_type, hand, 
                        max_list, int_list, min_list, 
                        fig=fig, ax=ax,
                        shade_distal=True, shade_proximal=True, 
                        halve_measurements=True, y_offset=True, 
                        distal_measurement_point="midpoint",
                        abs_max=absmax, 
                        width_vals=[max_w, min_w, True],
                        show_plot=show_plot,
                        save_plot=save_plot
                        )


def save_multiple_hand_dims(hand_names, dim_types):
    for h in hand_names:
        for d in dim_types:
            plot_single_hand(h, d, show_plot=False, save_plot=True)


def plots_both_types(hand_name, fig_size=20, save_plot=False, show_plot=True):
    # TODO: make sure aspect ratio looks nicely with 
    fig = plt.figure(figsize=(1*fig_size, 0.25*fig_size)) # TODO: comes out weird with the two plots
    width_inf = True  # TODO: fix here!

    max_list, int_list, min_list, (max_w, min_w), absmax = read_csv_measurements(hand, "precision")
    ax1 = fig.add_subplot(1,2,1)
    make_dimension_plot(dim_type, hand, 
                        max_list, int_list, min_list, 
                        fig=fig, ax=ax1,
                        shade_distal=True, shade_proximal=True, 
                        halve_measurements=True, y_offset=True, 
                        distal_measurement_point="midpoint",
                        abs_max=absmax, 
                        width_vals=[max_w, min_w, width_inf], # TODO: build width_inf into csv file
                        show_plot=False,
                        save_plot=False
                        )  # TODO: make a text object for width

    max_list, int_list, min_list, (max_w, min_w), absmax = read_csv_measurements(hand, "power")
    ax2 = fig.add_subplot(1,2,2)
    make_dimension_plot(dim_type, hand, 
                        max_list, int_list, min_list, 
                        fig=fig, ax=ax2,
                        shade_distal=True, shade_proximal=True, 
                        halve_measurements=True, y_offset=True, 
                        distal_measurement_point="midpoint",
                        abs_max=absmax, 
                        width_vals=[max_w, min_w, width_inf], 
                        show_plot=False,
                        save_plot=False
                        )

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


if __name__ == '__main__':
    # options: precision, power
    dim_type = "precision"
    # options: barrett, human, jaco2, mO_cylindrical, mO_spherical, mt42, robotiq2f85
    hand = "barrett"

    # max_list, int_list, min_list, (max_w, min_w), absmax = read_csv_measurements(hand, dim_type)

    # make_dimension_plot(dim_type, hand, 
    #                     max_list, int_list, min_list, 
    #                     shade_distal=True, shade_proximal=True, 
    #                     halve_measurements=True, y_offset=True, 
    #                     distal_measurement_point="midpoint",
    #                     abs_max=absmax, 
    #                     width_vals=[max_w, min_w, True],
    #                     show_plot=False,
    #                     save_plot=True
    #                     )

    #plots_both_types(hand)
    save_hands_plots(["barrett", "human", "jaco2", "mO_cylindrical", "mO_spherical", "mt42", "robotiq2f85"])

    # TODO: plot an example object onto the plot


    # # TODO: plot an example object onto the plot
