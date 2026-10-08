"""
Cloud Security Alert Lamp - FastAPI Backend Application
Integrates AWS S3, Lambda, DynamoDB, SNS, and AWS IoT Core.
Provides REST API, WebSockets (/ws), and static file serving for the Web Dashboard.
"""

import os
import json
import time
import logging
import asyncio
from datetime import datetime
from typing import Set, Dict, Any, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import boto3
from botocore.exceptions import ClientError

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("cloud_lamp.backend")

# AWS Environment Configuration
REGION = os.getenv("AWS_REGION", "us-east-1")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE_NAME", "SecurityEvents")
SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "")
IOT_ENDPOINT = os.getenv("AWS_IOT_ENDPOINT", "")
IOT_TOPIC = os.getenv("AWS_IOT_TOPIC", "cloud/security/alerts")
LAMBDA_FUNCTION_NAME = os.getenv("LAMBDA_FUNCTION_NAME", "CloudSecurityS3Auditor")

# Global LED & Security State Memory
class SystemState:
    def __init__(self):
        self.status = "OK"  # "OK" or "ALERT"
        self.public_count = 0
        self.public_buckets: List[str] = []
        self.total_scanned = 0
        self.last_scan_time = datetime.now().isoformat()
        self.events_history: List[Dict[str, Any]] = []

system_state = SystemState()

# WebSocket Connection Manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WebSocket client connected. Total clients: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket client disconnected. Total clients: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        if not self.active_connections:
            return
        dead_connections = set()
        msg_text = json.dumps(message)
        for connection in self.active_connections:
            try:
                await connection.send_text(msg_text)
            except Exception:
                dead_connections.add(connection)
        for dead in dead_connections:
            self.active_connections.discard(dead)

ws_manager = ConnectionManager()

# AWS Audit Logic Helper
def audit_s3_buckets_local():
    """Performs S3 audit directly via boto3 SDK."""
    s3 = boto3.client('s3', region_name=REGION)
    public_buckets = []
    total_buckets = 0

    try:
        resp = s3.list_buckets()
        buckets = resp.get('Buckets', [])
        total_buckets = len(buckets)

        for b in buckets:
            b_name = b['Name']
            is_pub = False
            
            # Check Public Access Block
            try:
                pab = s3.get_public_access_block(Bucket=b_name)
                cfg = pab.get('PublicAccessBlockConfiguration', {})
                if not (cfg.get('BlockPublicAcls') and cfg.get('IgnorePublicAcls') and 
                        cfg.get('BlockPublicPolicy') and cfg.get('RestrictPublicBuckets')):
                    is_pub = True
            except ClientError:
                is_pub = True

            # Check Bucket Policy
            if not is_pub:
                try:
                    pol = s3.get_bucket_policy_status(Bucket=b_name)
                    if pol.get('PolicyStatus', {}).get('IsPublic', False):
                        is_pub = True
                except ClientError:
                    pass

            if is_pub:
                public_buckets.append(b_name)

    except Exception as e:
        logger.warning(f"Local S3 audit warning: {e}")

    status = "ALERT" if len(public_buckets) > 0 else "OK"
    now_str = datetime.now().isoformat()
    
    system_state.status = status
    system_state.public_count = len(public_buckets)
    system_state.public_buckets = public_buckets
    system_state.total_scanned = total_buckets
    system_state.last_scan_time = now_str

    event_record = {
        "eventId": f"EVT-{int(time.time())}",
        "status": status,
        "public_buckets_count": len(public_buckets),
        "public_buckets": public_buckets,
        "total_scanned": total_buckets,
        "timestamp": now_str
    }
    system_state.events_history.insert(0, event_record)
    if len(system_state.events_history) > 50:
        system_state.events_history.pop()

    return event_record

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("==================================================")
    logger.info("🚀 Cloud Security Alert Lamp Backend Starting...")
    logger.info(f"⚡ AWS Region: {REGION}")
    logger.info("==================================================")
    
    # Run initial scan
    try:
        audit_s3_buckets_local()
    except Exception as e:
        logger.warning(f"Startup scan note: {e}")
        
    yield
    logger.info("🛑 Backend Shutting down...")

app = FastAPI(
    title="Cloud Security Alert Lamp API",
    description="Backend API for AWS S3 Security Audit & Physical IoT Alert Lamp",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoints
@app.get("/api/health")
def health():
    return {
        "status": "HEALTHY",
        "service": "Cloud Security Alert Lamp Backend",
        "region": REGION,
        "system_status": system_state.status,
        "public_buckets_count": system_state.public_count
    }

@app.get("/api/dashboard")
def get_dashboard():
    return {
        "status": system_state.status,
        "public_buckets_count": system_state.public_count,
        "public_buckets": system_state.public_buckets,
        "total_scanned": system_state.total_scanned,
        "last_scan_time": system_state.last_scan_time,
        "events_count": len(system_state.events_history)
    }

@app.get("/api/events")
def get_events():
    # Try fetching from DynamoDB if table exists
    try:
        dynamodb = boto3.resource('dynamodb', region_name=REGION)
        table = dynamodb.Table(DYNAMODB_TABLE)
        resp = table.scan(Limit=20)
        items = resp.get('Items', [])
        if items:
            return {"source": "DynamoDB", "events": items}
    except Exception:
        pass
    return {"source": "MemoryCache", "events": system_state.events_history}

@app.post("/api/scan")
async def trigger_scan(background_tasks: BackgroundTasks):
    """Triggers Lambda auditor scan or local scan and broadcasts via WebSocket."""
    # Attempt Lambda invocation if function exists
    result = None
    try:
        lam = boto3.client('lambda', region_name=REGION)
        res = lam.invoke(FunctionName=LAMBDA_FUNCTION_NAME, InvocationType='RequestResponse')
        payload = json.loads(res['Payload'].read().decode('utf-8'))
        result = payload
    except Exception as e:
        logger.info(f"Lambda trigger note ({e}); falling back to local boto3 scan...")
        result = audit_s3_buckets_local()

    # Broadcast via WebSocket
    await ws_manager.broadcast({
        "type": "SCAN_COMPLETE",
        "data": result,
        "dashboard": {
            "status": system_state.status,
            "public_buckets_count": system_state.public_count,
            "public_buckets": system_state.public_buckets,
            "total_scanned": system_state.total_scanned
        }
    })

    return {"message": "Security scan completed successfully", "result": result}

# WebSocket for Real-time Dashboard Updates
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        # Send initial state immediately
        await websocket.send_text(json.dumps({
            "type": "INITIAL_STATE",
            "data": {
                "status": system_state.status,
                "public_buckets_count": system_state.public_count,
                "public_buckets": system_state.public_buckets,
                "total_scanned": system_state.total_scanned,
                "last_scan_time": system_state.last_scan_time
            }
        }))
        while True:
            data = await websocket.receive_text()
            try:
                parsed = json.loads(data)
                if parsed.get("action") == "SCAN":
                    res = audit_s3_buckets_local()
                    await ws_manager.broadcast({
                        "type": "SCAN_COMPLETE",
                        "data": res
                    })
                elif parsed.get("action") == "PING":
                    await websocket.send_text(json.dumps({"type": "PONG"}))
            except Exception:
                pass
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)
    except Exception as e:
        logger.debug(f"WebSocket closed: {e}")
        ws_manager.disconnect(websocket)

# Mount Web Dashboard Frontend Static Files
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "web_dashboard"))
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="web_dashboard")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
