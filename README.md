<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
    <h3 align="center">Spotify API Reader</h3>
    <p align="center">
        Little application to fetch some data from spotify API.
    </p>
</div>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

Clone the repository via git or download a zip archive.
Open your preferred terminal and change to the directory where you stored the python files.
Run this:
```sh
pip install -r requirements.txt
```
This will install all necessary libraries.

### Installation

1. Make sure your client id and client secret are in the respective fields in `main.py`
   ```python
   ...
   SPOTIPY_CLIENT_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   SPOTIPY_CLIENT_SECRET = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
   ...
   ```
2. Run the application from your terminal:
   ```console
   streamlit run main.py
   ```
3. Your terminal will show you the address the web app is using (Network URL may not be the same):
   ```console
    You can now view your Streamlit app in your browser.

    Local URL: http://localhost:8501
    Network URL: http://192.168.178.20:8501
   ```
4. If your default browser has not opened by default, open the URL from above and have fun.

<p align="right">(<a href="#readme-top">back to top</a>)</p>
