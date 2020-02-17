# Python access to snow depth data from MountainHub API

Simplified and standardized access to snow depth data from the [MountainHub](https://about.mountainhub.com/) API, 
[https://api.mountainhub.com/timeline](https://api.mountainhub.com/timeline).

Adapted from [MountainHub.py module](https://github.com/communitysnowobs/validation/blob/master/validation/MountainHub.py) 
in the [validation](https://github.com/communitysnowobs/validation) GitHub repository from the 
[Community Snow Observations (CSO)](http://communitysnowobs.org/) Citizen Science project.

See [Jupyter notebook example]() for usage, and [api.mountainhumb.com_timeline.sample.json](api.mountainhumb.com_timeline.sample.json) 
for an example of the API JSON response.

## Installation 

If the dependencies installed (`pandas` and `requests`), `mtnhubsnow` can be installed with `pip install`:
```bash
pip install git+https://github.com/communitysnowobs/mountainhub-api.git
``` 

Otherwise, the `cso_environment.yml` conda environment file can be used. It will additionally install 
`matplotlib`, `geopandas` and `folium`.
```bash
wget https://raw.githubusercontent.com/communitysnowobs/mountainhub-api/master/cso_environment.yml
conda env create -f cso_environment.yml
```

### For development
```bash
git clone https://github.com/communitysnowobs/mountainhub-api.git
cd mountainhub-api
conda env create -f environment.yml
source activate mtnhubsnow
pip install -e .
# To be able to select conda environments in JupyterLab, install ipykernel
conda install ipykernel
```
