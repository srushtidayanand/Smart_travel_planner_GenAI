# Smart-Travel-Planner
A smart travel planner that uses hugging face to generate itinerary with streamlit as the frontend
---

# Smart Travel Planner - AI-Powered Travel Assistant

## Overview
The **Smart Travel Planner** is a web application built using Streamlit and powered by Hugging Face's Mixtral-8x7B-Instruct-v0.1 model. It allows users to generate personalized travel itineraries, packing lists, destination information, and budget breakdowns using AI. The system takes inputs like destination, travel dates, budget, and interests to create tailored travel plans. It offers an interactive user interface for easy and dynamic interactions.

## Features
- **Itinerary Generation**: Create a day-by-day travel itinerary, including activities, meals, and transportation options, while staying within your specified budget.
- **Packing List Creation**: Generate a comprehensive packing list based on your travel duration and planned activities.
- **Destination Information**: Get detailed information about a destination, including major attractions, local customs, safety tips, and language/currency details.
- **Budget Breakdown**: Get a detailed budget allocation for accommodation, transportation, food, activities, and emergency funds, based on your total budget and trip duration.

## Technologies Used
- **Streamlit**: For building the web application and user interface.
- **Hugging Face Transformers API**: For generating natural language responses using the Mixtral-8x7B-Instruct-v0.1 model.
- **Python Libraries**:
  - `requests`: For making API requests to Hugging Face.
  - `datetime`: For handling date and time inputs.
  - `json`: For saving and loading trip plans.
  - `os`: For handling file operations.

## Installation

### Prerequisites
Make sure you have Python 3.7+ installed.

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/smart-travel-planner.git
   cd smart-travel-planner
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Hugging Face API token:
   - Go to [Hugging Face](https://huggingface.co) and create an account (if you don't have one).
   - Obtain your API token from [Settings > Access Tokens](https://huggingface.co/settings/tokens).
   - Create a `.env` file in the root of the project and add your token:
     ```
     HUGGINGFACE_API_TOKEN=your_api_token
     ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open the provided local URL (typically `http://localhost:8501`) in your web browser to start using the app.

### Available Tabs:
- **Itinerary**: Generate a custom travel itinerary based on your preferences.
- **Packing List**: Generate a personalized packing list for your trip.
- **Destination Info**: Get useful information about your travel destination.
- **Budget Planner**: Generate a detailed budget breakdown for your trip.

## Example Inputs

- **Itinerary**:
  - **Destination**: Paris
  - **Start Date**: 2025-06-01
  - **End Date**: 2025-06-07
  - **Interests**: Museums, Food, Adventure
  - **Budget**: 1500 USD
  - **Travelers**: 2

- **Packing List**:
  - **Destination**: Tokyo
  - **Start Date**: 2025-07-10
  - **End Date**: 2025-07-15
  - **Activities**: Hiking, Shopping, Sightseeing

- **Budget Breakdown**:
  - **Destination**: New York
  - **Days**: 5
  - **Travelers**: 2
  - **Budget**: 3000 USD

## Future Work
- **Multi-modal Input Support**: Integrate map APIs for visualizing routes and destinations.
- **Database Integration**: Implement a cloud database to store and retrieve user trip plans.
- **Model Fine-tuning**: Fine-tune the AI model on domain-specific travel data for more accurate responses.
- **Real-time Integration**: Add support for real-time flight and hotel booking suggestions.
- **Multilingual Support**: Expand the app to support multiple languages for global users.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

You can save this content to a `README.md` file in your project directory.

Let me know if you need any modifications or additions!
