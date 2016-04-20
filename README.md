# GPyM
GPyM [dʒi:pi:ɜm / gee pee em] is a GPM (Global Precipitation Mission) Python Module.

### Import data
```sh
from cf2.io.GPM import GPMi
```
### To read the data
For DPR:
```sh
prjName = "GPM.DPR"
prdLv   = "L2"
prdVer  = "03"
varName = "NS/SLV/precipRateESurface"
```
For GMI:
```sh
prjName = "GPM.GMI"
prdLv   = "L2"
prdVer  = "03"  
varName = "S1/surfacePrecipitation"
```
### To load the orbit data
```sh
gpm = GPM(prjName, prdLv, prdVer)
```
After establishing a start time and an end time with the function datetime (sDTime, eDTime), the domain, resolution, and ???
```sh
gpmJP   = gpm('NS/SLV/precipRateESurface', sDTime, eDTime, BBox, res, delT )
```
The global data of GPM:
>obt   = gpm(varName, sDTime, eDTime, [[-89.99,-180.0],[89.99,179.99]])



