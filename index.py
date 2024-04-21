import functions_framework
import vertexai
from vertexai.preview.language_models import TextGenerationModel
from vertexai.generative_models import GenerativeModel, Part, FinishReason
import vertexai.preview.generative_models as generative_models
import json

# Replace with your project ID
PROJECT_ID = "instant-contact-420906"


# Define a function to generate text using Vertex AI
def generate_text(place,text):

    parameters = {
        "temperature": 0.2,
        "max_output_tokens": 256,
        "top_p": 0.8,
        "top_k": 40,
    }

    vertexai.init(project="instant-contact-420906", location="us-central1")
    model = GenerativeModel("gemini-1.5-pro-preview-0409")

    generation_config = {
    "max_output_tokens": 15000,
    "temperature": 0.2,
    "top_p": 0.95,
    }

    safety_settings = {
        generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }

    # responses = model.generate_content(
    #   [text],
    #   generation_config=generation_config,
    #   safety_settings=safety_settings,
    #   stream=True,
    # )
    json1 = str({
        "name": "",
        "nearby_places": ["name"],
        "description": "",
        "location": "location text",  # Add comma after location
        "google_map_url": "",  # Add colon after google_map_url
        "rating": "",
        "point_of_interest": ["name"],
        "distance": {
            "by car": "",
            "by train": "",
            "by flight": "",
        },
    })

    example_json = str(
        
    {
        "name": "Fort Kochi",
        "nearby places": ["Mattancherry Palace","Santa Cruz Basilica"
        ],
        "description": "Fort Kochi is a charming historical area known for its blend of Dutch, Portuguese, and British influences. It offers a unique cultural experience with colorful houses, art galleries, cafes, and vibrant streets.",
        "location": "Fort Kochi, Kochi, Kerala, India",
        "google map url": "https://goo.gl/maps/Y7vL5Y8mF2D2",
        "rating": 4.5,
        "point_of_interest": [
            {
                "name": "Chinese Fishing Nets"
            },
            {
                "name": "Art Galleries and Studios"
            },
        ],
        "distance": {
            "by car": "Depending on your location in Kochi, it can take 15-30 minutes by car.",
            "by train": "Ernakulam Junction is the nearest major railway station, and from there, you can take a taxi or bus to Fort Kochi.",
            "by flight": "Ferry services are available from Ernakulam mainland to Fort Kochi, offering scenic views of the harbor.",
        },
    }

    ) 
    query =f"take this as a use case : you are a travel guide and you give such responses for a customer's query Customer: I am in Kochi. I like to experience the lifestyle and food over here. I am sort of depressed. I feel lonely. I am a great lover of architecture and color. I love music. Give the output of content in JSON format so as to include:{json1}for example:{example_json},I'm currently in {place}:based on all this answer my query:{text} "

    
    response = model.generate_content([query], generation_config=parameters)
    print(f"Response from Model: {response.text}")
    return response.text


# Define a Flask app and route for text generation
from flask import Flask, request

app = Flask(__name__)


@app.route("/generateplaces", methods=["POST"])
def generate():
    data = request.get_json()
    place = data.get("place")
    text = data.get("text")
    print(place,text)
    response = generate_text(place,text)
    return {"response": response}

# @app.route("/generatedetail", methods=["POST"])
# def generate():
#     data = request.get_json()
#     place = data.get("place")
#     planner = data.get("planner")
#     text = data.get("text")
#     response = generate_text(place, planner, text)
#     return {"response": response}

# @app.route("/generateplanner", methods=["POST"])
# def generate():
#     data = request.get_json()
#     place = data.get("place")
#     planner = data.get("planner")
#     text = data.get("text")
#     response = generate_text(place, planner, text)
#     return {"response": response}


if __name__ == "__main__":
    app.run(debug=True)


# def generate_text(place: str, planner: list, text: str):

#     parameters = {
#         "temperature": 0.2,
#         "max_output_tokens": 256,
#         "top_p": 0.8,
#         "top_k": 40,
#     }

#     vertexai.init(project="instant-contact-420906", location="us-central1")
#     model = GenerativeModel("gemini-1.5-pro-preview-0409")

#     generation_config = {
#     "max_output_tokens": 10192,
#     "temperature": 0.2,
#     "top_p": 0.95,
#     }

#     safety_settings = {
#         generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
#         generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
#         generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
#         generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
#     }

