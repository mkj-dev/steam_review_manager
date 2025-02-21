import requests
import json
def get_reviews():
  try:    
    while True:
      try:
        inputAppId = int(input("Enter the app ID: "))
        inputNumberOfReviews = int(input("Enter the number of reviews you want to collect (max. 100): "))
        
        if inputAppId < 1 or not (1 <= inputNumberOfReviews <= 100):
          print("Invalid input. App ID must be greater than 0, and number of reviews must be between 1 and 100.")
          continue
        
        break
      except ValueError:
        print("Invalid input. App ID and number of reviews must be numbers.")
        
    url = f"https://store.steampowered.com/appreviews/{inputAppId}/?json=1&num_per_page={inputNumberOfReviews}"
    
    try:
      response = requests.get(url ,timeout=10)
      response.raise_for_status()
      
      data = response.json()
      
      with open("reviews.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        print("Success! Reviews saved to reviews.json!")
        
    except requests.exceptions.RequestException as e:
      print(f"Error fetching data: {e}")
  
  except KeyboardInterrupt:
    print("Program interrupted by user.")
  except Exception as e:
    print(f"Unexpected error: {e}")
    
get_reviews()