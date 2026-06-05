"""
Generate country profile README.md files from a single source of truth.

Run from repo root:
  python scripts/generate_country_profiles.py

Author: Adrian Dunkley
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "countries"


COUNTRIES = [
    {
        "slug": "jamaica",
        "name": "Jamaica",
        "capital": "Kingston",
        "currency": "Jamaican Dollar (JMD)",
        "languages": "English (official), Jamaican Patois",
        "population": "about 2.8 million",
        "area_km2": "10,991",
        "independence": "6 August 1962",
        "national_dish": "Ackee and saltfish",
        "music": "Reggae, dancehall, ska, mento",
        "dialect_phrases": [
            "Wah gwaan? -> How are you?",
            "Mi deh yah -> I'm here",
            "Likkle more -> See you later",
            "Wah yuh a seh? -> What are you saying?",
            "Mi soon come -> I'll be there shortly",
        ],
        "facts": [
            "Home of Blue Mountain Coffee, one of the world's most expensive coffees.",
            "Usain Bolt, the fastest man in history, is Jamaican.",
            "Maroons in Accompong and Moore Town fought the British to a treaty in 1739.",
            "Jamaica was the first country in the western world to build a railway, in 1845.",
        ],
        "ai_use_case": (
            "Predictive maintenance for the Jamaica Public Service grid. Outage prediction from weather, "
            "load, and feeder age can cut downtime in storm season. Pair with a customer SMS bot for ETAs."
        ),
        "dataset": "datasets/saint_lucia_rainfall.csv (rainfall patterns adaptable), local STATIN bulletins.",
    },
    {
        "slug": "trinidad-and-tobago",
        "name": "Trinidad and Tobago",
        "capital": "Port of Spain",
        "currency": "Trinidad and Tobago Dollar (TTD)",
        "languages": "English (official), Trinidadian Creole, Tobagonian Creole",
        "population": "about 1.4 million",
        "area_km2": "5,131",
        "independence": "31 August 1962",
        "national_dish": "Crab and callaloo (Trinidad), curry crab and dumpling (Tobago)",
        "music": "Calypso, soca, chutney, parang",
        "dialect_phrases": [
            "Allyuh -> All of you",
            "Lime -> hang out",
            "Doh dotish -> don't be silly",
            "Yuh playin mas? -> Are you joining the carnival?",
            "Steups -> a kiss teeth sound",
        ],
        "facts": [
            "Birthplace of the steel pan, the only acoustic instrument invented in the 20th century.",
            "Has the largest oil and gas industry in CARICOM.",
            "The Caroni Swamp hosts thousands of Scarlet Ibis at sunset.",
            "Carnival is the biggest in the Caribbean.",
        ],
        "ai_use_case": (
            "Demand forecasting for Carnival logistics: parking, ambulance positioning, food vendor supply, "
            "and ride share surge. Multi week lead time helps small vendors profit."
        ),
        "dataset": "datasets/tourism_reviews.csv, datasets/atlantic_storms.csv.",
    },
    {
        "slug": "barbados",
        "name": "Barbados",
        "capital": "Bridgetown",
        "currency": "Barbadian Dollar (BBD), pegged at 2 BBD per USD",
        "languages": "English (official), Bajan dialect",
        "population": "about 281,000",
        "area_km2": "430",
        "independence": "30 November 1966 (Republic since 30 November 2021)",
        "national_dish": "Cou cou and flying fish",
        "music": "Spouge, calypso, soca, bashment soca",
        "dialect_phrases": [
            "Wuh part yuh deh? -> Where are you?",
            "Lewwe go -> Let's go",
            "Wuh you mean? -> What do you mean?",
            "Cheese on bread -> mild exclamation",
            "Bare -> a lot of",
        ],
        "facts": [
            "Rihanna is Bajan. Mia Mottley is the prime minister.",
            "Barbados became a republic in 2021, removing the British monarch as head of state.",
            "The historic Bridgetown and its Garrison is a UNESCO World Heritage Site.",
            "Mount Gay is the world's oldest still operating rum distillery, since 1703.",
        ],
        "ai_use_case": (
            "Sentiment and theme analysis of TripAdvisor and Google reviews across the south coast, west coast, "
            "and east coast, feeding the Barbados Tourism Marketing Inc. quarterly briefing cycle."
        ),
        "dataset": "datasets/barbados_arrivals.csv, datasets/tourism_reviews.csv.",
    },
    {
        "slug": "bahamas",
        "name": "Bahamas",
        "capital": "Nassau",
        "currency": "Bahamian Dollar (BSD), pegged 1:1 with USD",
        "languages": "English (official), Bahamian Creole",
        "population": "about 410,000",
        "area_km2": "13,878",
        "independence": "10 July 1973",
        "national_dish": "Conch (variety of preparations), pigeon peas and rice",
        "music": "Junkanoo rake and scrape, calypso",
        "dialect_phrases": [
            "Wha goin on? -> What's happening?",
            "Sip sip -> gossip",
            "Cherl -> a friendly address",
            "Y'all -> you all",
            "Bey -> friend",
        ],
        "facts": [
            "An archipelago of about 700 islands and cays.",
            "The Junkanoo parade on Boxing Day and New Year's Day is a national festival.",
            "Atlantis Resort on Paradise Island is one of the largest in the world.",
            "The Bahamas was the first stop in the Americas for Columbus in 1492.",
        ],
        "ai_use_case": (
            "Hurricane damage rapid assessment using drone imagery for the National Emergency Management Agency. "
            "Post Dorian, faster damage classification meant faster relief routing."
        ),
        "dataset": "datasets/atlantic_storms.csv, NOAA HURDAT2.",
    },
    {
        "slug": "haiti",
        "name": "Haiti",
        "capital": "Port-au-Prince",
        "currency": "Haitian Gourde (HTG)",
        "languages": "Haitian Kreyol and French (both official)",
        "population": "about 11.5 million",
        "area_km2": "27,750",
        "independence": "1 January 1804",
        "national_dish": "Griot (fried pork) with diri ak djon djon",
        "music": "Kompa, rara, mizik rasin",
        "dialect_phrases": [
            "Sak pase? -> What's up?",
            "N ap boule -> We're cool",
            "Mèsi anpil -> Thank you very much",
            "Kouman ou ye? -> How are you?",
            "M renmen ou -> I love you",
        ],
        "facts": [
            "The first independent Black republic, established by formerly enslaved people in 1804.",
            "Haiti shares Hispaniola with the Dominican Republic.",
            "The Citadelle Laferrière in the north is the largest fortress in the Americas.",
            "Haiti has the largest diaspora population of any Caribbean nation.",
        ],
        "ai_use_case": (
            "Kreyol first chatbots for public services. Most existing tools assume French. A Kreyol native NLP "
            "pipeline can reach citizens who otherwise are left out."
        ),
        "dataset": "datasets/caribbean_dialect_phrases.csv (includes Kreyol entries).",
    },
    {
        "slug": "dominican-republic",
        "name": "Dominican Republic",
        "capital": "Santo Domingo",
        "currency": "Dominican Peso (DOP)",
        "languages": "Spanish (official)",
        "population": "about 11.3 million",
        "area_km2": "48,671",
        "independence": "27 February 1844",
        "national_dish": "La Bandera (rice, beans, meat, plantain)",
        "music": "Merengue, bachata, dembow",
        "dialect_phrases": [
            "¿Qué lo qué? -> What's up?",
            "Manín -> friend",
            "Tato -> all good",
            "Una vaina -> a thing",
            "Concón -> the crispy rice at the bottom of the pot",
        ],
        "facts": [
            "Santo Domingo is the oldest continuously inhabited European founded city in the Americas.",
            "The country has the largest economy in the Caribbean by GDP.",
            "Pico Duarte is the highest peak in the Caribbean at 3,098 metres.",
            "Merengue is its national music and a UNESCO intangible heritage.",
        ],
        "ai_use_case": (
            "Customer support automation for remittance providers serving the US Dominican diaspora, "
            "with Spanish first prompts that respect Dominican dialect."
        ),
        "dataset": "datasets/remittance_transactions.csv.",
    },
    {
        "slug": "cuba",
        "name": "Cuba",
        "capital": "Havana",
        "currency": "Cuban Peso (CUP)",
        "languages": "Spanish (official)",
        "population": "about 11 million",
        "area_km2": "109,884",
        "independence": "20 May 1902",
        "national_dish": "Ropa vieja, congrí, lechón",
        "music": "Son, mambo, rumba, salsa, timba",
        "dialect_phrases": [
            "Asere -> friend",
            "¿Qué bolá? -> What's up?",
            "Pinchar -> to work",
            "Coger botella -> to hitchhike",
            "Acere, qué volá -> hey buddy what's up",
        ],
        "facts": [
            "The largest island in the Caribbean.",
            "Old Havana is a UNESCO World Heritage Site.",
            "Cuba has one of the highest doctor to patient ratios in the world.",
            "Birthplace of salsa, son, and the mojito.",
        ],
        "ai_use_case": (
            "Offline first educational AI tutors that work without reliable internet, important in much of the "
            "country. Edge models on cheap Android phones can serve schools."
        ),
        "dataset": "Public Cuban statistical yearbooks, regional health data.",
    },
    {
        "slug": "puerto-rico",
        "name": "Puerto Rico",
        "capital": "San Juan",
        "currency": "United States Dollar (USD)",
        "languages": "Spanish and English (both official)",
        "population": "about 3.2 million",
        "area_km2": "9,104",
        "independence": "Unincorporated US territory",
        "national_dish": "Mofongo, arroz con gandules, lechón asado",
        "music": "Reggaeton, salsa, bomba, plena",
        "dialect_phrases": [
            "¿Qué pasa? -> What's up?",
            "Brutal -> excellent",
            "Wepa -> expression of joy",
            "Mano -> brother",
            "Janguear -> to hang out",
        ],
        "facts": [
            "Home of reggaeton, with Bad Bunny among its biggest global exports.",
            "El Yunque is the only tropical rainforest in the US National Forest System.",
            "Has been a US territory since 1898.",
            "Roberto Clemente was the first Latin American Hall of Fame baseball player.",
        ],
        "ai_use_case": (
            "Energy grid resilience modelling after Maria. Predicting feeder vulnerability before storms enables "
            "preventive crew positioning."
        ),
        "dataset": "NOAA storm archives, local PR energy data.",
    },
    {
        "slug": "guyana",
        "name": "Guyana",
        "capital": "Georgetown",
        "currency": "Guyanese Dollar (GYD)",
        "languages": "English (official), Guyanese Creole",
        "population": "about 800,000",
        "area_km2": "214,969",
        "independence": "26 May 1966",
        "national_dish": "Pepperpot, cook up rice",
        "music": "Chutney, calypso, soca",
        "dialect_phrases": [
            "Wuh side -> where",
            "Awee -> we",
            "Banna -> friend",
            "Lemme see -> let me see",
            "Yuh nah see -> don't you see",
        ],
        "facts": [
            "The only English speaking country in South America.",
            "Kaieteur Falls is one of the world's most powerful waterfalls.",
            "The discovery of offshore oil since 2015 is reshaping the economy.",
            "Has the world's largest single drop waterfall by volume.",
        ],
        "ai_use_case": (
            "Forest monitoring with satellite imagery and remote sensing to fight illegal logging and protect "
            "the Iwokrama rainforest."
        ),
        "dataset": "Public satellite data, NASA Earth observations.",
    },
    {
        "slug": "suriname",
        "name": "Suriname",
        "capital": "Paramaribo",
        "currency": "Surinamese Dollar (SRD)",
        "languages": "Dutch (official), Sranan Tongo, Sarnami Hindustani, Javanese",
        "population": "about 620,000",
        "area_km2": "163,820",
        "independence": "25 November 1975",
        "national_dish": "Pom",
        "music": "Kaseko, kawina, baithak gana",
        "dialect_phrases": [
            "Fa waka -> How are you (Sranan)",
            "Mi e go -> I'm going",
            "San de -> What's up",
            "A bun -> It's good",
            "Tangi -> Thanks",
        ],
        "facts": [
            "The smallest sovereign nation in South America.",
            "Paramaribo's historic city centre is a UNESCO World Heritage Site.",
            "Around 90 percent of the country is covered in rainforest.",
            "Highly multi ethnic, with Hindustani, Javanese, Creole, Maroon, Indigenous, and Chinese communities.",
        ],
        "ai_use_case": (
            "Multilingual public service chatbots that handle Dutch, Sranan Tongo, and Sarnami in a single flow."
        ),
        "dataset": "datasets/caribbean_dialect_phrases.csv.",
    },
    {
        "slug": "belize",
        "name": "Belize",
        "capital": "Belmopan",
        "currency": "Belize Dollar (BZD), pegged at 2 BZD per USD",
        "languages": "English (official), Belizean Kriol, Spanish, Garifuna, Maya",
        "population": "about 410,000",
        "area_km2": "22,966",
        "independence": "21 September 1981",
        "national_dish": "Rice and beans with stewed chicken",
        "music": "Punta, brukdown, calypso",
        "dialect_phrases": [
            "Weh di go aan -> What's going on (Kriol)",
            "Da how yu di du -> How are you doing",
            "Aarite -> alright",
            "Bredda -> brother",
            "Yu noh -> you know",
        ],
        "facts": [
            "Home of the Belize Barrier Reef, the second largest in the world.",
            "The only Central American country with English as its official language.",
            "Caracol and other ancient Maya sites lie within its borders.",
            "Garifuna culture is recognised by UNESCO as a Masterpiece of Intangible Heritage.",
        ],
        "ai_use_case": (
            "Reef health monitoring using citizen science photo submissions from tour operators and divers, "
            "scored with a CNN trained on bleaching imagery."
        ),
        "dataset": "datasets/sst_anomaly.csv.",
    },
    {
        "slug": "antigua-and-barbuda",
        "name": "Antigua and Barbuda",
        "capital": "Saint John's",
        "currency": "Eastern Caribbean Dollar (XCD)",
        "languages": "English (official), Antiguan Creole",
        "population": "about 100,000",
        "area_km2": "442",
        "independence": "1 November 1981",
        "national_dish": "Fungee and pepperpot",
        "music": "Calypso, soca, benna",
        "dialect_phrases": [
            "Wha gwan -> What's up",
            "Me gone -> I'm leaving",
            "Likkle more -> see you later",
            "Yuh ah no joke -> you are something else",
            "Cool runnings -> all is well",
        ],
        "facts": [
            "Famous for having a beach for every day of the year.",
            "Nelson's Dockyard is a UNESCO World Heritage Site.",
            "Barbuda is home to one of the largest Frigatebird colonies in the world.",
            "The country was severely hit by Irma in 2017, especially Barbuda.",
        ],
        "ai_use_case": (
            "Cruise tourism shoulder season demand forecasting, helping smaller operators plan staffing."
        ),
        "dataset": "datasets/barbados_arrivals.csv (regional pattern).",
    },
    {
        "slug": "dominica",
        "name": "Dominica",
        "capital": "Roseau",
        "currency": "Eastern Caribbean Dollar (XCD)",
        "languages": "English (official), Dominican Kwéyòl",
        "population": "about 73,000",
        "area_km2": "751",
        "independence": "3 November 1978",
        "national_dish": "Mountain chicken (crapaud), callaloo",
        "music": "Bouyon, cadence-lypso",
        "dialect_phrases": [
            "Sa ka fèt -> What's happening (Kwéyòl)",
            "Mwen byen -> I'm fine",
            "Mèsi -> Thank you",
            "Bondyé -> God",
            "Annou alé -> Let's go",
        ],
        "facts": [
            "Known as the Nature Isle of the Caribbean.",
            "Home of the only remaining pre-Columbian indigenous population, the Kalinago.",
            "Boiling Lake is the world's second largest hot lake.",
            "Devastated by Hurricane Maria in 2017, now rebuilding as the world's first climate resilient nation.",
        ],
        "ai_use_case": (
            "Climate resilience planning, using flood maps, soil moisture data, and population models to "
            "prioritise infrastructure investment."
        ),
        "dataset": "datasets/atlantic_storms.csv, satellite elevation data.",
    },
    {
        "slug": "grenada",
        "name": "Grenada",
        "capital": "Saint George's",
        "currency": "Eastern Caribbean Dollar (XCD)",
        "languages": "English (official), Grenadian Creole, Patois (declining)",
        "population": "about 113,000",
        "area_km2": "344",
        "independence": "7 February 1974",
        "national_dish": "Oil down",
        "music": "Soca, calypso, jab jab",
        "dialect_phrases": [
            "Wha goin on -> What's happening",
            "Liming -> hanging out",
            "Maco -> nosy person",
            "Bazodee -> dazed",
            "Sweet hand -> good cook",
        ],
        "facts": [
            "Known as the Spice Isle, Grenada produces nutmeg, mace, cinnamon, and cloves.",
            "Underwater Sculpture Park is the world's first of its kind.",
            "Hurricane Beryl in 2024 hit Carriacou hard, prompting a national reconstruction push.",
            "Grand Anse is consistently named among the world's best beaches.",
        ],
        "ai_use_case": (
            "Spice supply chain traceability using image recognition at processing plants combined with "
            "blockchain or simpler ledger systems."
        ),
        "dataset": "datasets/atlantic_storms.csv, agricultural export records.",
    },
    {
        "slug": "st-kitts-and-nevis",
        "name": "Saint Kitts and Nevis",
        "capital": "Basseterre",
        "currency": "Eastern Caribbean Dollar (XCD)",
        "languages": "English (official), Kittitian Creole",
        "population": "about 55,000",
        "area_km2": "261",
        "independence": "19 September 1983",
        "national_dish": "Stewed saltfish with spicy plantain, dumplings, breadfruit",
        "music": "Soca, calypso, Sugar Mas",
        "dialect_phrases": [
            "Wha appenin -> What's happening",
            "Mi deh yah -> I'm here",
            "Cudden -> can't",
            "Yuh swarm -> you joker",
            "Wuk -> work",
        ],
        "facts": [
            "The smallest sovereign state in the Western Hemisphere.",
            "Brimstone Hill Fortress is a UNESCO World Heritage Site.",
            "Sugar dominated for centuries until the industry closed in 2005.",
            "Citizenship by Investment programme is among the oldest in the world.",
        ],
        "ai_use_case": (
            "Citizenship application document processing using OCR plus structured extraction to reduce "
            "processing time."
        ),
        "dataset": "Local government public sector data.",
    },
    {
        "slug": "st-lucia",
        "name": "Saint Lucia",
        "capital": "Castries",
        "currency": "Eastern Caribbean Dollar (XCD)",
        "languages": "English (official), Saint Lucian Kwéyòl",
        "population": "about 180,000",
        "area_km2": "617",
        "independence": "22 February 1979",
        "national_dish": "Green fig and saltfish",
        "music": "Soca, zouk, dennery segment",
        "dialect_phrases": [
            "Sa ka fèt -> What's happening (Kwéyòl)",
            "Mwen la -> I'm here",
            "Bondyé bon -> God is good",
            "Annou alé -> Let's go",
            "Sé bon -> It's good",
        ],
        "facts": [
            "Home to the Pitons, a UNESCO World Heritage Site.",
            "Two Nobel laureates from one island: Sir Arthur Lewis and Derek Walcott.",
            "Has the only drive in volcano in the world at Soufrière.",
            "Jounen Kwéyòl (Creole Day) celebrates language and heritage every October.",
        ],
        "ai_use_case": (
            "Rainfall and flood prediction at parish level, integrated with the Met Office's public alert system."
        ),
        "dataset": "datasets/saint_lucia_rainfall.csv.",
    },
    {
        "slug": "st-vincent-and-the-grenadines",
        "name": "Saint Vincent and the Grenadines",
        "capital": "Kingstown",
        "currency": "Eastern Caribbean Dollar (XCD)",
        "languages": "English (official), Vincentian Creole",
        "population": "about 110,000",
        "area_km2": "389",
        "independence": "27 October 1979",
        "national_dish": "Roasted breadfruit and fried jackfish",
        "music": "Soca, calypso, bigdrum",
        "dialect_phrases": [
            "Wha goin on -> What's happening",
            "Yuh good -> Are you well",
            "Tek time -> Take it easy",
            "Vex -> angry",
            "Sweetie -> candy",
        ],
        "facts": [
            "La Soufrière erupted in 2021 displacing about 20 percent of the population.",
            "The Grenadines are 32 islands, many privately owned.",
            "Pirates of the Caribbean was filmed largely in the Grenadines.",
            "Bequia is one of the last places in the world to allow limited traditional whaling.",
        ],
        "ai_use_case": (
            "Ash fall and air quality forecasting for the population near La Soufrière, with SMS based alerts."
        ),
        "dataset": "Volcanic monitoring open data.",
    },
    {
        "slug": "aruba",
        "name": "Aruba",
        "capital": "Oranjestad",
        "currency": "Aruban Florin (AWG)",
        "languages": "Dutch and Papiamento (official), English, Spanish widely spoken",
        "population": "about 110,000",
        "area_km2": "180",
        "independence": "Constituent country of the Kingdom of the Netherlands",
        "national_dish": "Keshi yena",
        "music": "Tumba, soca, salsa",
        "dialect_phrases": [
            "Bon dia -> Good morning (Papiamento)",
            "Con ta bay -> How are you",
            "Mi ta bon -> I'm fine",
            "Danki -> Thank you",
            "Te awor -> See you later",
        ],
        "facts": [
            "Outside the hurricane belt, it rarely experiences major storms.",
            "Papiamento is a creole language with Portuguese, Spanish, Dutch, and African roots.",
            "Tourism makes up about three quarters of GDP.",
            "Famous for its windy southern coast, ideal for kite surfing.",
        ],
        "ai_use_case": (
            "Multilingual hotel concierge bots that switch fluidly between English, Dutch, Spanish, and Papiamento."
        ),
        "dataset": "datasets/tourism_reviews.csv.",
    },
    {
        "slug": "curacao",
        "name": "Curaçao",
        "capital": "Willemstad",
        "currency": "Netherlands Antillean Guilder (ANG)",
        "languages": "Dutch, Papiamento, English (all official)",
        "population": "about 155,000",
        "area_km2": "444",
        "independence": "Constituent country of the Kingdom of the Netherlands",
        "national_dish": "Keshi yena, stoba",
        "music": "Tumba, ritmo kombina",
        "dialect_phrases": [
            "Bon bini -> Welcome",
            "Kon ta bai -> How are you",
            "Hopi bon -> Very good",
            "Masha danki -> Thank you very much",
            "Pasa bon -> Have a good one",
        ],
        "facts": [
            "Willemstad is a UNESCO World Heritage Site for its pastel Dutch colonial architecture.",
            "Curaçao liqueur, the blue one, originates here.",
            "Home to one of the largest oil refineries in the region.",
            "Carnival here runs for weeks across the island.",
        ],
        "ai_use_case": (
            "Logistics optimisation for the Free Trade Zone, balancing inbound shipping with outbound to "
            "Latin American markets."
        ),
        "dataset": "Public maritime AIS data.",
    },
    {
        "slug": "cayman-islands",
        "name": "Cayman Islands",
        "capital": "George Town",
        "currency": "Cayman Islands Dollar (KYD)",
        "languages": "English (official)",
        "population": "about 70,000",
        "area_km2": "264",
        "independence": "British Overseas Territory",
        "national_dish": "Turtle stew, conch fritters",
        "music": "Soca, reggae, country",
        "dialect_phrases": [
            "Wha goin on -> What's going on",
            "Caymanian -> from the Cayman Islands",
            "Cudjoe -> a friendly term",
            "Bro -> brother",
            "Ya mon -> agreement",
        ],
        "facts": [
            "Home of Seven Mile Beach, often ranked among the best in the world.",
            "Largest registered insurance and hedge fund jurisdiction in the Caribbean.",
            "Stingray City lets visitors swim with stingrays in shallow water.",
            "Brac, Little Cayman, and Grand Cayman make up the three islands.",
        ],
        "ai_use_case": (
            "Anti money laundering pattern detection in fund administration, with strong privacy and "
            "regulator approved auditability."
        ),
        "dataset": "Public OFAC sanctions lists, internal AML logs.",
    },
    {
        "slug": "turks-and-caicos",
        "name": "Turks and Caicos Islands",
        "capital": "Cockburn Town",
        "currency": "United States Dollar (USD)",
        "languages": "English (official)",
        "population": "about 47,000",
        "area_km2": "948",
        "independence": "British Overseas Territory",
        "national_dish": "Conch dishes, peas and grits",
        "music": "Rake and scrape, ripsaw",
        "dialect_phrases": [
            "Wassup -> What's up",
            "Belonger -> a native of Turks and Caicos",
            "Yes my dear -> term of warmth",
            "Bey -> friend",
            "Aint it -> isn't it",
        ],
        "facts": [
            "Made up of about 40 islands and cays, only eight inhabited.",
            "Salt was the major export for centuries, hence Salt Cay's name.",
            "Has the third largest coral reef system in the world.",
            "Provo and Grace Bay drive much of its tourism economy.",
        ],
        "ai_use_case": (
            "Beach safety prediction from currents, wind, and tide data, fed into a daily dashboard for hotels."
        ),
        "dataset": "NOAA buoy data, local marine reports.",
    },
    {
        "slug": "british-virgin-islands",
        "name": "British Virgin Islands",
        "capital": "Road Town",
        "currency": "United States Dollar (USD)",
        "languages": "English (official)",
        "population": "about 31,000",
        "area_km2": "151",
        "independence": "British Overseas Territory",
        "national_dish": "Fungee and fish",
        "music": "Fungi, soca, calypso",
        "dialect_phrases": [
            "Wha goin on -> What's happening",
            "Belonger -> a native of the BVI",
            "Aw -> oh",
            "Bey -> friend",
            "Yeah man -> agreement",
        ],
        "facts": [
            "About 60 islands and cays, 16 inhabited.",
            "World class sailing destination, especially the Sir Francis Drake Channel.",
            "Major offshore financial centre with thousands of company registrations.",
            "Anegada is a coral island, while the rest are volcanic.",
        ],
        "ai_use_case": (
            "Marine traffic anomaly detection from AIS data to support customs and environmental monitoring."
        ),
        "dataset": "Public AIS feeds.",
    },
    {
        "slug": "us-virgin-islands",
        "name": "United States Virgin Islands",
        "capital": "Charlotte Amalie",
        "currency": "United States Dollar (USD)",
        "languages": "English (official), Spanish, Virgin Islands Creole",
        "population": "about 88,000",
        "area_km2": "346",
        "independence": "United States territory since 1917",
        "national_dish": "Fungi, kallaloo, conch",
        "music": "Quelbe, soca",
        "dialect_phrases": [
            "Wha goin on -> What's happening",
            "Bambye -> later on",
            "Limin -> hanging out",
            "Ja -> agreement",
            "Cuz -> cousin or friend",
        ],
        "facts": [
            "Three main islands: Saint Thomas, Saint Croix, and Saint John.",
            "Two thirds of Saint John is the Virgin Islands National Park.",
            "Purchased by the United States from Denmark in 1917.",
            "Hit hard by Hurricanes Irma and Maria in 2017.",
        ],
        "ai_use_case": (
            "Storm preparedness public alert system, integrated with FEMA flows and translated to Spanish "
            "and Virgin Islands Creole."
        ),
        "dataset": "datasets/atlantic_storms.csv.",
    },
    {
        "slug": "bermuda",
        "name": "Bermuda",
        "capital": "Hamilton",
        "currency": "Bermudian Dollar (BMD), pegged 1:1 with USD",
        "languages": "English (official), Portuguese widely spoken",
        "population": "about 64,000",
        "area_km2": "54",
        "independence": "British Overseas Territory",
        "national_dish": "Fish chowder, Sunday codfish breakfast",
        "music": "Gombey, calypso, jazz",
        "dialect_phrases": [
            "Onion -> Bermudian (used affectionately)",
            "Innit -> isn't it",
            "Goin tarn -> going downtown",
            "Da Rock -> Bermuda",
            "Bie -> man, friend",
        ],
        "facts": [
            "Not in the Caribbean Sea, but culturally and politically often grouped with the Caribbean.",
            "Major reinsurance hub.",
            "The Gombey dance combines African, Caribbean, and British military traditions.",
            "Famous for pink sand beaches due to crushed red foram skeletons.",
        ],
        "ai_use_case": (
            "Reinsurance catastrophe modelling, using hurricane intensity and damage models to inform pricing."
        ),
        "dataset": "datasets/atlantic_storms.csv.",
    },
]


def render(country):
    md = f"""# {country['name']}

