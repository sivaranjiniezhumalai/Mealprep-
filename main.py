import requests
import streamlit
import random
import pandas

get_categories_api = "http://www.themealdb.com/api/json/v1/1/list.php?c=list?"
get_categories_response = requests.get(get_categories_api)
get_categories = get_categories_response.json().get("meals")
categories = ["Select a category"]
for category in get_categories:
    categories.append(category.get("strCategory"))

streamlit.title("Meal Planner")
selected_category = streamlit.selectbox("Select the Food Category:", categories)

if selected_category != "Select a category":
    get_food_list_by_category_api = "https://www.themealdb.com/api/json/v1/1/filter.php?c=" + selected_category
    get_food_list_by_category_response = requests.get(get_food_list_by_category_api)
    get_food_list_by_category = get_food_list_by_category_response.json().get("meals")
    get_food_id = random.choice(get_food_list_by_category).get("idMeal")
    
    get_meal_recipe_by_id_api = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=" + get_food_id
    get_meal_recipe_by_id_response = requests.get(get_meal_recipe_by_id_api)
    meal_data = get_meal_recipe_by_id_response.json().get("meals")[0]
    # streamlit.write(get_meal_recipe_by_id)

    # Streamlit UI setup
    streamlit.title(meal_data["strMeal"])  # Display meal name
    streamlit.image(meal_data["strMealThumb"])  # Display meal image

    # Ingredient listcd c:/Users/
    ingredients = []
    measurements = []

    # Loop through the ingredients and measurements
    for i in range(1, 21):
        ingredient = meal_data.get(f"strIngredient{i}")
        measurement = meal_data.get(f"strMeasure{i}")
        
        if ingredient and ingredient.strip():  # Only include non-empty ingredients
            ingredients.append(ingredient.strip())
            measurements.append(measurement.strip() if measurement else 'N/A')

    # Create a DataFrame for ingredients and measurements
    ingredient_df = pandas.DataFrame({
        'Ingredient': ingredients,
        'Measurement': measurements
    })

    # Display the ingredient list in a table
    streamlit.subheader("Ingredients")
    streamlit.table(ingredient_df)

    # Recipe instructions
    streamlit.subheader("Instructions")
    streamlit.write(meal_data["strInstructions"])
