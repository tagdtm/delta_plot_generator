from delta_plot import Delta_plot
import get_data_c

if __name__ == "__main__":
    pic1 = "baseline.png"
    pic2 = "comparison.png"
    dplot = Delta_plot(pic1,pic2)
    width, height = dplot.get_size(pic1)

    R1, G1, B1 = dplot.get_RGB(pic1,height,width)
    R2, G2, B2 = dplot.get_RGB(pic2,height,width)

    colormap = "Colormap_recipe.csv"
    datasize = 101
    data_r, R_reference, G_reference, B_reference = dplot.color_reference(colormap, datasize)
    data, data2 = get_data_c.get_data_cython(R1,R2,G1,G2,R_reference,G_reference,data_r,height,width)
    data_delta = dplot.data_delta(25,data,data2,height,width)

    figname = "test.jpg"
    dplot.fig_plot(data_delta, figname, height, width)