Country profile for AI for Caribbeans.

## Quick facts

- **Capital:** {country['capital']}
- **Currency:** {country['currency']}
- **Languages:** {country['languages']}
- **Population:** {country['population']}
- **Area:** {country['area_km2']} km^2
- **Independence:** {country['independence']}
- **National dish:** {country['national_dish']}
- **Music:** {country['music']}

## Dialect and language

A small sample of common phrases:

"""
    for phrase in country["dialect_phrases"]:
        md += f"- {phrase}\n"

    md += "\n## Five facts you should know\n\n"
    for fact in country["facts"]:
        md += f"- {fact}\n"

    md += f"""
## AI use case tailored to {country['name']}

{country['ai_use_case']}

## Suggested datasets

{country['dataset']}

## Try this

Open one of the [applications](../../applications) and adapt it to {country['name']}.
A good starter: pick a tourism, climate, or finance project, swap the place names
and exchange rates, and run it on local data you can collect in a week.
"""
    return md


def main():
    index_lines = ["# Countries", "", "Profiles, facts, dialect notes, and tailored AI use cases.", ""]
    for c in sorted(COUNTRIES, key=lambda x: x["name"]):
        path = OUT / c["slug"] / "README.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render(c))
        index_lines.append(f"- [{c['name']}]({c['slug']}/README.md)")
    (OUT / "README.md").write_text("\n".join(index_lines) + "\n")
    print(f"Wrote {len(COUNTRIES)} country profiles.")


if __name__ == "__main__":
    main()
