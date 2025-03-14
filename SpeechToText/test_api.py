import os
from dotenv import load_dotenv
from ai_analysis import analyze_brainstorming, generate_action_items, suggest_improvements, summarize_text

load_dotenv()

def test_analysis():
    # Test text focused on document management and PDF handling
    test_text = """
    We need to improve our document signing workflow. The current process takes too long and users get confused.
    Key issues:
    1. PDF upload sometimes fails with large files
    2. Email notifications are delayed when sharing documents
    3. Electronic signatures don't always show up correctly on mobile
    4. Users want a way to track who has viewed their documents
    
    Suggestions from team:
    - Add a progress bar for large file uploads
    - Implement real-time signature status updates
    - Create email templates for different sharing scenarios
    - Add a document access log feature
    - Improve mobile UI for signature placement
    """
    
    print("\n=== Testing Analysis ===")
    result = analyze_brainstorming(test_text)
    if result['success']:
        print("\nAnalysis Result:")
        print(result['analysis'])
    else:
        print("\nAnalysis Error:", result['error'])
    
    print("\n=== Testing Action Items ===")
    result = generate_action_items(test_text)
    if result['success']:
        print("\nAction Items:")
        print(result['action_items'])
    else:
        print("\nAction Items Error:", result['error'])
    
    print("\n=== Testing Improvements ===")
    result = suggest_improvements(test_text)
    if result['success']:
        print("\nImprovement Suggestions:")
        print(result['suggestions'])
    else:
        print("\nImprovements Error:", result['error'])
    
    print("\n=== Testing Summary ===")
    result = summarize_text(test_text)
    if result['success']:
        print("\nSummary:")
        print(result['summary'])
    else:
        print("\nSummary Error:", result['error'])

if __name__ == "__main__":
    if not os.getenv('TOGETHER_API_KEY'):
        print("Error: TOGETHER_API_KEY not found in environment variables")
        print("Please add your Together.ai API key to the .env file:")
        print('TOGETHER_API_KEY="your-api-key-here"')
    else:
        test_analysis()
