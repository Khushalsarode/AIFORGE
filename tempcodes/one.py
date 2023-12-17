from pymongo import MongoClient
import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://khushalsarodein:BOladow4VbYLH95s@allinopensource.ndcpkrm.mongodb.net/?retryWrites=true&w=majority")
db = client["AllInOpensource"]

# Create or get the 'keywords' collection
keywords_collection = db["keywords"]

# Extended list of possible keywords
extended_keyword_list = [
    # ... (your extended list)
    # (No need to repeat the keyword list here again)
         "AI",
    "Artificial Intelligence",
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
    "Computer Vision",
    "Neural Networks",
    "Chatbot",
    "LLM",
    "Software",
    "Writing Tools",
    "Research Tools",
    "Automation",
    "News",
    "Blog",
    "Forum",
    "Community",
    "Networking",
    "PPT",
    "Documents",
    "PDF",
    "Canva",
    "Notion",
    "Blogging",
    "Hackathons",
    "Frameworks",
    "Content Writing",
    "Hacks",
    "Designing",
    "Text Generation",
    "Image Generation",
    "Music",
    "Sound LLM",
    "Courses",
    "Technology",
    "Profile Evaluation Tool",
    "LinkedIn Tool",
    "Code Review Tools",
    "Books",
    "Tutorials",
    "Learning Paths",
    "Free Certificates",
    "Community Website",
    "Alternative Software",
    "Video AI",
    "Video Editors",
    "Programming",
    "Coding",
    "Algorithms",
    "Data Science",
    "Cybersecurity",
    "Ethical Hacking",
    "Data Privacy",
    "Blockchain",
    "Virtual Reality",
    "Augmented Reality",
    "Internet of Things (IoT)",
    "Quantum Computing",
    "Robotics",
    "3D Printing",
    "Space Technology",
    "Health Tech",
    "Finance Tech",
    "Educational Tech",
    "Startups",
    "Entrepreneurship",
    "Business",
    "Digital Marketing",
    "Social Media",
    "SEO",
    "Web Development",
    "Mobile App Development",
    "User Experience (UX)",
    "User Interface (UI)",
    "Open Source",
    "Linux",
    "DevOps",
    "Cloud Computing",
    "Agile",
    "Scrum",
    "Project Management",
    "Remote Work",
    "Productivity",
    "Self-Improvement",
    "Mindfulness",
    "Fitness",
    "Health and Wellness",
    "Nutrition",
    "Travel",
    "Photography",
    "Gaming",
    "Entertainment",

]

# Insert extended keywords into the MongoDB collection
for i, kw in enumerate(extended_keyword_list, 1):
    keywords_collection.insert_one({"keyword": kw})
    print(f"Inserted keyword {i}: {kw}")

print("Insertion completed.")
