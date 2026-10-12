from mainapp.ai_service import analyze_room_with_gemini


image_path = "test_room.jpg"

result = analyze_room_with_gemini(image_path)

print("\nAI ROOM ANALYSIS")
print("================")

print("Room Type:", result["room_type"])
print("Furniture:", result["furniture"])
print("Colors:", result["colors"])
print("Style:", result["style"])
print("Lighting:", result["lighting"])
print("Flooring:", result["flooring"])
print("Walls:", result["walls"])

print("\nSuggestions:")
for suggestion in result["suggestions"]:
    print("-", suggestion)