#     # responses = model.generate_content(
#     #   [text],
#     #   generation_config=generation_config,
#     #   safety_settings=safety_settings,
#     #   stream=True,
#     # )
#     if place:
#         json1 = {
#             "name": "",
#             "nearby_places": [
#                 {"name": "", "description": "", "location": "", "rating": ""},
#             ],
#             "description": "",
#             "location": "location text",  # Add comma after location
#             "google_map_url": "",  # Add colon after google_map_url
#             "rating": "",
#             "point_of_interest": [
#                 {"name": "", "description": ""},
#             ],
#             "distance": {
#                 "by car": "",
#                 "by train": "",
#                 "by flight": "",
#             },
#         }

#         example_json = {
#             "name": "Fort Kochi",
#             "nearby places": [
#                 {
#                     "name": "Mattancherry Palace",
#                     "description": "Historical palace showcasing Kerala architecture with murals and artifacts.",
#                     "location": "Mattancherry, Kochi",
#                     "rating": 4.3,
#                 },
#                 {
#                     "name": "Santa Cruz Basilica",
#                     "description": "One of the oldest churches in India, known for its Gothic architecture and stained glass windows.",
#                     "location": "Fort Kochi",
#                     "rating": 4.6,
#                 },
#             ],
#             "description": "Fort Kochi is a charming historical area known for its blend of Dutch, Portuguese, and British influences. It offers a unique cultural experience with colorful houses, art galleries, cafes, and vibrant streets.",
#             "location": "Fort Kochi, Kochi, Kerala, India",
#             "google map url": "https://goo.gl/maps/Y7vL5Y8mF2D2",
#             "rating": 4.5,
#             "point_of_interest": [
#                 {
#                     "name": "Chinese Fishing Nets",
#                     "description": "Iconic landmarks along the coast, offering stunning sunset views and a glimpse into traditional fishing methods.",
#                 },
#                 {
#                     "name": "Art Galleries and Studios",
#                     "description": "Explore the local art scene with numerous galleries showcasing contemporary and traditional works.",
#                 },
#             ],
#             "distance": {
#                 "by car": "Depending on your location in Kochi, it can take 15-30 minutes by car.",
#                 "by train": "Ernakulam Junction is the nearest major railway station, and from there, you can take a taxi or bus to Fort Kochi.",
#                 "by flight": "Ferry services are available from Ernakulam mainland to Fort Kochi, offering scenic views of the harbor.",
#             },
#         }
#         query ="take this as a use case : you are a travel guide and you give such responses for a customer's query Customer: I am in Kochi. I like to experience the lifestyle and food over here. I am sort of depressed. I feel lonely. I am a great lover of architecture and color. I love music. Give the output of content in JSON format so as to include:{json1}for example:{example_json},I'm currently in {place} "

#     if planner:
#             example = {
#                     "Morning": [
#                         {
#                             "time": "9:00 AM - 9:30 AM",
#                             "description": "Start with a leisurely breakfast at a cafe in Fort Kochi. Enjoy a cup of South Indian filter coffee and local breakfast items like Idli, Dosa, or Appam with coconut chutney and sambar.",
#                         },
#                         {
#                             "time": "9:30 AM - 10:00 AM",
#                             "description": "Explore the Santa Cruz Basilica.",
#                         },
#                     ],
#                     "Afternoon": [
#                         {
#                             "time": "1:30 PM - 2:30 PM",
#                             "description": "Enjoy a Keralan lunch at a reputable restaurant or local eatery in Fort Kochi. Sample various seafood specialties like Karimeen fry (pearlspot fish) or Meen Curry (fish curry) with steamed rice and local vegetables.",
#                         },
#                     ],
#                     "optional_activities": "- Take a boat ride in the harbor or visit nearby islands like Bolgatty or Willingdon (duration depends on chosen activity). \n- Catch a Kathakali dance performance showcasing the traditional dance form of Kerala (typically 1-2 hours). \n- Visit the Kerala Folklore Museum to learn about the state's rich heritage (plan for 1-2 hours).",
#                 }

#             json2 ={
#                     "timeofday": {
#                         "time": [
#                             {"start_time": "", "end_time": "", "description": ""},
#                             #  ... more activities within the same timeofday
#                         ]
#                     },
#                     "optional_activities": "",
#                 }

#             query ="take this as a use case : you are a travel guide and you give such responses for a customer's query Customer:plan a beautiful day where these are the places I need to go:{planner} and in the schedule also include food timings. Give the output of content in JSON format so as to include:{json2},for example:{example}"


#     response = model.generate_content([query], generation_config=parameters)
#     print(f"Response from Model: {response.text}")
#     return response.text

