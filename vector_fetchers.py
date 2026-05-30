import yfinance as yf
import requests
import datetime
import os
import xml.etree.ElementTree as ET

class VectorFetchers:
    def __init__(self, senses_module):
        # We connect the Fetchers to the Senses so V.E.C.T.O.R. can speak the results
        self.senses = senses_module
        
        # Pulls the weather key from your secret .env file
        self.weather_api_key = os.getenv("OPENWEATHER_API_KEY")

    def get_time_and_date(self):
        """Reads the computer's internal clock and speaks it naturally."""
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p") 
        current_date = now.strftime("%A, %B %d") 
        return f"It is currently {current_time} on {current_date}."

    def get_price(self, symbol):
        """Fetches the live price of a stock or cryptocurrency."""
        if self.senses:
            self.senses.speak(f"Fetching current market data for {symbol}...")
        
        try:
            asset = yf.Ticker(symbol)
            current_price = asset.history(period="1d")['Close'].iloc[-1]
            formatted_price = round(current_price, 2)
            
            return f"The current price of {symbol} is {formatted_price}."
        
        except Exception:
            return f"I apologize, but I could not find the market data for {symbol}."

    def get_weather(self, city):
        """Connects to OpenWeather API with an automatic backup system."""
        if self.senses:
            self.senses.speak(f"Scanning the atmosphere for {city}...")
        
        # Safety net: If you haven't put the key in your .env yet, use the public backup
        if not self.weather_api_key:
            try:
                url = f"https://wttr.in/{city}?format=3"
                response = requests.get(url)
                if response.status_code == 200:
                    return f"Using backup radar: {response.text.strip()}"
            except Exception:
                pass
            return "Weather services are currently offline."
            
        try:
            # Main engine: OpenWeather API
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                temp = round(data['main']['temp'])
                feels_like = round(data['main']['feels_like'])
                description = data['weather'][0]['description']
                return f"The current temperature in {city} is {temp} degrees, feeling like {feels_like} degrees, with {description}."
            else:
                return "Unable to reach the OpenWeather satellite network."
        except Exception:
            return "Atmospheric sensors encountered an unexpected error."

    def get_news_summary(self):
        """Pulls the top 3 live global headlines directly from Google News."""
        if self.senses:
            self.senses.speak("Scanning global news networks for top stories...")
        
        try:
            # We connect to the live Google News feed
            url = "https://news.google.com/rss"
            response = requests.get(url)
            
            if response.status_code == 200:
                # This breaks the feed down so Python can read the individual articles
                root = ET.fromstring(response.content)
                items = root.findall('./channel/item')
                
                news_summary = "Here are the top three global headlines right now: "
                
                # We grab just the first 3 headlines so he doesn't talk forever
                for i in range(min(3, len(items))):
                    title = items[i].find('title').text
                    news_summary += f"Number {i+1}: {title}. "
                    
                return news_summary
            else:
                return "I am currently unable to connect to the global news feeds."
                
        except Exception:
            return "My news retrieval sensors are experiencing interference."

    def process_data_request(self, command):
        """The master switch that sorts your real-world data and time requests."""
        command_lower = command.lower()
        
        # Check if you asked for the time or date
        if "time" in command_lower or "date" in command_lower or "day" in command_lower:
            result = self.get_time_and_date()
            if self.senses: self.senses.speak(result)
            
        # Check if you asked for money markets
        elif "price" in command_lower or "stock" in command_lower:
            result = self.get_price("BTC-USD")
            if self.senses: self.senses.speak(result)
            
        # Check if you asked for the weather or temperature
        elif "weather" in command_lower or "temperature" in command_lower or "forecast" in command_lower:
            # We remove question marks so the weather satellite doesn't get confused
            clean_command = command_lower.replace("?", "").replace(".", "")
            words = clean_command.split()
            
            # Grabs the last word you said to find the city
            city = words[-1] if len(words) > 1 else "your location"
            
            if city in ["weather", "temperature", "forecast"]:
                city = "New York"
                
            result = self.get_weather(city)
            if self.senses: self.senses.speak(result)
            
        # Check if you asked for the news
        elif "news" in command_lower:
            result = self.get_news_summary()
            if self.senses: self.senses.speak(result)

# --- Testing the Unified Module ---
if __name__ == "__main__":
    class DummySenses:
        def speak(self, text):
            print(f"\n[V.E.C.T.O.R.]: {text}")

    my_senses = DummySenses()
    fetchers = VectorFetchers(my_senses)
    
    print("--- Test: Live Global News ---")
    fetchers.process_data_request("Read me the news")