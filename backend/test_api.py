"""
Quick test script for FeedBreak API
Run this after starting the server to verify all endpoints work
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/v1"

# Test device ID
DEVICE_ID = "test-device-123"

def print_response(endpoint: str, response: requests.Response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"Endpoint: {endpoint}")
    print(f"Status: {response.status_code}")
    print(f"Response:")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)
    print(f"{'='*60}\n")

def test_health():
    """Test health check endpoint"""
    print("🔍 Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print_response("GET /health", response)
    return response.status_code == 200

def test_create_user():
    """Test user creation"""
    print("👤 Testing User Creation...")
    user_data = {
        "device_id": DEVICE_ID,
        "nome": "João Silva",
        "idade": 18,
        "interesses": ["ciência", "tecnologia", "matemática"],
        "nivel_educacional": "ensino_medio"
    }
    response = requests.post(f"{API_BASE}/user", json=user_data)
    print_response("POST /api/v1/user", response)
    return response.status_code == 200

def test_get_user():
    """Test get user"""
    print("👤 Testing Get User...")
    response = requests.get(f"{API_BASE}/user/{DEVICE_ID}")
    print_response(f"GET /api/v1/user/{DEVICE_ID}", response)
    return response.status_code == 200

def test_list_videos():
    """Test list videos"""
    print("🎥 Testing List Videos...")
    response = requests.get(f"{API_BASE}/videos?limit=5")
    print_response("GET /api/v1/videos", response)
    return response.status_code == 200

def test_next_video():
    """Test get next video"""
    print("▶️  Testing Next Video...")
    response = requests.get(f"{API_BASE}/videos/next?device_id={DEVICE_ID}")
    print_response("GET /api/v1/videos/next", response)
    
    if response.status_code == 200:
        data = response.json()
        if data.get("video"):
            return data["video"]["id"]
    return None

def test_record_progress(video_id: str):
    """Test record progress"""
    print("📊 Testing Record Progress...")
    progress_data = {
        "device_id": DEVICE_ID,
        "video_id": video_id,
        "completed": True
    }
    response = requests.post(f"{API_BASE}/progress", json=progress_data)
    print_response("POST /api/v1/progress", response)
    return response.status_code == 200

def test_get_question(video_id: str):
    """Test get question (requires n8n)"""
    print("❓ Testing Get Question (requires n8n)...")
    response = requests.get(
        f"{API_BASE}/questions",
        params={"device_id": DEVICE_ID, "video_id": video_id}
    )
    print_response("GET /api/v1/questions", response)
    
    if response.status_code == 200:
        return response.json().get("id")
    return None

def test_submit_answer(question_id: str, video_id: str):
    """Test submit text answer"""
    print("💬 Testing Submit Answer...")
    answer_data = {
        "device_id": DEVICE_ID,
        "question_id": question_id,
        "video_id": video_id,
        "text_response": "Fotossíntese é o processo onde plantas verdes convertem luz solar em energia química usando clorofila. A planta absorve luz solar, água e dióxido de carbono para produzir glicose (energia) e oxigênio como subproduto."
    }
    response = requests.post(f"{API_BASE}/answer", json=answer_data)
    print_response("POST /api/v1/answer", response)
    return response.status_code == 200

def test_dashboard_stats():
    """Test dashboard stats"""
    print("📈 Testing Dashboard Stats...")
    response = requests.get(f"{API_BASE}/dashboard/stats")
    print_response("GET /api/v1/dashboard/stats", response)
    return response.status_code == 200

def test_dashboard_e2e():
    """Test dashboard E2E responses"""
    print("📋 Testing Dashboard E2E...")
    response = requests.get(f"{API_BASE}/dashboard/e2e?limit=10")
    print_response("GET /api/v1/dashboard/e2e", response)
    return response.status_code == 200

def run_all_tests():
    """Run all tests in sequence"""
    print("\n🚀 Starting FeedBreak API Tests...\n")
    
    results = []
    
    # Basic tests
    results.append(("Health Check", test_health()))
    results.append(("Create User", test_create_user()))
    results.append(("Get User", test_get_user()))
    results.append(("List Videos", test_list_videos()))
    
    # Video flow test
    video_id = test_next_video()
    if video_id:
        results.append(("Next Video", True))
        results.append(("Record Progress", test_record_progress(video_id)))
        
        # E2E flow (may fail if n8n not configured)
        try:
            question_id = test_get_question(video_id)
            if question_id:
                results.append(("Get Question", True))
                results.append(("Submit Answer", test_submit_answer(question_id, video_id)))
            else:
                results.append(("Get Question", False))
                print("⚠️  Note: Question generation may require n8n webhook")
        except Exception as e:
            results.append(("E2E Flow", False))
            print(f"⚠️  E2E test failed (likely n8n not configured): {e}")
    else:
        results.append(("Next Video", False))
        print("⚠️  No videos available. Please add videos to database first.")
    
    # Dashboard tests
    results.append(("Dashboard Stats", test_dashboard_stats()))
    results.append(("Dashboard E2E", test_dashboard_e2e()))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    print(f"\n{passed_count}/{total_count} tests passed")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server")
        print("Make sure the server is running: python app/main.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")

