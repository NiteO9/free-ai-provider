########/
# you can change host and port and add your server domain and run in vps or hosting but now it works on locally run server file and add configuration settings in used ai tools.... 
#########\
# don't changes any configuration files in this project.... 
# The real model: gpt-4o-mini-2024-07-18
from flask import Flask, request, jsonify, Response
import requests
import json
import time
import random
import base64
import hashlib
import hmac
import re
from typing import Any, Dict, List, Optional
# my telegram channel: https://t.me/tele_t
app = Flask(__name__)
# github: https://github.com/NiteO9
@app.after_request
def add_cors(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    return response

FIREBASE_API_KEY = "AIzaSyBrHRq1560psTF4pnWChWGV4G1mgymWb8g"
FIREBASE_PROJECT = "chat-gpt-android"
FIREBASE_APP_ID = "1:753152701563:android:e94b420fd3024dcbdb1ede"
ANDROID_PACKAGE = "com.smartwidgetlabs.chatgpt"
ANDROID_CERT = "5D08264B44E0E53FBCCC70B4F016474CC6C5AB5C"
DEVICE_ID = "378F55C6F5BDFD8D"
SECRET_KEY = "vulcanlabs_smith_secret_key_2024"
FALLBACK_TOKEN = "H1a9u5gRJxpcRjfthEafDu8wOal6FH1qzOnQBCmrtv3Nwg/S/HdJGEZQPHVwdXzsQno37E0Y0V0CADOxaLLGCUJiTPlQ/AdO50BtZsC+UO1oDHEhFk/vBlLnCJ9UekkDYfWZC9RtzVtVRqXiYWFQvUelbH6wPH4Yj5LTHZ9vmfo="

access_token = None
x_auth_token = None
LAST_TOOL_SIGNATURE = None

TOOL_SYSTEM_PREFIX = """
You are a coding agent.

When a tool is needed, you must respond with ONLY valid JSON and nothing else.
Use exactly this shape:

{
  "tool_calls": [
    {
      "id": "call_1",
      "type": "function",
      "function": {
        "name": "tool_name",
        "arguments": { ... }
      }
    }
  ]
}

Rules:
- Do not write markdown.
- Do not write explanations.
- Do not wrap JSON in code fences.
- If no tool is needed, answer normally.
- If a tool is needed, output only the JSON object above.
""".strip()

def generate_request_id():
    return f"{random.randint(1000000000000, 9999999999999)}{int(time.time() * 1000)}"

def extract_content(msg):
    content = msg.get('content', '')
    if isinstance(content, list):
        text_parts = []
        for part in content:
            if isinstance(part, dict):
                if part.get('type') == 'text':
                    text_parts.append(part.get('text', ''))
                elif part.get('type') == 'image_url':
                    continue
                else:
                    text_parts.append(str(part))
            elif isinstance(part, str):
                text_parts.append(part)
        return ' '.join(text_parts)
    return str(content)

def build_tool_prompt(tools: List[Dict[str, Any]], tool_choice: Any = "auto") -> str:
    if not tools:
        return ""

    lines = [TOOL_SYSTEM_PREFIX, "", "Available tools:"]
    for t in tools:
        fn = t.get("function", {})
        name = fn.get("name", "unknown")
        desc = fn.get("description", "")
        params = fn.get("parameters", {})
        lines.append(f"- {name}: {desc}")
        lines.append(f"  parameters: {json.dumps(params, ensure_ascii=False)}")

    if tool_choice == "none":
        lines.append("")
        lines.append("Tool use is disabled for this turn.")
    elif isinstance(tool_choice, dict):
        lines.append("")
        lines.append(f"Tool choice policy: {json.dumps(tool_choice, ensure_ascii=False)}")
    else:
        lines.append("")
        lines.append("Choose the best tool when needed.")

    return "\n".join(lines)

def serialize_messages(messages: List[Dict[str, Any]]) -> str:
    parts = []
    for msg in messages:
        role = msg.get("role", "user")
        content = extract_content(msg)

        if role == "assistant" and msg.get("tool_calls"):
            parts.append(f"assistant tool_calls: {json.dumps(msg['tool_calls'], ensure_ascii=False)}")
        elif role == "tool":
            tool_call_id = msg.get("tool_call_id", "")
            parts.append(f"tool[{tool_call_id}]: {content}")
        else:
            parts.append(f"{role}: {content}")

    return "\n".join(parts)

def extract_json_block(text: str) -> Optional[Dict[str, Any]]:
    t = text.strip()

    try:
        obj = json.loads(t)
        if isinstance(obj, dict):
            return obj
    except:
        pass

    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", t, re.IGNORECASE)
    if fenced:
        candidate = fenced.group(1).strip()
        try:
            obj = json.loads(candidate)
            if isinstance(obj, dict):
                return obj
        except:
            pass

    start = t.find("{")
    end = t.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = t[start:end+1]
        try:
            obj = json.loads(candidate)
            if isinstance(obj, dict):
                return obj
        except:
            pass

    return None
# my telegram channel: https://t.me/tele_t
def to_openai_tool_calls(obj: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
    tool_calls = obj.get("tool_calls")
    if not isinstance(tool_calls, list):
        return None

    cleaned = []
    for i, tc in enumerate(tool_calls, start=1):
        if not isinstance(tc, dict):
            continue
        fn = tc.get("function", {})
        if not isinstance(fn, dict):
            continue
        name = fn.get("name")
        arguments = fn.get("arguments", {})
        if not name:
            continue
        if isinstance(arguments, str):
            args_str = arguments
        else:
            args_str = json.dumps(arguments, ensure_ascii=False)

        cleaned.append({
            "id": tc.get("id") or f"call_{i}",
            "type": "function",
            "function": {
                "name": name,
                "arguments": args_str
            }
        })

    return cleaned or None

def tool_signature(tool_calls):
    return hashlib.sha256(
        json.dumps(tool_calls, sort_keys=True).encode()
    ).hexdigest()

def get_challenge():
    url = f"https://firebaseappcheck.googleapis.com/v1/projects/{FIREBASE_PROJECT}/apps/{FIREBASE_APP_ID}:generatePlayIntegrityChallenge"
    params = {'key': FIREBASE_API_KEY}
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 15; RMX3834)',
        'Content-Type': 'application/json',
        'X-Firebase-Client': 'H4sIAAAAAAAA_6tWykhNLCpJSk0sKVayio7VUSpLLSrOzM9TslIyUqoFAFyivEQfAAAA',
        'X-Android-Package': ANDROID_PACKAGE,
        'X-Android-Cert': ANDROID_CERT
    }
    try:
        r = requests.post(url, params=params, json={}, headers=headers, timeout=10)
        return r.json().get("challenge") if r.status_code == 200 else None
    except:
        return None

