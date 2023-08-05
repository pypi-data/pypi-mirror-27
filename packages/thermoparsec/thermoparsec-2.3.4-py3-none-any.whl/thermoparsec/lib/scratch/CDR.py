from lib.componentdetection.CD import *
from pyspark.sql import SparkSession

from lib.scratch.PPD import *

spark = SparkSession.builder. \
    appName("ParsecSparkDemo"). \
    config("spark.master", "local[*]"). \
    getOrCreate()

def MapPeak(t,w):
    p = PPD(t[1],w)
    return (t,p)


data = spark.read.json("data/json"). \
     rdd.map(lambda scan: CreateKVpair(scan,1)). \
     flatMap(lambda scan: MapMzListForScan(scan)). \
     map(lambda mz: KeyMz(mz)). \
     groupByKey().flatMap(lambda file: KeyTraces(file)). \
     collect()#map(lambda t: MapPeak(t)).collect()







#KeyTraces(data[0])
#t = MapPeak(data[288],.1)
r = PPD(data[288][1],.1)
s = 1




