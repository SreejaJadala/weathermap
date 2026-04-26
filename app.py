import streamlit as st
import requests as req

st.set_page_config(page_title="Weather Advisor", layout="centered")

st.title("🌧️🌤️ Smart Weather Advisor")

city = st.text_input("Enter City Name")

if st.button("Get Suggestions"):

    api_key = st.secrets["OPENWEATHER_API_KEY"]
    # url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    weather_res = req.get(url)

    if weather_res.status_code == 200:
        weather_data = weather_res.json()


        temp_celsius = weather_data["main"]["temp"]
        st.subheader("🌡️ Current Weather")
        st.write(f"Temperature: {temp_celsius} °C")
        st.write(f"Humidity: {weather_data['main']['humidity']}%")
        st.write(f"Condition: {weather_data['weather'][0]['description']}")

        prompt = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"""Using this weather data: {weather_data}

Suggest:
1. What clothes to wear
2. What food is good in this weather
3. Health tips

Format:
Clothing:
Food:
Health Tips:"""
                        }
                    ]
                }
            ]
        }

        headers = {
            "x-goog-api-key": st.secrets["GEMINI_API_KEY"],
            "Content-Type": "application/json"
        }

        res = req.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
            json=prompt,
            headers=headers
        )

        output = res.json()

        result = output["candidates"][0]["content"]["parts"][0]["text"]

        st.subheader("🤖 Suggestions")
        st.success(result)

    else:
        st.error("City not found ❌")

