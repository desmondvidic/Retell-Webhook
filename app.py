from fastapi import FastAPI, Request
import httpx

app = FastAPI()

KB_API_URL = "https://bbqn-backend.onrender.com/kb/query"

@app.post("/retell-webhook")
async def retell_webhook(req: Request):
    data = await req.json()
    
    user_message = data.get("message") or data.get("query") or ""
    city = data.get("city", "Delhi and Bangalore")
    location = data.get("location")

    params = {"city": city, "query": user_message}
    if location:
        params["location"] = location

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(KB_API_URL, params=params)
            response.raise_for_status()
            kb_response = response.json()
            answer = kb_response.get("answer", "Sorry, no answer found.")
        except Exception:
            answer = "Sorry, I could not fetch the information right now."

    return {"reply": answer}
