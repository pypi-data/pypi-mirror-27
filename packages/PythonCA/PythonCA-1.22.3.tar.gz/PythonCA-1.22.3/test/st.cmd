#!/opt/epics/base/bin/darwin-x86/softIoc
## Register all support components

dbLoadDatabase("/opt/epics/base/dbd/softIoc.dbd")
#wfexample_registerRecordDeviceDriver(pdbbase)

dbLoadTemplate("excas.substitutions","")
dbLoadRecords("./test.db")

iocInit()

