from ai_engine import AIEngine

ai = AIEngine()
test_data = {
    "chair": 1,
    "vase": 1,
    "potted plant": 1,
    "tv": 1
}

print("Sending object data to Gemini...")
result = ai.generate_analysis(test_data)
print("\n--- AURA GEMINI TEST RESULT ---")
print(result)
print("-------------------------------")
