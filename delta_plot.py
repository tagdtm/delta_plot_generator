from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from mpl_toolkits.axes_grid1 import Divider, Size 
from mpl_toolkits.axes_grid1.mpl_axes import Axes 
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import csv

class Delta_plot:
    """
    This class provides function set to plot scalor delta plot.
    The user should provide the colormap data, used in the picture in csv format.

    """
    def __init__(self,pic1: str,pic2: str):
        """
        Args:
            pic1 (str): directory of baseline picture
            pic2 (str): directory of compared picture
        """
        self.pic1 = pic1
        self.pic2 = pic2

    def get_size(self,pic):
        img = Image.open(pic)
        width,height = img.size

        return width, height

    def get_RGB(self,pic,height,width):
        img = Image.open(pic)
        R = np.zeros((height,width),dtype=int)
        G = np.zeros((height,width),dtype=int)
        B = np.zeros((height,width),dtype=int)

        for y in range(height):
            for x in range(width):
                R[y,x],G[y,x],B[y,x] = img.getpixel((x, y))

        return R,G,B

    def color_reference(self,colormap:str,datasize: int):
        """
        Convert csv data to ndarray
        Args:
            colormap (str): directory of colormap csv file
            datasize (int): how many data does the file include for each column

        Returns:
            _type_: return RGB value correspond to the normalised scalor
        """
        R_reference = np.zeros(datasize, dtype = int)
        G_reference = np.zeros(datasize, dtype = int)
        B_reference = np.zeros(datasize, dtype = int)
        data_r = np.zeros(101, dtype = int)

        i = 0

        # STARCCM+ colormap reference
        with open(colormap, 'r', encoding='utf-8') as fin:
            reader = csv.reader(fin)

            for row in reader:
                data_r[i] = row[0] 
                R_reference[i] = row[1]
                G_reference[i] = row[2]
                B_reference[i] = row[3]
                i += 1
        return data_r, R_reference, G_reference, B_reference

    def data_delta(self, data_range:int,data,data2,height,width):
        """
        calculate data delta

        Args:
            data_range (int): colormap range. If the colormap range is -1 to 3, input will be 4
            data (_type_): scalor data that is used as baseline
            data2 (_type_): scalor data that user wants to compare with

        Returns:
            _type_: dataset is provided
        """
        data_delta = (data2-data)/data_range
        # copy the data to the both side
        for y in range(1, int(height/2)):
            for x in range(1, width):
                #if data_delta[y,x] == 0:
                    #data_delta[y,x] = 100
                data_delta[height-y,x] = data_delta[y,x] 

        return data_delta

    def my_colormap(self,colors,uc = 'white',oc = 'white'):
        """
        User can use the colormap

        Args:
            colors (_type_): _description_
            uc (str, optional): _description_. Defaults to 'white'.
            oc (str, optional): _description_. Defaults to 'white'.
        """
        cmap = LinearSegmentedColormap.from_list('custom',colors)
        cmap.set_under(uc)
        cmap.set_over(oc)

    def fig_plot(self,data_delta, figname: str,height:int, width:int, dpi = 100, cmap = "seismic",vmin = -1, vmax = 1):
        """ 
        This function gives plot whose region is exactly the same size as the given picture

        Args:
            data_delta (any): given RGB data is plotted 
            figname (str): give filename + file format, i.e. mypic.jpg
            dpi (int, optional): _description_. Defaults to 100.
            cmap (str, optional): _description_. Defaults to "seismic".
            vmin (int, optional): _description_. Defaults to -1.
            vmax (int, optional): _description_. Defaults to 1.
        """
        # designate size
        ax_w_px = width  # plot width (pixcel)
        ax_h_px = height  # plot height (pixel)

        ax_w_inch = ax_w_px / dpi
        ax_h_inch = ax_h_px / dpi
        ax_margin_inch = (0.5, 0.5, 0.5, 0.5)  # Left,Top,Right,Bottom [inch]

        fig_w_inch = ax_w_inch + ax_margin_inch[0] + ax_margin_inch[2] 
        fig_h_inch = ax_h_inch + ax_margin_inch[1] + ax_margin_inch[3]

        fig = plt.figure( dpi=dpi, figsize=(fig_w_inch, fig_h_inch))
        ax_p_w = [Size.Fixed(ax_margin_inch[0]),Size.Fixed(ax_w_inch)]
        ax_p_h = [Size.Fixed(ax_margin_inch[1]),Size.Fixed(ax_h_inch)]
        divider = Divider(fig, (0.0, 0.0, 1.0, 1.0), ax_p_w, ax_p_h, aspect=False)
        ax = Axes(fig, divider.get_position())
        ax.set_axes_locator(divider.new_locator(nx=1,ny=1))
        fig.add_axes(ax)

        # plot
        #im = ax.imshow(data_delta,cmap = cmap,vmin=-1, vmax=1)
        im = ax.imshow(data_delta,cmap = cmap,vmin=vmin, vmax=vmax)
        fig.colorbar(im,aspect = 40, pad = 0.08, shrink = 0.6, orientation="horizontal")
        plt.savefig(figname)



    