from app.services.llm_extractor import llm_extractor
import logging

logging.basicConfig(level=logging.DEBUG)

with open('scripts/test_screenshot.png', 'rb') as f:
    result = llm_extractor.extract(f.read(), 'test.png')
    print(result)
