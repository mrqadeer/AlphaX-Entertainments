App Module
==========

The `app` module is the main entry point for the Streamlit application, `AlphaX Entertainments`. It configures the application layout, handles user interactions, and manages different content display based on user choices.

**Key Components**

1. **CSS Loading**
   The `load_css` function loads and injects custom CSS into the Streamlit app to style the application interface.

2. **Main Function**
   The `main` function is the core of the application. It initializes the user interface, handles sidebar menu options, and directs user input to the appropriate handlers.

3. **Sidebar Menu**
   The sidebar provides navigation options:
   - **Home**: Displays the main content of the application.
   - **Credentials**: Allows users to input their OpenAI API key.
   - **Try AlphaX**: Provides functionality for text, image, audio, and video processing.

4. **Handlers**
   Based on user selection, the application invokes different handlers:
   - **Text Handler**: Processes text input.
   - **Image Handler**: Processes image input.
   - **Audio Handler**: Processes audio input.
   - **Video Handler**: Processes video input.

5. **Footer**
   A footer with social media links is added to connect users with the developers and the project.

Usage
------

Here is how you can use the `app` module:

**1. Running the Application**

To start the Streamlit application, execute the following command:

```bash
streamlit run app.py
