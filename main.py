import urllib.request
import urllib.parse
import json
import webbrowser

def get_corrected_info(query):
    try:
        search_query = urllib.parse.quote(query)
        search_url = f"https://bn.wikipedia.org/w/api.php?action=opensearch&search={search_query}&limit=1&namespace=0&format=json"
        
        headers = {'User-Agent': 'XtremeAI/2.0'}
        req_search = urllib.request.Request(search_url, headers=headers)
        
        with urllib.request.urlopen(req_search) as response:
            search_data = json.loads(response.read().decode())
            
            if len(search_data) > 1 and search_data[1]:
                corrected_title = search_data[1][0]
                page_url = search_data[3][0] # উইকিপিডিয়া লিংকের ইনডেক্স
                
                topic = urllib.parse.quote(corrected_title.replace(" ", "_"))
                summary_url = f"https://bn.wikipedia.org/api/rest_v1/page/summary/{topic}"
                
                req_summary = urllib.request.Request(summary_url, headers=headers)
                with urllib.request.urlopen(req_summary) as res:
                    data = json.loads(res.read().decode())
                    return {
                        "text": f"🔍 আপনি কি বুঝিয়েছেন: {corrected_title}?\n\n📌 তথ্য: {data.get('extract')}",
                        "url": page_url
                    }
            else:
                return {"text": "❌ দুঃখিত, Xtreme AI এই বিষয়ে কোনো তথ্য খুঁজে পায়নি。", "url": None}
                
    except Exception:
        return {"text": "📡 ইন্টারনেট সংযোগ বা তথ্য সংগ্রহে সমস্যা হয়েছে।", "url": None}

def xtreme_ai_chat(query):
    query = query.lower()
    
    if query in ["hi", "hello", "হাই", "হ্যালো"]:
        return "হ্যালো! আমি Xtreme AI। আপনাকে কীভাবে সাহায্য করতে পারি?"
    elif "কেমন আছো" in query:
        return "আমি ভালো আছি! আপনি কেমন আছেন? আপনি কি আজ কিছু জানতে চান?"
    elif "নাম কি" in query:
        return "আমার নাম Xtreme AI। আমি আপনার স্মার্ট অ্যাসিস্ট্যান্ট।"
    else:
        return None

def main():
    print("====================================")
    print("      🚀 XTREME AI (Smart Assistant) ")
    print("====================================")
    print("বন্ধ করতে 'exit' লিখুন।\n")
    
    while True:
        user_input = input("👤 আপনি: ").strip()
        
        if user_input.lower() == 'exit':
            print("বিদায়! ভালো থাকবেন।")
            break
            
        if not user_input:
            continue
            
        chat_reply = xtreme_ai_chat(user_input)
        
        if chat_reply:
            print(f"🤖 Xtreme AI: {chat_reply}")
        else:
            print("⌛ তথ্য বিশ্লেষণ করা হচ্ছে...")
            result = get_corrected_info(user_input)
            print(f"\n--- ফলাফল ---\n{result['text']}\n--------------")
            
            # ওপেন লিংক অপশন
            if result['url']:
                open_link = input("\n🔗 আপনি কি পুরো পেজটি ব্রাউজারে ওপেন করতে চান? (y/n): ").lower()
                if open_link == 'y':
                    webbrowser.open(result['url'])
                    print("🌐 ব্রাউজারে পেজটি ওপেন হচ্ছে...")

if __name__ == "__main__":
    main()
