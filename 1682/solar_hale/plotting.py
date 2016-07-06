import numpy as np
import matplotlib.pyplot as plt
from gpkit.small_scripts import unitstr

def poor_mans_contour(model, xvarname, xsweep, zvarname, zsweep, yvarname,
                      ylimits, vref=None, vrefname=None, href=None,
                      hrefname=None):

    # save sold substitions substitute
    x_old = model.substitutions[xvarname]
    z_old = model.substitutions[zvarname]

    # substitute in new variables
    model.substitutions.update({xvarname: ("sweep", xsweep)})

    # create figure
    fig, ax = plt.subplots()
    lines = []

    # iterate through z variables
    for val in zsweep:
        model.substitutions.update({zvarname: val})
        sol = model.solve("mosek", skipsweepfailures=True)

        l, = ax.plot(sol(xvarname), sol(yvarname),
                     label="%s: %s" % (zvarname, val))
        lines.append(l)

    # return substitution values to what they were
    model.substitutions.update({xvarname: x_old})
    model.substitutions.update({zvarname: z_old})

    # format plot
    ax.set_xlabel("%s [%s]" % (model[xvarname].descr["label"],
                               unitstr(model[xvarname].units)))
    ax.set_ylabel("%s [%s]" % (model[yvarname].descr["label"],
                               unitstr(model[yvarname].units)))
    ax.set_ylim((ylimits[0], ylimits[1]))
    if vref:
        l, = ax.plot([vref, vref], ylimits, "r--", label=vrefname)
        lines.append(l)
    if href:
        l, = ax.plot([xsweep[0], xsweep[-1]], [href, href], "r--",
                     label=hrefname)
        lines.append(l)

    plt.legend(handles=lines)
    plt.grid()

    return fig, ax