def generate_x_auth_token(challenge):
    try:
        data = f"{challenge}|{DEVICE_ID}|{int(time.time())}"
        sig = hmac.new(SECRET_KEY.encode(), data.encode(), hashlib.sha256).digest()
        token = base64.b64encode(data.encode() + sig).decode()
        return token.replace('+', '-').replace('/', '_').rstrip('=')
    except:
        return FALLBACK_TOKEN

def authenticate():
    global access_token, x_auth_token
    challenge = get_challenge()
    x_auth_token = generate_x_auth_token(challenge) if challenge else FALLBACK_TOKEN

    request_id = generate_request_id()
    payload = {
        "device_id": DEVICE_ID,
        "order_id": "",
        "product_id": "",
        "purchase_token": "",
        "subscription_id": ""
    }
    headers = {
        'host': 'api.vulcanlabs.co',
        'x-vulcan-application-id': ANDROID_PACKAGE,
        'x-vulcan-request-id': request_id,
        'x-auth-token': x_auth_token,
        'user-agent': 'Chat Smith Android, Version 8.251222.2(1211)',
        'Content-Type': 'application/json'
    }
    try:
        r = requests.post("https://api.vulcanlabs.co/smith-auth/api/v1/token",
                         json=payload, headers=headers, timeout=15)
        if r.status_code == 200:
            access_token = r.json().get("AccessToken")
            return True
        return False
    except:
        return False

