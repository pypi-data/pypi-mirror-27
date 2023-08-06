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
        ch.put(*y,dtype=ca.DBR_DOUBLE,cb=cb)
        ch.flush()
        ch.put(*z,dtype=ca.DBR_DOUBLE,cb=cb)
        ch.flush()
        gc.collect()
        gc.get_count()
        if (((i % 1000) == 0) or (i in (1,2,5,10,20,50,100,200,500,))):
            ru_self.append(resource.getrusage(resource.RUSAGE_SELF))
            ru_chil.append(resource.getrusage(resource.RUSAGE_CHILDREN))
            xdata.append(i)
    ru_self.append(resource.getrusage(resource.RUSAGE_SELF))
    ru_chil.append(resource.getrusage(resource.RUSAGE_CHILDREN))
    xdata.append(N)
    pyplot.plot(xdata, [r.ru_maxrss for r in ru_self])
    pyplot.plot(xdata, [r.ru_maxrss for r in ru_chil])
    for d in xdata:
        print d,"\t",
    print 
    for d in (r.ru_maxrss for r in ru_self):
        print d,"\t",
    print
    pyplot.show(True)
    

if __name__ == "__main__":
    test(5*1000)
