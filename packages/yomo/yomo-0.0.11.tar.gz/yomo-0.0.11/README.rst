==========
Yo Modules
==========

Python 3 modules for atmospheric research, especially airborne sunphotometry. 

Yo comes from the Japanese word for the Sun.

.. moduleauthor:: Yohei Shinozuka <Yohei.Shinozuka@nasa.gov>

Examples:
from yomo import assemble, Look
with assemble(r'c:\data\source\AIRHOUSEKEEPING\Hskping_P3_20160910_R0.ict') as dataset:
    with Look(dataset, 'time', 'Relative_Humidity') as lk0:
        pass