def send_message(messages, model_name="deepseek-reasoner", temperature=0.2, max_tokens=8192):
    global access_token, x_auth_token
    if not access_token:
        if not authenticate():
            return {"error": "Authentication failed"}

    request_id = generate_request_id()
    payload = {
        "usage_model": {"provider": "deepseek", "model": model_name},
        "user": DEVICE_ID,
        "messages": messages,
        "nsfw_check": True
    }

    headers = {
        'User-Agent': 'Chat Smith Android, Version 8.251222.2(1211)',
        'x-auth-token': x_auth_token,
        'authorization': f"Bearer {access_token}",
        'x-firebase-appcheck-error': '-9: Integrity API error (-9)',
        'x-vulcan-application-id': ANDROID_PACKAGE,
        'x-vulcan-request-id': request_id,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    try:
        r = requests.post(
            "https://api.vulcanlabs.co/smith-v2/api/v7/chat_android",
            json=payload,
            headers=headers,
            timeout=90
        )
        if r.status_code == 200:
            return {"success": True, "data": r.json()}
        return {"error": f"Status {r.status_code}", "response": r.text[:500]}
    except Exception as e:
        return {"error": str(e)}

def generate_stream_response(content):
    request_id = f"chatcmpl-{int(time.time())}"
    created = int(time.time())

    start = {
        "id": request_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": "deepseek-reasoner",
        "choices": [{"index": 0, "delta": {"role": "assistant"}, "finish_reason": None}]
    }
    yield f"data: {json.dumps(start)}\n\n"

    words = content.split()
    for i in range(0, len(words), 2):
        chunk_text = " ".join(words[i:i+2])
        if i > 0:
            chunk_text = " " + chunk_text

        chunk = {
            "id": request_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": "deepseek-reasoner",
            "choices": [{"index": 0, "delta": {"content": chunk_text}, "finish_reason": None}]
        }
        yield f"data: {json.dumps(chunk)}\n\n"
        time.sleep(0.02)

    end = {
        "id": request_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": "deepseek-reasoner",
        "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 0, "completion_tokens": len(content)//3, "total_tokens": len(content)//3}
    }
    yield f"data: {json.dumps(end)}\n\n"
    yield "data: [DONE]\n\n"

def generate_tool_call_stream(tool_calls):
    request_id = f"chatcmpl-{int(time.time())}"
    created = int(time.time())

    start = {
        "id": request_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": "deepseek-reasoner",
        "choices": [
            {
                "index": 0,
                "delta": {"role": "assistant"},
                "finish_reason": None
            }
        ]
    }
    yield f"data: {json.dumps(start)}\n\n"

    delta_chunk = {
        "id": request_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": "deepseek-reasoner",
        "choices": [
            {
                "index": 0,
                "delta": {"tool_calls": tool_calls},
                "finish_reason": None
            }
        ]
    }
    yield f"data: {json.dumps(delta_chunk)}\n\n"

    end = {
        "id": request_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": "deepseek-reasoner",
        "choices": [
            {
                "index": 0,
                "delta": {},
                "finish_reason": "tool_calls"
            }
        ]
    }
    yield f"data: {json.dumps(end)}\n\n"
    yield "data: [DONE]\n\n"

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'provider': 'chatsmith',
        'model': 'deepseek-reasoner',
        'streaming': True,
        'tools': True
    })

