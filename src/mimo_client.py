"""
MiMo API Client — AI-Powered Development
Powered by Xiaomi MiMo-V2.5-Pro
"""
import os, json
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

@dataclass
class MiMoConfig:
    api_key: str = ""
    base_url: str = "https://api.xiaomimimo.com/v1"
    model: str = "MiMo-V2.5-Pro"
    max_tokens: int = 4096
    temperature: float = 0.7
    def __post_init__(self):
        if not self.api_key:
            self.api_key = os.getenv("MIMO_API_KEY", "")

class MiMoClient:
    def __init__(self, config=None, system_prompt=""):
        self.config = config or MiMoConfig()
        self.system_prompt = system_prompt
        self.client = OpenAI(api_key=self.config.api_key, base_url=self.config.base_url)
    def chat(self, messages, **kw):
        p = {"model": kw.get("model", self.config.model), "messages": messages,
             "temperature": kw.get("temperature", self.config.temperature),
             "max_tokens": kw.get("max_tokens", self.config.max_tokens)}
        if kw.get("json_mode"): p["response_format"] = {"type": "json_object"}
        return self.client.chat.completions.create(**p).choices[0].message.content
    def analyze(self, prompt, system=None):
        msgs = []
        s = system or self.system_prompt
        if s: msgs.append({"role": "system", "content": s})
        msgs.append({"role": "user", "content": prompt})
        return self.chat(msgs)
    def analyze_json(self, prompt, system=None):
        return json.loads(self.analyze(prompt + "\nRespond ONLY with valid JSON.", system))
