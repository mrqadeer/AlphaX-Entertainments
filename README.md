# AlphaX Entertainments

Welcome to the Hugging Face Model Showcase app! This app demonstrates the power and versatility of Hugging Face models across multiple domains, including NLP, Audio, Computer Vision and Multimodal. The app utilizes models offering serverless APIs for seamless responses.
## Deployment
### On Streamlit Cloud
Check it out [AlphaX Entertainments](https://alphax-entertainments.streamlit.app/)
### On Render
Check it out [AlphaX Entertainments](https://alphax-entertainments.streamlit.app/)
## Table of Contents

- [AlphaX Entertainments](#alphax-entertainments)
  - [Deployment](#deployment)
    - [On Streamlit Cloud](#on-streamlit-cloud)
    - [On Render](#on-render)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Features](#features)
    - [Limitations](#limitations)
  - [Contributing](#contributing)
      - [Documenation](#documenation)
  - [License](#license)

## Installation

1. Clone the repository:
   Open your terminal and run command

   ```
   git clone https://github.com/mrqadeer/AlphaX-Entertainments
   ```
2. Go to the project folder
   ```bash 
   cd AlphaX-Entertainments
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   ```
   Activate on Windows
   ```bash
   env\Scripts\activate
   ```
   Activate on Linux/Mac
   ```bash
   source env/bin/activate
   ```
If you are using Conda, you can create a conda environment and activate it:
```bash
conda create --name env
conda activate env
```
1. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the application:

   ```
   streamlit run app.py
   ```
2. If your streamlit app doesn't open in your web browser then go to ```http://localhost:8501``` 
to access the app.
1. Provide OpenAI API Key to get your access key follow the link [OpenAI API Key](https://platform.openai.com/account/api-keys)
2. Close the Sign In dialog and navigate to ```Try AlphaX``` 
3. Select the desired option and click on ```Try AlphaX```
- **Note**: You need to have OpenAI API key which provides you access to the model ```gpt-4o```
## Features
- **Text Processing**: Analyze and manipulate text inputs.
- **Image Handling**: Upload and process images for recognition tasks.
- **Audio Processing**: Record and analyze audio files.
- **Video Processing**: Handle video inputs with functionality for analysis and recognition.
- **User-Friendly Interface**: Built with Streamlit for easy navigation and usage.

### Limitations
- Poor respose for Lollywood Media.
- Needs to improve by fine tuning model.
## Contributing

We welcome contributions! Please read [Contribution](CONTRIBUTE.md) file for more detail.

#### Documenation
For documentation, please refer to the [AlphaX Entertainments Documentation](https://mrqadeer.github.io/AlphaX-Entertainments/index.html)


## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.