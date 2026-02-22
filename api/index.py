from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json, statistics, os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DATA = [{"region":"apac","latency_ms":134.19,"uptime_pct":98.205},{"region":"apac","latency_ms":115.96,"uptime_pct":98.599},{"region":"apac","latency_ms":198.82,"uptime_pct":98.579},{"region":"apac","latency_ms":183.19,"uptime_pct":98.08},{"region":"apac","latency_ms":159.45,"uptime_pct":98.774},{"region":"apac","latency_ms":108.77,"uptime_pct":98.681},{"region":"apac","latency_ms":211.74,"uptime_pct":98.89},{"region":"apac","latency_ms":113.18,"uptime_pct":98.752},{"region":"apac","latency_ms":123.98,"uptime_pct":99.08},{"region":"apac","latency_ms":140.78,"uptime_pct":97.234},{"region":"apac","latency_ms":133.96,"uptime_pct":99.183},{"region":"apac","latency_ms":239.33,"uptime_pct":97.373},{"region":"emea","latency_ms":158.73,"uptime_pct":98.039},{"region":"emea","latency_ms":181.58,"uptime_pct":98.276},{"region":"emea","latency_ms":166.51,"uptime_pct":98.65},{"region":"emea","latency_ms":172.57,"uptime_pct":98.618},{"region":"emea","latency_ms":140.84,"uptime_pct":99.09},{"region":"emea","latency_ms":212.84,"uptime_pct":97.746},{"region":"emea","latency_ms":197.51,"uptime_pct":98.914},{"region":"emea","latency_ms":110.38,"uptime_pct":97.996},{"region":"emea","latency_ms":167.17,"uptime_pct":97.833},{"region":"emea","latency_ms":170.61,"uptime_pct":97.835},{"region":"emea","latency_ms":191.3,"uptime_pct":99.16},{"region":"emea","latency_ms":215.14,"uptime_pct":97.262},{"region":"amer","latency_ms":231.23,"uptime_pct":99.045},{"region":"amer","latency_ms":169,"uptime_pct":97.824},{"region":"amer","latency_ms":204.9,"uptime_pct":97.483},{"region":"amer","latency_ms":155.55,"uptime_pct":99.117},{"region":"amer","latency_ms":166.61,"uptime_pct":99.486},{"region":"amer","latency_ms":146.23,"uptime_pct":97.478},{"region":"amer","latency_ms":177.53,"uptime_pct":97.95},{"region":"amer","latency_ms":206.3,"uptime_pct":97.869},{"region":"amer","latency_ms":229.64,"uptime_pct":98.92},{"region":"amer","latency_ms":142.31,"uptime_pct":98.633},{"region":"amer","latency_ms":188.78,"uptime_pct":98.229},{"region":"amer","latency_ms":192.52,"uptime_pct":98.717}]

@app.post("/api")
async def latency_check(request: Request):
    body = await request.json()
    regions = [r.lower() for r in body.get("regions", [])]
    threshold_ms = body.get("threshold_ms", 180)
    result = {}
    for region in regions:
        records = [r for r in DATA if r["region"] == region]
        if not records:
            result[region] = None
            continue
        latencies = sorted([r["latency_ms"] for r in records])
        uptimes = [r["uptime_pct"] for r in records]
        idx = min(int(0.95 * len(latencies)), len(latencies) - 1)
        result[region] = {
            "avg_latency": round(statistics.mean(latencies), 4),
            "p95_latency": round(latencies[idx], 4),
            "avg_uptime": round(statistics.mean(uptimes), 4),
            "breaches": sum(1 for l in latencies if l > threshold_ms),
        }
    return JSONResponse(content=result)


