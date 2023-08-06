#!python
# -*- coding:utf-8 -*-

import ca
import gc,resource
import matplotlib.pyplot as pyplot
import scipy

pyplot.interactive(True)

x=x=scipy.linspace(-1,1,1024)*2*scipy.pi

y=scipy.sin(x)
z=scipy.cos(x)

ch=ca.channel("myWF")
ch.flush()
ch.wait_conn(10)

def test(N=1000):
    pyplot.clf()
    gc.collect()
    def cb(*args,**kw):
        gc.collect()
    xdata=[0]
    ru_self=[resource.getrusage(resource.RUSAGE_SELF),]
    ru_chil=[resource.getrusage(resource.RUSAGE_CHILDREN),]
    ru_self.append(resource.getrusage(resource.RUSAGE_SELF))
    ru_chil.append(resource.getrusage(resource.RUSAGE_CHILDREN))
    xdata.append(1)
    ru_self.append(resource.getrusage(resource.RUSAGE_SELF))
    ru_chil.append(resource.getrusage(resource.RUSAGE_CHILDREN))
    xdata.append(2)
    for i in range(N):
        ch.put(*y)
        ch.flush()
        ch.put(*z)
        ch.flush()
        gc.collect()
        gc.get_count()
        if ((i % 100) == 0):
            pyplot.plot([r.ru_maxrss for r in ru_self])
            pyplot.plot([r.ru_maxrss for r in ru_chil])
    ru_self.append(resource.getrusage(resource.RUSAGE_SELF))
    ru_chil.append(resource.getrusage(resource.RUSAGE_CHILDREN))
    xdata.append(N)
    pyplot.plot(xdata, [r.ru_maxrss for r in ru_self])
    pyplot.plot(xdata, [r.ru_maxrss for r in ru_chil])

    print [r.ru_maxrss for r in ru_self]
    pyplot.show(True)
    

if __name__ == "__main__":
    test(4*1000)
