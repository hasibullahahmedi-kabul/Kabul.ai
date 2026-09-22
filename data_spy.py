import requests
from bs4 import BeautifulSoup

def fetch_global_intel():
    print("[INFO] در حال هک شبکه‌ها و جمع‌آوری اطلاعات...")
    # به عنوان مثال، اخبار یک سایت تکنولوژی/عمومی را هدف قرار می‌دهیم
    url = "https://zoomit.ir" 
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # استخراج تگ‌های هدینگ (تیترهای خبری)
        headlines = soup.find_all(['h2', 'h3'], limit=5)
        
        intel_reports = []
        for index, line in enumerate(headlines, 1):
            clean_text = line.get_text().strip()
            if clean_text:
                intel_reports.append(f"گزارش {index}: {clean_text}")
                
        return intel_reports
    except Exception as e:
        return [f"خطا در شبکه جاسوسی: {str(e)}"]

if __name__ == "__main__":
    reports = fetch_global_intel()
    for report in reports:
        print(report)
