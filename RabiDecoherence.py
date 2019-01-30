from __future__ import division
import numpy
import random
import matplotlib.pyplot as pyplot
import matplotlib.colors as colors
import matplotlib.cm as cm
from matplotlib import gridspec
from matplotlib.ticker import AutoMinorLocator

#Constants

rabi_frq = 2 * numpy.pi / 100
gamma = 0.1 * rabi_frq
T_sim = 1000.0
points = 10000
Time_array = numpy.arange( 0, T_sim, ( T_sim / points ) )
dec = 1

#Functions

def Averager( T_simulation, N ):
    average = numpy.zeros( points )
    for i in range( N ):
        average = average + curve_plot( T_simulation )
    return average / N

def decay_times( T_simu ):
    Total = 0.0
    times = numpy.zeros( 1 )
    while True:
        dt = - numpy.log( numpy.random.rand() ) / gamma * 4 / 3
        if ( dt + Total ) < T_simu:
            Total = dt + Total
            times = numpy.append( times, [ Total ] )
        else:
            break
    times = numpy.append( times, [ T_simu ] )
    return times

def curve_plot( T_simul ):
    plot = numpy.zeros( points )
    T_tot = 0
    times = decay_times( T_simul )
    for i in range( len( times ) - 1 ):
        t = 0
        for j in range( int( (10 ** dec) * numpy.round( times[ i ], decimals = dec ) ), int( (10 ** dec) * numpy.round( times[ i + 1 ], decimals = dec ) ) ):
            plot[j] = numpy.sin( t * rabi_frq * 0.5 ) ** 2
            t = t + ( T_simul / points )
    return plot

def analytic():
    analytic_ary = numpy.zeros(points)
    A = 1 / ( 2 + ( gamma / rabi_frq ) ** 2 )
    B = 3 * A * gamma / ( 4 * abs( rabi_frq ** 2 - ( gamma / 4 ) ** 2 ) ** 0.5 )
    for i in range(points):
        X =  abs( rabi_frq ** 2 - ( gamma / 4 ) ** 2 ) ** 0.5 * Time_array[i] 
        analytic_ary[i] = - numpy.exp( - 3 / 4 * gamma * Time_array[i] ) * ( A * numpy.cos( X ) + B * numpy.sin( X ) ) + 1 / ( 2 + ( gamma / rabi_frq ) ** 2 )
    return analytic_ary

def residuals():
    residual = numpy.zeros( points - 1 )
    residual = ( Average[1:] - Analytic[1:] ) / Analytic[1:]
    return residual

#Function Generated Data

Average = Averager( T_sim, 10000) #N= 15000 for av%residual < 1%
Analytic = analytic()
print "The average percentage residual is {} %.".format( numpy.mean( abs( residuals() ) ) * 100 )

#Graph Stuff

pyplot.figure()
#pyplot.subplot
#pyplot.xlabel('Time (Units)')
#pyplot.ylabel('Exited State Population')
#pyplot.axis([0.0, 1000, 0.0, 1.0])
#pyplot.yticks( [ 0.0, 0.5, 1.0 ] )
#pyplot.plot( Time_array, Average, color = "red", )
#pyplot.plot( Time_array, curve_plot( T_sim ), color = "blue", linestyle = "--" )
#pyplot.plot( Time_array, Analytic, color = "green", )
#pyplot.show()

pyplot.rcParams["font.family"] = "times"
pyplot.rcParams['text.usetex'] = True
gs = gridspec.GridSpec(2,1, height_ratios=[3, 1])
fontsi = 17

pyplot.subplot(gs[0])
pyplot.axis([0.0, 1000.0, 0, 1])
#pyplot.plot(x_data, y_data, label = "Data", color = 'blue')
pyplot.plot( Time_array, Average, color = "red", label = "MCW Simulation" )
pyplot.plot( Time_array, Analytic, color = "green", label = "Analytic Solution" )
pyplot.plot( Time_array, curve_plot( T_sim ), color = "blue", label = "Typical Run") #linestyle = "--" )
pyplot.ticklabel_format(style = 'sci', scilimits = (2, 2), axis = 'y')
pyplot.setp(pyplot.subplot(gs[0]).get_xticklabels(), visible = False)
pyplot.tick_params(axis='both', which = 'both', labelsize = fontsi)
pyplot.ylabel("Exited State Population", fontsize = fontsi)
pyplot.legend(loc = "upper right", fontsize = fontsi)

pyplot.subplot(gs[1], sharex = pyplot.subplot(gs[0]))
pyplot.axis([0.0, 1000.0, -3 , 3])
pyplot.yticks([-2, -1, 0, 1, 2])
pyplot.xticks([0, 200, 400, 600, 800, 1000])
pyplot.grid(b = True, linestyle = '-', axis = 'y', which = 'major', color = 'grey', lw = 0.5, zorder =11)
pyplot.grid(linestyle = '--', axis = 'x', color = 'grey', lw = 0.5, zorder = 10)
pyplot.axhline(y = 1., color = 'grey', linestyle = '-', lw = 0.5, zorder = 5)
pyplot.axhline(y = -1., color = 'grey', linestyle = '-', lw = 0.5, zorder = 4)
#pyplot.axhline(y = 6., color = 'grey', linestyle = '-', lw = 0.5, zorder = 6)
#pyplot.axhline(y = -6., color = 'grey', linestyle = '-', lw = 0.5, zorder = 7)
#pyplot.axhline(y = 8., color = 'grey', linestyle = '-', lw = 0.5, zorder = 8)
#pyplot.axhline(y = -8., color = 'grey', linestyle = 0.1, zorder = 2)
#pyplot.axhspan(2., 4., color = 'yellow', alpha = 0.1, zorder =3)
pyplot.axhspan(-1., 1., color = 'blue', alpha = 0.1, zorder = 1)
pyplot.scatter(Time_array[ 1: ], 100 * residuals(), color = 'black', label = 'Tube A', zorder = 12, marker = 'x')
pyplot.tick_params(axis='both', which = 'both', labelsize = fontsi)
pyplot.ylabel("Percentage\nResiduals", fontsize = fontsi)
pyplot.xlabel("Time (1/100 Rabi Period)", fontsize = fontsi)

pyplot.subplots_adjust(hspace = .0)
pyplot.show()