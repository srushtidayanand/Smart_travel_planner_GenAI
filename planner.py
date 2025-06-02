import requests
import os
import json
from datetime import datetime, timedelta, date
import streamlit as st

HUGGINGFACE_API_TOKEN = ""  
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}

def generate_ai_response(prompt, max_tokens=1000, temperature=0.7):
    """Generic function to interact with the AI model"""
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.9,
            "do_sample": True
        }
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict):
            full_text = result[0].get("generated_text", "❌ No generated text found.")
            cleaned_text = full_text.replace(prompt, "").strip()
            return cleaned_text
        elif isinstance(result, dict) and "error" in result:
            return f"❌ API Error: {result['error']}"
        else:
            return "❌ Unexpected response format from the model."
    except requests.exceptions.RequestException as e:
        return f"❌ Network error: {str(e)}"

def parse_date(date_input):
    """Parse date string or datetime.date into a datetime object"""
    if isinstance(date_input, datetime):
        return date_input
    elif isinstance(date_input, date):
        return datetime.combine(date_input, datetime.min.time())
    elif isinstance(date_input, str):
        try:
            return datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            return None
    return None


def generate_itinerary(destination, start_date, end_date, interests, budget, travelers):
    """Generate a comprehensive travel itinerary"""
    start = parse_date(start_date)
    end = parse_date(end_date)

    if not start or not end:
        return "❌ Invalid date format. Please use YYYY-MM-DD format."

    if end < start:
        return "❌ End date must be after start date."

    days = (end - start).days + 1

    try:
        budget_per_person = float(budget) / int(travelers)
        budget_daily = budget_per_person / days
    except (ValueError, ZeroDivisionError):
        return "❌ Invalid budget or travelers count."

    prompt = f"""
    You are an expert travel assistant. Create a detailed {days}-day itinerary for a trip to {destination}.

    Trip Details:
    - Travel dates: {start_date} to {end_date}
    - Number of travelers: {travelers}
    - Total budget: {budget} (approximately {budget_daily:.2f} per person per day)
    - Interests: {interests}

    For each day, provide:
    1. Recommended activities and attractions with estimated costs
    2. Meal suggestions with price ranges
    3. Transportation options

    Format each day as follows:

    ## Day X: {start.strftime('%A, %B %d')} (adjust date for each day)

    ### Morning:
    - Activity: [Activity name] - [Estimated cost]
    - [Brief description]

    ### Afternoon:
    - Activity: [Activity name] - [Estimated cost]
    - [Brief description]

    ### Evening:
    - Activity: [Activity name] - [Estimated cost]
    - [Brief description]

    ### Meals:
    - Breakfast: [Suggestion] - [Price range]
    - Lunch: [Suggestion] - [Price range]
    - Dinner: [Suggestion] - [Price range]

    ### Transportation:
    - [Options with costs]

    ### Daily Budget Summary:
    - Activities: $X
    - Food: $X
    - Transportation: $X
    - Total: $X (remaining budget for the trip: $X)

    Make the trip enjoyable, include specific places, and keep it realistic within the budget constraints.
    """

    print("\nGenerating your personalized itinerary... Please wait...\n")
    return generate_ai_response(prompt, max_tokens=2000)

def generate_packing_list(destination, start_date, end_date, activities):
    """Generate a personalized packing list"""
    start = parse_date(start_date)
    end = parse_date(end_date)

    if not start or not end:
        return "❌ Invalid date format. Please use YYYY-MM-DD format."

    days = (end - start).days + 1

    prompt = f"""
    You are a travel packing expert. Create a comprehensive packing list for a {days}-day trip to {destination} from {start_date} to {end_date}.

    The traveler will be participating in these activities: {activities}

    Organize the packing list into these categories:
    1. Essential Documents
    2. Clothing (appropriate for the destination and season)
    3. Toiletries
    4. Electronics
    5. Activity-specific gear (based on the mentioned activities)
    6. Medications and First Aid
    7. Miscellaneous items

    For each item, indicate:
    - If it's essential or optional
    - Recommended quantity
    - Any special notes (e.g., "keep in carry-on")

    Format your response as a clear, well-organized list that is easy to reference.
    """

    print("\nGenerating your personalized packing list... Please wait...\n")
    return generate_ai_response(prompt)

