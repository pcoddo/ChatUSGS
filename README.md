<!-- Header -->
![Header](https://raw.githubusercontent.com/pcoddo/ChatUSGS/main/img/example.PNG)

# **ChatUSGS**
</p>
<p align="left">
    <em>Simple chat interface to access data using USGS Graph Image API and OpenAI GPT-3.5</em>
</p>

<!-- Badges -->
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/pcoddo/ChatUSGS?include_prereleases)
![GitHub last commit](https://img.shields.io/github/last-commit/pcoddo/ChatUSGS)
![GitHub](https://img.shields.io/github/license/pcoddo/ChatUSGS)

---

## About
Chat interface featuring Gradio front-end that allows users to request real-time hydrometeorological condtions through the USGS [Water Data for the Nation](https://waterdata.usgs.gov/nwis) platform. Designed to allow plain language requests for water conditions (water levels, discharge, water quality), air temperature, precipitation, and windspeed. Requests are parsed using the OpenAI [GPT-3.5 Language Model](https://platform.openai.com/docs/models/gpt-3-5) and return results based on specified location and time frame.


## Installation
### <u>OpenAI Setup:</u>
1. Sign up for an [OpenAI account](https://platform.openai.com/)
2. Create secret [API Key](https://platform.openai.com/account/api-keys) and save to device

### <u>Code Installation</u>
Clone repository to your device:
```shell
git clone https://github.com/pcoddo/ChatUSGS.git
```
Install required packages using pip or environment manager:
```shell
pip install gradio

conda install -c conda-forge gradio
```

### <u>Dependencies</u>
**Python** version 3.9+

**Packages:**
  - argparse
  - gradio
  - pandas
  - pickle
  - urllib
  - requests
  
## Usage
### <u>Update code with OpenAI API Key</u>
Insert your private key on Line 26 in `backend.py`

### <u>Running script</u>
Navigate to ChatUSGS directory:
```shell
cd path\to\ChatUSGS
```
Run `app.py` script using command line or Python IDE:
<p align="center">
  <img src="https://raw.githubusercontent.com/pcoddo/ChatUSGS/main/img/run.png" width="600">
</p>

Click local URL to open app in browser:
<p align="center">
  <img src="https://raw.githubusercontent.com/pcoddo/ChatUSGS/main/img/open.png" width="600">
</p>

In chat window, enter your prompt. GPT-3.5 will attempt to parse requests for observation of interest (e.g. flooding, water quality, weather), location, and time period. Example prompts and outputs are as follows:

<p align="center">
  <img src="https://raw.githubusercontent.com/pcoddo/ChatUSGS/main/img/prompts.PNG" width="1000">
</p>

Outputs are passed to the USGS [Graph Image API](https://labs.waterdata.usgs.gov/about-graph-image-api/index.html). Requests for data are currently limited to the following USGS parameters:

| Parameter        | Unit                  | Code  |
| ---------------- | --------------------- | ----- |
| Gage Height      | Feet                  | 00065 |
| Air Temperature  | Degree Fahrenheit     | 00021 |
| Dissolved Oxygen | Milligrams per Liter  | 00030 |
| Wind Speed       | Miles per Hour        | 00035 |
| Precipitation    | Inches                | 00045 |
| Streamflow       | Cubic Feet per Second | 00060 |

## License
[MIT License](https://opensource.org/licenses/MIT)

## Questions?
**Contact:** [Perry Oddo](https://perryoddo.com/#contact)


<p align="center">
  <a href="#chatusgs">(Back to top)</a>
</p>