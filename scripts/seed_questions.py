# scripts/seed_questions.py
# Script to populate the database with 50 sample questions

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal
from models import Category, Question

# Sample questions data
SAMPLE_QUESTIONS = [
    # Science (15 questions)
    {
        "question": "What is the chemical symbol for water?",
        "correctAnswer": "H2O",
        "incorrectAnswers": ["CO2", "NaCl", "HCl"],
        "category": "Science",
        "difficulty": "easy",
        "tags": ["chemistry", "basic"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What planet is known as the Red Planet?",
        "correctAnswer": "Mars",
        "incorrectAnswers": ["Venus", "Jupiter", "Saturn"],
        "category": "Science",
        "difficulty": "easy",
        "tags": ["astronomy", "planets"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What is the speed of light approximately?",
        "correctAnswer": "3 x 10^8 m/s",
        "incorrectAnswers": ["3 x 10^6 m/s", "3 x 10^10 m/s", "3 x 10^4 m/s"],
        "category": "Science",
        "difficulty": "medium",
        "tags": ["physics", "constants"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "Which element is needed for combustion?",
        "correctAnswer": "Oxygen",
        "incorrectAnswers": ["Nitrogen", "Hydrogen", "Carbon"],
        "category": "Science",
        "difficulty": "easy",
        "tags": ["chemistry", "combustion"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What is the largest organ in the human body?",
        "correctAnswer": "Skin",
        "incorrectAnswers": ["Liver", "Brain", "Heart"],
        "category": "Science",
        "difficulty": "easy",
        "tags": ["biology", "anatomy"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "How many chromosomes do humans have?",
        "correctAnswer": "46",
        "incorrectAnswers": ["44", "48", "50"],
        "category": "Science",
        "difficulty": "medium",
        "tags": ["biology", "genetics"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What is the main gas in Earth's atmosphere?",
        "correctAnswer": "Nitrogen",
        "incorrectAnswers": ["Oxygen", "Carbon Dioxide", "Argon"],
        "category": "Science",
        "difficulty": "easy",
        "tags": ["atmosphere", "earth"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What is the smallest unit of life?",
        "correctAnswer": "Cell",
        "incorrectAnswers": ["Atom", "Molecule", "Tissue"],
        "category": "Science",
        "difficulty": "easy",
        "tags": ["biology", "basic"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What force keeps planets in orbit?",
        "correctAnswer": "Gravity",
        "incorrectAnswers": ["Magnetism", "Electricity", "Friction"],
        "category": "Science",
        "difficulty": "medium",
        "tags": ["physics", "gravity"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What is the pH of pure water?",
        "correctAnswer": "7",
        "incorrectAnswers": ["5", "8", "6"],
        "category": "Science",
        "difficulty": "easy",
        "tags": ["chemistry", "pH"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "Which gas do plants absorb from the atmosphere?",
        "correctAnswer": "Carbon Dioxide",
        "incorrectAnswers": ["Oxygen", "Nitrogen", "Hydrogen"],
        "category": "Science",
        "difficulty": "easy",
        "tags": ["biology", "photosynthesis"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What is the most abundant element in the universe?",
        "correctAnswer": "Hydrogen",
        "incorrectAnswers": ["Helium", "Oxygen", "Carbon"],
        "category": "Science",
        "difficulty": "medium",
        "tags": ["astronomy", "elements"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What is the boiling point of water at sea level?",
        "correctAnswer": "100°C",
        "incorrectAnswers": ["50°C", "75°C", "125°C"],
        "category": "Science",
        "difficulty": "easy",
        "tags": ["chemistry", "basic"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What type of rock is formed from volcanic activity?",
        "correctAnswer": "Igneous",
        "incorrectAnswers": ["Sedimentary", "Metamorphic", "Limestone"],
        "category": "Science",
        "difficulty": "medium",
        "tags": ["geology", "rocks"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What is the SI unit of force?",
        "correctAnswer": "Newton",
        "incorrectAnswers": ["Joule", "Watt", "Pascal"],
        "category": "Science",
        "difficulty": "medium",
        "tags": ["physics", "units"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },

    # History (10 questions)
    {
        "question": "Who was the first US president?",
        "correctAnswer": "George Washington",
        "incorrectAnswers": ["Thomas Jefferson", "Abraham Lincoln", "John Adams"],
        "category": "History",
        "difficulty": "easy",
        "tags": ["US", "presidents"],
        "type": "multiple_choice",
        "regions": ["US"],
        "isNiche": False
    },
    {
        "question": "When did World War II end?",
        "correctAnswer": "1945",
        "incorrectAnswers": ["1944", "1946", "1947"],
        "category": "History",
        "difficulty": "easy",
        "tags": ["ww2", "dates"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "Who built the Great Wall of China?",
        "correctAnswer": "Chinese dynasties",
        "incorrectAnswers": ["Mongols", "Japanese", "Koreans"],
        "category": "History",
        "difficulty": "medium",
        "tags": ["China", "architecture"],
        "type": "multiple_choice",
        "regions": ["Asia"],
        "isNiche": False
    },
    {
        "question": "What civilization built Machu Picchu?",
        "correctAnswer": "Inca",
        "incorrectAnswers": ["Aztec", "Maya", "Olmec"],
        "category": "History",
        "difficulty": "medium",
        "tags": ["americas", "civilizations"],
        "type": "multiple_choice",
        "regions": ["Americas"],
        "isNiche": False
    },
    {
        "question": "Who was the first emperor of Rome?",
        "correctAnswer": "Augustus",
        "incorrectAnswers": ["Julius Caesar", "Nero", "Marcus Aurelius"],
        "category": "History",
        "difficulty": "medium",
        "tags": ["rome", "emperors"],
        "type": "multiple_choice",
        "regions": ["Europe"],
        "isNiche": False
    },
    {
        "question": "What country gifted the Statue of Liberty to the US?",
        "correctAnswer": "France",
        "incorrectAnswers": ["England", "Spain", "Germany"],
        "category": "History",
        "difficulty": "easy",
        "tags": ["US", "monuments"],
        "type": "multiple_choice",
        "regions": ["US", "Europe"],
        "isNiche": False
    },
    {
        "question": "Who discovered penicillin?",
        "correctAnswer": "Alexander Fleming",
        "incorrectAnswers": ["Marie Curie", "Louis Pasteur", "Isaac Newton"],
        "category": "History",
        "difficulty": "medium",
        "tags": ["science", "medicine"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "When was the Declaration of Independence signed?",
        "correctAnswer": "1776",
        "incorrectAnswers": ["1775", "1777", "1778"],
        "category": "History",
        "difficulty": "easy",
        "tags": ["US", "independence"],
        "type": "multiple_choice",
        "regions": ["US"],
        "isNiche": False
    },
    {
        "question": "What was the longest war in history?",
        "correctAnswer": "The Hundred Years' War",
        "incorrectAnswers": ["World War II", "Vietnam War", "Cold War"],
        "category": "History",
        "difficulty": "hard",
        "tags": ["wars", "europe"],
        "type": "multiple_choice",
        "regions": ["Europe"],
        "isNiche": True
    },
    {
        "question": "Who was the last Pharaoh of Egypt?",
        "correctAnswer": "Cleopatra VII",
        "incorrectAnswers": ["Nefertiti", "Hatshepsut", "Ramesses II"],
        "category": "History",
        "difficulty": "hard",
        "tags": ["egypt", "pharaohs"],
        "type": "multiple_choice",
        "regions": ["Africa"],
        "isNiche": True
    },

    # Geography (10 questions)
    {
        "question": "What is the largest continent?",
        "correctAnswer": "Asia",
        "incorrectAnswers": ["Africa", "North America", "Europe"],
        "category": "Geography",
        "difficulty": "easy",
        "tags": ["continents", "basic"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What is the longest river in the world?",
        "correctAnswer": "Nile",
        "incorrectAnswers": ["Amazon", "Mississippi", "Yangtze"],
        "category": "Geography",
        "difficulty": "medium",
        "tags": ["rivers", "natural"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What is the capital of Australia?",
        "correctAnswer": "Canberra",
        "incorrectAnswers": ["Sydney", "Melbourne", "Perth"],
        "category": "Geography",
        "difficulty": "medium",
        "tags": ["capitals", "australia"],
        "type": "multiple_choice",
        "regions": ["Oceania"],
        "isNiche": False
    },
    {
        "question": "Which country has the most islands?",
        "correctAnswer": "Sweden",
        "incorrectAnswers": ["Norway", "Japan", "Indonesia"],
        "category": "Geography",
        "difficulty": "hard",
        "tags": ["islands", "europe"],
        "type": "multiple_choice",
        "regions": ["Europe"],
        "isNiche": True
    },
    {
        "question": "What is the smallest country in the world?",
        "correctAnswer": "Vatican City",
        "incorrectAnswers": ["Monaco", "San Marino", "Liechtenstein"],
        "category": "Geography",
        "difficulty": "easy",
        "tags": ["countries", "basic"],
        "type": "multiple_choice",
        "regions": ["Europe"],
        "isNiche": False
    },
    {
        "question": "What desert is the largest in the world?",
        "correctAnswer": "Sahara",
        "incorrectAnswers": ["Gobi", "Kalahari", "Atacama"],
        "category": "Geography",
        "difficulty": "easy",
        "tags": ["deserts", "natural"],
        "type": "multiple_choice",
        "regions": ["Africa"],
        "isNiche": False
    },
    {
        "question": "What is the deepest ocean?",
        "correctAnswer": "Pacific",
        "incorrectAnswers": ["Atlantic", "Indian", "Arctic"],
        "category": "Geography",
        "difficulty": "medium",
        "tags": ["oceans", "natural"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What is the longest mountain range in the world?",
        "correctAnswer": "Andes",
        "incorrectAnswers": ["Himalayas", "Rockies", "Ural"],
        "category": "Geography",
        "difficulty": "medium",
        "tags": ["mountains", "natural"],
        "type": "multiple_choice",
        "regions": ["Americas"],
        "isNiche": False
    },
    {
        "question": "Which country has the most natural lakes?",
        "correctAnswer": "Canada",
        "incorrectAnswers": ["Russia", "USA", "Brazil"],
        "category": "Geography",
        "difficulty": "hard",
        "tags": ["lakes", "north-america"],
        "type": "multiple_choice",
        "regions": ["Americas"],
        "isNiche": True
    },
    {
        "question": "What is the capital of Japan?",
        "correctAnswer": "Tokyo",
        "incorrectAnswers": ["Osaka", "Kyoto", "Nagoya"],
        "category": "Geography",
        "difficulty": "easy",
        "tags": ["capitals", "asia"],
        "type": "multiple_choice",
        "regions": ["Asia"],
        "isNiche": False
    },

    # Sports (10 questions)
    {
        "question": "What sport is played on a diamond?",
        "correctAnswer": "Baseball",
        "incorrectAnswers": ["Cricket", "Softball", "Tennis"],
        "category": "Sports",
        "difficulty": "easy",
        "tags": ["baseball", "field"],
        "type": "multiple_choice",
        "regions": ["US"],
        "isNiche": False
    },
    {
        "question": "How many players are on a soccer team?",
        "correctAnswer": "11",
        "incorrectAnswers": ["9", "10", "12"],
        "category": "Sports",
        "difficulty": "easy",
        "tags": ["soccer", "teams"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What country invented basketball?",
        "correctAnswer": "Canada",
        "incorrectAnswers": ["USA", "England", "Japan"],
        "category": "Sports",
        "difficulty": "medium",
        "tags": ["basketball", "history"],
        "type": "multiple_choice",
        "regions": ["Americas"],
        "isNiche": False
    },
    {
        "question": "What is the most popular sport in the world?",
        "correctAnswer": "Football (Soccer)",
        "incorrectAnswers": ["Cricket", "Basketball", "Tennis"],
        "category": "Sports",
        "difficulty": "easy",
        "tags": ["soccer", "popular"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What color is a tennis ball?",
        "correctAnswer": "Yellow",
        "incorrectAnswers": ["White", "Green", "Orange"],
        "category": "Sports",
        "difficulty": "easy",
        "tags": ["tennis", "basic"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What is the diameter of a basketball hoop?",
        "correctAnswer": "18 inches",
        "incorrectAnswers": ["15 inches", "20 inches", "22 inches"],
        "category": "Sports",
        "difficulty": "hard",
        "tags": ["basketball", "equipment"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": True
    },
    {
        "question": "Which country has won the most Cricket World Cups?",
        "correctAnswer": "Australia",
        "incorrectAnswers": ["India", "West Indies", "England"],
        "category": "Sports",
        "difficulty": "medium",
        "tags": ["cricket", "world-cup"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What is the highest score in a single bowling game?",
        "correctAnswer": "300",
        "incorrectAnswers": ["200", "250", "350"],
        "category": "Sports",
        "difficulty": "medium",
        "tags": ["bowling", "scores"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What sport uses a puck?",
        "correctAnswer": "Ice Hockey",
        "incorrectAnswers": ["Field Hockey", "Lacrosse", "Curling"],
        "category": "Sports",
        "difficulty": "easy",
        "tags": ["hockey", "equipment"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What country is famous for sumo wrestling?",
        "correctAnswer": "Japan",
        "incorrectAnswers": ["China", "Korea", "Mongolia"],
        "category": "Sports",
        "difficulty": "easy",
        "tags": ["sumo", "japan"],
        "type": "multiple_choice",
        "regions": ["Asia"],
        "isNiche": False
    },

    # Literature (5 questions)
    {
        "question": "Who wrote 'Romeo and Juliet'?",
        "correctAnswer": "William Shakespeare",
        "incorrectAnswers": ["Charles Dickens", "Jane Austen", "Mark Twain"],
        "category": "Literature",
        "difficulty": "easy",
        "tags": ["shakespeare", "classics"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What is the name of the wizard in 'The Lord of the Rings'?",
        "correctAnswer": "Gandalf",
        "incorrectAnswers": ["Merlin", "Dumbledore", "Saruman"],
        "category": "Literature",
        "difficulty": "easy",
        "tags": ["fantasy", "tolkein"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What book begins with 'Call me Ishmael'?",
        "correctAnswer": "Moby Dick",
        "incorrectAnswers": ["The Old Man and the Sea", "Treasure Island", "20,000 Leagues"],
        "category": "Literature",
        "difficulty": "medium",
        "tags": ["classics", "opening-lines"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "What is the first book in the Harry Potter series?",
        "correctAnswer": "The Philosopher's Stone",
        "incorrectAnswers": ["The Chamber of Secrets", "The Prisoner of Azkaban", "The Goblet of Fire"],
        "category": "Literature",
        "difficulty": "easy",
        "tags": ["harry-potter", "series"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    },
    {
        "question": "Who wrote 'Pride and Prejudice'?",
        "correctAnswer": "Jane Austen",
        "incorrectAnswers": ["Charlotte Bronte", "Emily Bronte", "Charles Dickens"],
        "category": "Literature",
        "difficulty": "medium",
        "tags": ["classics", "women-authors"],
        "type": "multiple_choice",
        "regions": ["global"],
        "isNiche": False
    }
]



MEDIA_QUESTIONS = [
    {
        "question": "Which word did you hear?",
        "correctAnswer": "Apple",
        "incorrectAnswers": ["Orange", "Banana", "Grape"],
        "category": "English",
        "difficulty": "easy",
        "tags": ["listening", "vocabulary"],
        "type": "audio",
        "mediaUrl": "/media/audio/apple.wav",
        "regions": ["global"],
        "isNiche": False,
    },
    {
        "question": "Which word did you hear?",
        "correctAnswer": "Orange",
        "incorrectAnswers": ["Apple", "Banana", "Grape"],
        "category": "English",
        "difficulty": "easy",
        "tags": ["listening", "vocabulary"],
        "type": "audio",
        "mediaUrl": "/media/audio/orange.wav",
        "regions": ["global"],
        "isNiche": False,
    },
    {
        "question": "Which word did you hear?",
        "correctAnswer": "Banana",
        "incorrectAnswers": ["Apple", "Orange", "Grape"],
        "category": "English",
        "difficulty": "easy",
        "tags": ["listening", "vocabulary"],
        "type": "audio",
        "mediaUrl": "/media/audio/banana.wav",
        "regions": ["global"],
        "isNiche": False,
    },
    {
        "question": "Which animal is shown?",
        "correctAnswer": "Cat",
        "incorrectAnswers": ["Dog", "Lion", "Tiger"],
        "category": "Science",
        "difficulty": "easy",
        "tags": ["animals", "image"],
        "type": "image",
        "mediaUrl": "/media/images/cat.png",
        "regions": ["global"],
        "isNiche": False,
    },
    {
        "question": "Which animal is shown?",
        "correctAnswer": "Dog",
        "incorrectAnswers": ["Cat", "Lion", "Tiger"],
        "category": "Science",
        "difficulty": "easy",
        "tags": ["animals", "image"],
        "type": "image",
        "mediaUrl": "/media/images/dog.png",
        "regions": ["global"],
        "isNiche": False,
    },
    {
        "question": "Which animal is shown?",
        "correctAnswer": "Lion",
        "incorrectAnswers": ["Cat", "Dog", "Tiger"],
        "category": "Science",
        "difficulty": "medium",
        "tags": ["animals", "image"],
        "type": "image",
        "mediaUrl": "/media/images/lion.png",
        "regions": ["global"],
        "isNiche": False,
    },
]


def _get_or_create_category(db, categories, category_name):
    if category_name not in categories:
        category = db.query(Category).filter(Category.name.ilike(category_name)).first()
        if not category:
            category = Category(name=category_name)
            db.add(category)
            db.flush()
        categories[category_name] = category
    return categories[category_name]


def _insert_question_if_missing(db, categories, q_data):
    existing = db.query(Question).filter(
        Question.question_text == q_data["question"],
        Question.type == q_data["type"],
    ).first()
    if existing:
        if q_data.get("mediaUrl") and existing.media_url != q_data["mediaUrl"]:
            existing.media_url = q_data["mediaUrl"]
        return False

    category = _get_or_create_category(db, categories, q_data["category"])
    db.add(Question(
        question_text=q_data["question"],
        correct_answer=q_data["correctAnswer"],
        incorrect_answers=q_data["incorrectAnswers"],
        category_id=category.id,
        difficulty=q_data["difficulty"],
        tags=q_data["tags"],
        type=q_data["type"],
        regions=q_data["regions"],
        is_niche=q_data["isNiche"],
        media_url=q_data.get("mediaUrl"),
    ))
    return True


def seed_database():
    from database import migrate_schema
    migrate_schema()

    db = SessionLocal()
    try:
        print("Starting database seeding...")
        categories = {}
        added_count = 0

        for q_data in SAMPLE_QUESTIONS:
            if _insert_question_if_missing(db, categories, q_data):
                added_count += 1

        for q_data in MEDIA_QUESTIONS:
            if _insert_question_if_missing(db, categories, q_data):
                added_count += 1

        db.commit()
        print(f"Successfully added {added_count} new questions to the database!")
        print("Categories available:", ", ".join(sorted(categories.keys())))

    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting QuizApp database seeding script...")
    seed_database()
    print("Done!")
