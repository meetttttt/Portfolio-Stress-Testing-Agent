from tests.test_analysis_api import test_analyze_endpoint
import sys
import traceback

try:
    test_analyze_endpoint()
    print("Test Passed!")
except Exception:
    traceback.print_exc()