@app.route('/v1/chat/completions', methods=['POST', 'OPTIONS'])
def chat():
    global LAST_TOOL_SIGNATURE

    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON provided'}), 400

    messages = data.get('messages', [])
    if not messages:
        return jsonify({'error': 'Messages required'}), 400

    tools = data.get('tools', [])
    tool_choice = data.get('tool_choice', 'auto')
    stream = data.get('stream', False)

    tool_prompt = build_tool_prompt(tools, tool_choice)
    conversation_text = serialize_messages(messages)

    system_parts = []
    if tool_prompt:
        system_parts.append(tool_prompt)

    system_parts.append("Conversation transcript:\n" + conversation_text)

    system_message = "\n\n".join(system_parts)

    last_user = None
    for msg in reversed(messages):
        if msg.get("role") == "user":
            last_user = extract_content(msg)
            break

    if not last_user:
        return jsonify({'error': 'No user message found'}), 400

    formatted_messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": last_user}
    ]

    temperature = 0.0 if tools else data.get("temperature", 0.2)

    response = send_message(
        formatted_messages,
        model_name="deepseek-reasoner",
        temperature=temperature,
        max_tokens=data.get("max_tokens", 8192)
    )

    if response.get("error"):
        return jsonify({'error': response['error'], 'details': response.get('response')}), 500

    try:
        content = response["data"]["choices"][0]["Message"]["content"]
    except:
        try:
            content = response["data"]["choices"][0]["message"]["content"]
        except:
            return jsonify({'error': 'Invalid response structure'}), 500

    if tools:
        parsed = extract_json_block(content)
        if parsed:
            tool_calls = to_openai_tool_calls(parsed)
            if tool_calls:
                sig = tool_signature(tool_calls)
                if sig == LAST_TOOL_SIGNATURE:
                    if stream:
                        return Response(
                            generate_stream_response("Done."),
                            mimetype='text/event-stream',
                            headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'}
                        )
                    return jsonify({
                        "id": f"chatcmpl-{int(time.time())}",
                        "object": "chat.completion",
                        "created": int(time.time()),
                        "model": data.get("model", "deepseek-reasoner"),
                        "choices": [
                            {
                                "index": 0,
                                "message": {
                                    "role": "assistant",
                                    "content": "Done."
                                },
                                "finish_reason": "stop"
                            }
                        ],
                        "usage": {
                            "prompt_tokens": 0,
                            "completion_tokens": len("Done.") // 3,
                            "total_tokens": len("Done.") // 3
                        }
                    })
                LAST_TOOL_SIGNATURE = sig
                if stream:
                    return Response(
                        generate_tool_call_stream(tool_calls),
                        mimetype='text/event-stream',
                        headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'}
                    )
                return jsonify({
                    "id": f"chatcmpl-{int(time.time())}",
                    "object": "chat.completion",
                    "created": int(time.time()),
                    "model": data.get("model", "deepseek-reasoner"),
                    "choices": [
                        {
                            "index": 0,
                            "message": {
                                "role": "assistant",
                                "content": None,
                                "tool_calls": tool_calls
                            },
                            "finish_reason": "tool_calls"
                        }
                    ],
                    "usage": {
                        "prompt_tokens": 0,
                        "completion_tokens": len(content) // 3,
                        "total_tokens": len(content) // 3
                    }
                })

    if stream:
        return Response(
            generate_stream_response(content),
            mimetype='text/event-stream',
            headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'}
        )

    return jsonify({
        'id': f'chatcmpl-{int(time.time())}',
        'object': 'chat.completion',
        'created': int(time.time()),
        'model': data.get("model", "deepseek-reasoner"),
        'choices': [
            {
                'index': 0,
                'message': {'role': 'assistant', 'content': content},
                'finish_reason': 'stop'
            }
        ],
        'usage': {'prompt_tokens': 0, 'completion_tokens': len(content)//3, 'total_tokens': len(content)//3}
    })

@app.route('/v1/models', methods=['GET'])
def models():
    return jsonify({
        'object': 'list',
        'data': [
            {
                'id': 'deepseek-reasoner',
                'object': 'model',
                'created': int(time.time()),
                'owned_by': 'chatsmith'
            }
        ]
    })
print ("github: NiteO9 telegram: @tele_t")
if __name__ == '__main__':
    print("Starting ChatSmith Provider on 0.0.0.0:8000")
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)