from nilearn import plotting
from IPython import display


def display_input(nifti, i, fig, ax, cut_coords=None):
    if cut_coords is None:
        cut_coords = [-9]
    plotting.plot_img(nifti, title="In {}".format(i), axes=ax,
                      display_mode="z", cut_coords=cut_coords)
    display.clear_output(wait=True)
    display.display(fig)


def display_output(nifti, i, fig, ax, cut_coords=None):
    if cut_coords is None:
        cut_coords = [-9]
    ax.clear()
    plotting.plot_img(nifti, title="Out {}".format(i), axes=ax,
                      display_mode="z", cut_coords=cut_coords)
