# OCO XCO2
OCO XCO2 downloads and visualises XCO2 data from NASA's Orbiting Carbon Observatory 2 ([OCO-2](https://www.nasa.gov/mission_pages/oco2/index.html)) satellite.

![OCO-2](https://www.nasa.gov/sites/default/files/styles/full_width/public/thumbnails/image/oco2.jpg?itok=pRGuPey1)

## Area of study
OCO-2 XCO2 data is processed for New Zealand during 2019.

![NZ 2019 CO2](/images/oco2-xco2-nz-2019.png)

![NZ 2019 CO2](/images/oco2-xco2-nz-2019-hist.png)

![NZ 2019 CO2](/images/oco2-xco2-nz-2019-ravg.png)

## Prerequisites
- Python https://www.python.org/downloads/
- Jupyter https://jupyter.org/install
- Conda (recommended) https://docs.conda.io/en/latest/miniconda.html
- Panoply (optionally) - requires a JRE https://www.giss.nasa.gov/tools/panoply/download/

## Running
- `oco_xco2_download.ipynb` to download OCO-2 files from the NASA Goddard Earth Sciences (GES) Data and Information Services Center (DISC), ~ 20GB. 
- `oco_xco2_analysis.ipynb` to read the files and generate the plots above.

## Credits
- SIF tools https://github.com/cfranken/SIF_tools
