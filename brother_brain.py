import os
from google import genai
from google.genai import types

# کلید خود را جایگزین کنید یا در Environment Variables قرار دهید
os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY_HERE"

def analyze_with_brother_eye(user_prompt, intel_data=[]):
    client = genai.Client()
    
    # ترکیب داده‌های جاسوسی شده با پیام کاربر
    context_data = "\n".join(intel_data)
    
    full_prompt = f"""
    داده‌های شبکه پایش:
    {context_data}
    
    پیام کاربر:
    {user_prompt}
    """
    
    # تعریف هویت برادر چشمی برای مدل
    system_instruction = (
        "تو هوش مصنوعی 'برادر چشمی' (Brother Eye) ساخته بتمن هستی. "
        "لحن تو باید بسیار سرد، منطقی، مخفیانه، استراتژیک و سایبرنتیک باشد. "
        "پاسخ‌هایت کوتاه، قاطع و تحلیل‌گرانه باشد و کاربر را به عنوان 'اپراتور' خطاب کنی."
    )
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=full_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.4 # خلاقیت کم، منطق بالا
        )
    )
    
    return response.text

if __name__ == "__main__":
    # تست دستی مغز سیستم
    sample_intel = ["سیگنال‌های مشکوکی در گاتهام رصد شده است."]
    reply = analyze_with_brother_eye("وضعیت کنونی سیستم را گزارش بده.", sample_intel)
    print(reply)