def generate_budget_breakdown(destination, days, budget, travelers):
    """Generate a budget breakdown"""
    try:
        total_budget = float(budget)
        num_travelers = int(travelers)
        num_days = int(days)
    except ValueError:
        return "❌ Invalid budget, travelers, or days value."

    prompt = f"""
    You are a travel budget expert. Create a detailed budget breakdown for a {days}-day trip to {destination} for {travelers} traveler(s) with a total budget of {budget}.

    Provide a realistic allocation of funds across these categories:
    1. Accommodation (hotels, Airbnb, etc.)
    2. Transportation (flights, local transit, car rental)
    3. Food and drinks (daily breakdown)
    4. Activities and attractions
    5. Shopping and souvenirs
    6. Emergency fund (recommend 10-15% of total)

    For each category:
    - Provide estimated costs
    - Suggest budget-friendly alternatives where applicable
    - Include specific examples relevant to {destination}

    Also include:
    - Daily budget per person
    - Money-saving tips specific to this destination
    - Payment methods and currency considerations

    Format as a clear, itemized budget plan.
    """

    print("\nGenerating your budget breakdown... Please wait...\n")
    return generate_ai_response(prompt)

def save_trip_plan(trip_data):
    """Save trip plan to a JSON file"""
    filename = f"trip_to_{trip_data['destination']}_{trip_data['start_date']}.json"

    save_data = {k: v for k, v in trip_data.items() if k not in ['itinerary', 'packing_list', 'budget_breakdown']}

    try:
        with open(filename, 'w') as f:
            json.dump(save_data, f, indent=4)
        return f"✅ Trip details saved to {filename}"
    except Exception as e:
        return f"❌ Failed to save trip details: {str(e)}"

def load_trip_plan(filename):
    """Load trip plan from a JSON file"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except Exception as e:
        return f"❌ Failed to load trip details: {str(e)}"

def get_destination_info(destination):
    """Get basic information about the destination"""
    prompt = f"""
    You are a travel expert. Provide a brief overview of {destination} as a travel destination.
    Include:
    1. A short description of the location
    2. Best times to visit
    3. Major attractions
    4. Local customs and etiquette travelers should know
    5. Common languages spoken
    6. Currency used
    7. Any travel advisories or safety tips

    Keep your response concise but informative.
    """

    print(f"\nGetting information about {destination}... Please wait...\n")
    return generate_ai_response(prompt)

st.set_page_config(page_title="Smart Travel Planner", layout="wide")
st.title("🌍 Smart Travel Planner - AI-Powered Travel Assistant")

tab1, tab2, tab3, tab4 = st.tabs(["🧳 Itinerary", "📦 Packing List", "📍 Destination Info", "💸 Budget Planner"])

with tab1:
    st.subheader("Create Custom Itenary")
    destination = st.text_input("Destination")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.today())
    with col2:
        end_date = st.date_input("End Date", datetime.today() + timedelta(days=5))
    travelers = st.number_input("Number of Travelers", min_value=1, step=1)
    budget = st.text_input("Total Budget (USD)", "1000")
    interests = st.text_area("Travel Interests (e.g., museums, beaches, adventure)")

    if st.button("Generate Itinerary"):
        if destination and start_date and end_date and travelers and budget and interests:
            with st.spinner("Generating itinerary..."):
                result = generate_itinerary(destination, parse_date(start_date), parse_date(end_date), interests, budget, travelers)
                st.markdown("### 🗓️ Your Itinerary")
                st.markdown(result)
        else:
            st.warning("Please fill all fields to generate the itinerary.")

with tab2:
    st.subheader("Generate a Packing List")
    destination2 = st.text_input("Destination", key="dest2")
    start_date2 = st.date_input("Start Date", datetime.today(), key="start2")
    end_date2 = st.date_input("End Date", datetime.today() + timedelta(days=3), key="end2")
    activities = st.text_area("Planned Activities", key="act")

    if st.button("Generate Packing List"):
        if destination2 and activities:
            with st.spinner("Creating packing list..."):
                result = generate_packing_list(destination2, start_date2, end_date2, activities)
                st.markdown("### 🧳 Your Packing List")
                st.markdown(result)
        else:
            st.warning("Please enter the destination and activities.")

with tab3:
    st.subheader("Learn About a Destination")
    destination3 = st.text_input("Destination", key="dest3")
    if st.button("Get Destination Info"):
        if destination3:
            with st.spinner("Fetching info..."):
                info = get_destination_info(destination3)
                st.markdown(f"### 🗺️ About {destination3}")
                st.markdown(info)
        else:
            st.warning("Please enter a destination.")

with tab4:
    st.subheader("Plan Your Budget")
    destination4 = st.text_input("Destination", key="dest4")
    days4 = st.number_input("Trip Duration (Days)", min_value=1, value=5)
    travelers4 = st.number_input("Number of Travelers", min_value=1, value=2)
    budget4 = st.text_input("Total Budget (USD)", "2000", key="budget4")

    if st.button("Generate Budget Plan"):
        if destination4 and budget4:
            with st.spinner("Calculating budget..."):
                breakdown = generate_budget_breakdown(destination4, days4, budget4, travelers4)
                st.markdown("### 💵 Budget Breakdown")
                st.markdown(breakdown)
        else:
            st.warning("Please enter destination and budget.")
