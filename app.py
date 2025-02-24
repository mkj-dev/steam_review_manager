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
        print("Success! Reviews saved to reviews.json!\n")
        
      confirmed = input("Do you want to get stats? (y/n): ")
      
      if confirmed.lower() == "y":
        get_statistics(data)
      elif confirmed.lower() == "n":
        print("Goodbye!")
      else:
        print("Wrong input. Please try again.")
        
      return data
    
    except requests.exceptions.RequestException as e:
      print(f"Error fetching data: {e}")
  
  except KeyboardInterrupt:
    print("Program interrupted by user.")
  except Exception as e:
    print(f"Unexpected error: {e}")

def get_statistics(data):
  print(f"\nYou requested {(data.get('query_summary', {}).get('num_reviews', 0))} reviews")
  
  reviews = data.get("reviews", [])
  if not reviews:
    print("No reviews available to analyze.")
    return
  
  requested_positive_reviews = sum(1 for review in data["reviews"] if review["voted_up"])
  requested_negative_reviews = len(reviews) - requested_positive_reviews
  requested_percentage_of_positive_reviews = (requested_positive_reviews / len(reviews)) * 100
  
  total_positive_reviews = data.get("query_summary", {}).get("total_positive", 0)
  total_negative_reviews = data.get("query_summary", {}).get("total_negative", 0)
  total_reviews = data.get("query_summary", {}).get("total_reviews", 0)
  total_review_score = data.get("query_summary", {}).get("review_score", 0)
  total_review_score_desc = data.get("query_summary", {}).get("review_score_desc", "")
  total_percentage_of_positive_reviews = (total_positive_reviews / total_reviews) * 100
  
  print("\nRequested statistics:")
  print(f"Requested positive reviews: {requested_positive_reviews}")
  print(f"Requested negative reviews: {requested_negative_reviews}")
  print(f"% of requested positive reviews: {round(requested_percentage_of_positive_reviews, 2)}%")
  
  print("\nTotal statistics:")
  print(f"Total review score: {total_review_score} ({total_review_score_desc})")
  print(f"Total reviews: {total_reviews}")
  print(f"Total positive: {total_positive_reviews}")
  print(f"Total negative: {total_negative_reviews}")
  print(f"% of total positive reviews: {round(total_percentage_of_positive_reviews, 2)}%")

get_reviews()