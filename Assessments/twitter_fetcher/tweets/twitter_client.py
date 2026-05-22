import datetime
import random
import time

class TwitterClient:
    """
    Developer Mock Client for Twitter (X) API v2.
    Strictly operates in mock mode to simulate X API behaviors, network delay,
    and various response status codes (200 OK, 404 User Not Found, 429 Rate Limit).
    """

    def __init__(self, latency=0.6, simulate_status="200"):
        self.latency = latency
        self.simulate_status = simulate_status

    def fetch_user_and_tweets(self, username):
        """
        Simulates fetching user details and latest 5 tweets from the X API v2.
        Applies configured network latency and simulates error states.
        """
        # Clean username
        username = username.strip().replace("@", "")
        if not username:
            raise ValueError("Username cannot be empty")

        # 1. Simulate network delay
        if self.latency > 0:
            time.sleep(self.latency)

        # 2. Simulate API status codes
        if self.simulate_status == "404":
            raise ValueError(f"User @{username} not found on X/Twitter (Simulated 404)")
        elif self.simulate_status == "429":
            raise RuntimeError("Twitter API rate limit exceeded (Simulated 429). Please try again in 15 minutes.")
        elif self.simulate_status == "500":
            raise RuntimeError("Internal Server Error from Twitter API v2 (Simulated 500)")

        # 3. Generate high-fidelity mock data (Success 200)
        return self.get_mock_data(username)

    def get_mock_data(self, username):
        """
        Generates rich mock profile and tweet data.
        """
        lower_username = username.lower()
        now = datetime.datetime.now(datetime.timezone.utc)

        # Customize profiles for key usernames
        if "elonmusk" in lower_username:
            mock_profile = {
                "username": "elonmusk",
                "name": "Elon Musk",
                "profile_image_url": "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=150&h=150&fit=crop",
                "description": "Maximalist. Making life multiplanetary. Accelerating sustainable energy. X Corp.",
                "verified": True,
                "followers_count": 182400000,
                "following_count": 524,
                "tweet_count": 42105,
            }
        elif "nasa" in lower_username:
            mock_profile = {
                "username": "NASA",
                "name": "NASA",
                "profile_image_url": "https://images.unsplash.com/photo-1614728894747-a83421e2b9c9?w=150&h=150&fit=crop",
                "description": "There is space for everybody. Exploring the secrets of the universe for the benefit of all. 🚀✨",
                "verified": True,
                "followers_count": 78900000,
                "following_count": 184,
                "tweet_count": 72412,
            }
        elif "google" in lower_username:
            mock_profile = {
                "username": "Google",
                "name": "Google",
                "profile_image_url": "https://images.unsplash.com/photo-1573804633927-bfcbcd909acd?w=150&h=150&fit=crop",
                "description": "Google's mission is to organize the world's information and make it universally accessible and useful.",
                "verified": True,
                "followers_count": 31400000,
                "following_count": 482,
                "tweet_count": 135400,
            }
        elif "openai" in lower_username:
            mock_profile = {
                "username": "OpenAI",
                "name": "OpenAI",
                "profile_image_url": "https://images.unsplash.com/photo-1677442136019-21780efad99a?w=150&h=150&fit=crop",
                "description": "OpenAI's mission is to ensure that artificial general intelligence benefits all of humanity.",
                "verified": True,
                "followers_count": 3200000,
                "following_count": 12,
                "tweet_count": 1850,
            }
        else:
            # General user profile fallback
            mock_profile = {
                "username": username,
                "name": username.capitalize(),
                "profile_image_url": f"https://api.dicebear.com/7.x/bottts/svg?seed={username}",
                "description": f"This is a mock bio for @{username}. Hello X / Twitter! Passionate about tech, design, and coding.",
                "verified": random.choice([True, False]),
                "followers_count": random.randint(100, 500000),
                "following_count": random.randint(50, 1500),
                "tweet_count": random.randint(10, 15000),
            }

        # Custom mock tweets based on user
        mock_tweets = []
        
        def get_iso_time(hours_ago):
            time_diff = now - datetime.timedelta(hours=hours_ago)
            return time_diff.isoformat()

        if "elonmusk" in lower_username:
            tweets_pool = [
                ("Starship Flight 5 launching soon. Goal is catch of the giant booster with the tower arms! Exciting times ahead 🚀", 1, 24000, 120000, 4800, 3100000),
                ("Tesla Full Self-Driving (Supervised) is improving exponentially. Soon it will be safer than humans in all conditions. @Tesla", 4, 18000, 95000, 5200, 2400000),
                ("Next generation Optimius robots are doing useful work in Tesla factories. Production starting next year.", 8, 14000, 88000, 3200, 1900000),
                ("Maybe we should put a trampolin on Mars. Lower gravity would be epic.", 15, 32000, 175000, 11000, 5400000),
                ("X is the ultimate platform for free speech and citizen journalism. Video posts are now receiving 10x more reach! 🔥", 26, 21000, 110000, 8900, 4200000)
            ]
        elif "nasa" in lower_username:
            tweets_pool = [
                ("Staring into the cosmic deep. 🌌 The James Webb Space Telescope has captured this stunning new view of a star-forming region in the Eagle Nebula. #JWST #Astronomy", 2, 8500, 42000, 680, 850000),
                ("Prepare for launch! 🚀 Our Artemis II crew is busy training for their historic mission around the Moon. Learn about the science payloads on board: nasa.gov/artemis", 6, 4200, 28000, 320, 510000),
                ("Mars, we are listening. 🛰️ The Perseverance rover has recorded the sounds of Martian wind and laser impacts. Listen to the red planet: nasa.gov/mars-sounds", 12, 6100, 34000, 490, 680000),
                ("Earth from space is a work of art. 🌍 Captured from the ISS, the auroras paint the atmosphere in glowing green and red hues. Simply breathtaking.", 20, 12000, 68000, 950, 1200000),
                ("A solar storm is approaching! ☀️ Beautiful auroras may be visible at lower latitudes tonight. Keep your eyes on the skies! #Auroras #SpaceWeather", 30, 9800, 52000, 1100, 940000)
            ]
        elif "google" in lower_username:
            tweets_pool = [
                ("Meet the next era of search. 🔍 We are introducing new AI-organized search results to help you find answers to complex questions faster. Try it out now!", 3, 1200, 8500, 340, 450000),
                ("Say hello to Gemini 1.5 Pro. Now with a 2-million token context window, enabling developers to build entirely new kinds of applications. #GoogleGemini", 7, 2400, 14000, 580, 720000),
                ("Android 15 is here! 📱 Designed with productivity, privacy, and user customization at the core. Update your Pixel devices today.", 14, 3100, 18500, 980, 980000),
                ("Google I/O 2026 kicks off! Watch the keynote live to see the latest updates in AI, workspace, cloud, and hardware: io.google", 24, 4800, 22000, 1200, 1500000),
                ("We are committed to running on 24/7 carbon-free energy by 2030. Here is how our wind and solar grids are powering our data centers.", 48, 1500, 9800, 210, 310000)
            ]
        elif "openai" in lower_username:
            tweets_pool = [
                ("We are introducing GPT-4o, our new flagship model that can reason across audio, vision, and text in real-time. Rolled out to all users today.", 1, 9500, 54000, 1400, 2100000),
                ("Sora is our model that can generate realistic and imaginative scenes from text instructions. We're excited to start sharing creative control. #OpenAISora", 5, 12000, 68000, 1800, 3200000),
                ("Our API now supports structured outputs! Developers can define a JSON Schema, and the model will strictly follow it with 100% reliability.", 10, 2100, 15000, 340, 650000),
                ("We are launching OpenAI Academy to invest in developer ecosystems and AI training around the globe, starting in emerging markets.", 22, 1800, 11200, 220, 480000),
                ("Introducing SearchGPT: a temporary prototype of new search features that give you fast and timely answers with clear and relevant sources.", 32, 7200, 39000, 920, 1700000)
            ]
        else:
            # General tech tweets
            tweets_pool = [
                ("Just pushed a major refactor to production. Everything is 3x faster, and 200 lines of spaghetti code are gone. Best feeling ever! 💻🚀 #buildinpublic #python", 2, 45, 340, 12, 4500),
                ("Vanilla CSS has gotten so good lately. Grid, Flexbox, custom properties, container queries, and nested selectors make frameworks feel almost redundant.", 5, 82, 510, 34, 7800),
                ("What is your favorite stack for building MVP web applications in 2026? I'm currently enjoying Django + Tailwind + HTMX. Fast, robust, and clean.", 11, 23, 140, 56, 3200),
                ("Spent 4 hours debugging a production issue only to realize it was a typo in an environment variable name. We've all been there, right? 😅", 19, 110, 890, 78, 12000),
                ("Learning in public is the ultimate cheat code for developers. It builds your network, documents your journey, and forces you to really understand the concepts.", 28, 67, 420, 22, 5900)
            ]

        for idx, (text, hours_ago, rts, likes, replies, views) in enumerate(tweets_pool[:5]):
            mock_tweets.append({
                "id": str(1000000000000000000 + idx + random.randint(1000, 9999)),
                "text": text,
                "created_at": get_iso_time(hours_ago),
                "likes": likes,
                "retweets": rts,
                "replies": replies,
                "views": views
            })

        return {
            "mode": "developer_mock",
            "reason": "Developer Mock Mode explicitly enabled",
            "user": mock_profile,
            "tweets": mock_tweets
        }