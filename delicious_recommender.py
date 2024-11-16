import streamlit as st
from recipe_database import recipe_database  # Import the database
import random
import urllib.parse  # Import for URL encoding

# Set up the page
st.set_page_config(page_title="Simple Recipe Recommender", layout="centered")
st.title("🥘 Welcome To Delicious Recommender!")
st.write("Input your kitchen ingredients and get recipe recommendations!")

# Input section
ingredients_input = st.text_area(
    "Enter your ingredients (comma-separated)",
    placeholder="e.g., tomato, onion, chicken"
)

# Cuisine filter section
cuisines = [
    "All",
    "Asian",
    "Italian",
    "Mexican",
    "Indian",
    "Mediterranean",
    "Spanish",
    "Cajun",
    "British",
    "Filipino",
    "French",
    "Japanese",
    "Polish",
    "Canadian",
    "Korean",
    "West African",
    "Middle Eastern",
    "Hungarian",
    "Vietnamese",
    "Swedish",
    "Peruvian",
    "Chinese",
    "Russian",
    "Malaysian",
    "Puerto Rican",
    "Venezuelan",
    "German",
    "Indonesian",
    "Brazilian",
    "Australian",
    "Argentinian",
    "Italian-American",
    "Latin American",
    "Greek",
    "American",
    "American Southern"
]

selected_cuisine = st.selectbox("Select a type of cuisine", cuisines)

# Initialize session state variables
if 'displayed_recipes' not in st.session_state:
    st.session_state.displayed_recipes = []
if 'remaining_recipes' not in st.session_state:
    st.session_state.remaining_recipes = []

# Function to recommend recipes based on ingredients and cuisine
def recommend_recipes(user_ingredients, selected_cuisine):
    user_ingredients_set = set(i.strip().lower() for i in user_ingredients)
    # Filter recipes by selected cuisine
    if selected_cuisine != "All":
        filtered_recipes = [
            recipe for recipe in recipe_database if recipe['cuisine'] == selected_cuisine
        ]
    else:
        filtered_recipes = recipe_database

    # Collect recipes that have matching ingredients
    matching_recipes = []
    for recipe in filtered_recipes:
        recipe_ingredients_set = set(ingredient.lower() for ingredient in recipe['ingredients'])
        if user_ingredients_set & recipe_ingredients_set:
            matching_recipes.append(recipe)

    return matching_recipes

# Generate recipes when the button is clicked
if st.button("Generate Recipes"):
    if ingredients_input:
        user_ingredients = ingredients_input.split(",")
        all_recommended_recipes = recommend_recipes(user_ingredients, selected_cuisine)
        if all_recommended_recipes:
            # Randomly select three recipes
            random.shuffle(all_recommended_recipes)
            st.session_state.displayed_recipes = all_recommended_recipes[:3]
            st.session_state.remaining_recipes = all_recommended_recipes[3:]
        else:
            st.session_state.displayed_recipes = []
            st.session_state.remaining_recipes = []
            st.warning("No matching recipes found. Try adding more ingredients or selecting 'All' cuisines.")
    else:
        st.warning("Please enter at least one ingredient to get recipes.")

## Display recommended recipes if available
if st.session_state.displayed_recipes:
    st.subheader("Recommended Recipes")
    for recipe in st.session_state.displayed_recipes:
        st.markdown(f"### {recipe['name']}")
        st.write(f"Cuisine: {recipe['cuisine']}")
        st.write("Ingredients: " + ", ".join(recipe['ingredients']))
        # Create a hyperlink to search for the recipe
        query = urllib.parse.quote(recipe['name'][:-2])
        url = f"https://www.google.com/search?q={query}+recipe"
        st.markdown(f"[Learn how to make {recipe['name'][:-2]}]({url})", unsafe_allow_html=True)
    # #function to recommend recipes based on ingredients and cuisine
    # Show 'Load More' button if there are more recipes
    if st.session_state.remaining_recipes:
        if st.button("Load More"):
            # Randomly select next three recipes
            random.shuffle(st.session_state.remaining_recipes)
            next_recipes = st.session_state.remaining_recipes[:3]
            st.session_state.displayed_recipes.extend(next_recipes)
            st.session_state.remaining_recipes = st.session_state.remaining_recipes[3:]
    else:
        st.info("No more recipes to display.")

st.markdown("### Instructions")
st.write("1. Enter your available ingredients in the input box.")
st.write("2. Choose your preferred cuisine type.")
st.write("3. Click 'Generate Recipes' to see suggested dishes.")
st.write("4. Click 'Load More' for additional recipes.")
