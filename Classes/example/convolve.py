import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import deconvolve
x = np.arange(-6,6,0.1)

gauss = np.exp(-(x**2)/0.5)
flat = np.ones(x.shape)*0.25
slope = x/6

plt.plot(x,gauss,label="gauss")
plt.plot(x,flat,label="flat")
plt.plot(x,slope,label="slope")

plt.plot(x,gauss*gauss,'--',label="gauss*gauss")
plt.plot(x,gauss*flat,'--',label="gauss*flat")
plt.plot(x,gauss*slope,'--',label="gauss*slope")

plt.legend()

plt.show()



pieces = [flat, gauss+0.25, slope-np.min(slope)+0.25]

for i in range(3):
    plt.subplot(131+i)
    plt.plot(x,pieces[i])
    plt.plot(x,gauss*pieces[i],'--')
    plt.ylim((0,2.5))

plt.show()




fn = np.concatenate(pieces)
con, r = deconvolve(fn,gauss)

plt.plot(fn)
plt.plot(con,'--')
plt.show()


gauss2 = np.exp(-(np.arange(-0.5,0.5,0.1)**2)/0.5)
con = np.convolve(fn,gauss2,mode="same")

plt.plot(fn)
plt.plot(con,'--')
plt.show()

squiggle = -gauss2*np.sign(np.arange(-0.5,0.5,0.1))

con = np.convolve(fn,squiggle,mode="same")

plt.plot(fn)
plt.plot(con,'--')
plt.plot(plt.xlim(),[0,0],'k')
plt.show()