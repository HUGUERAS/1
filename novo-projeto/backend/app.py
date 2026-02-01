#!/usr/bin/env python3
"""
FastAPI standalone app for Ativo Real backend
No Azure Functions dependencies - pure Python + FastAPI
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional

# Database and models
from database import SessionLocal
import models
import schemas
from sqlalchemy import select

# JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET", "CHANGE-THIS-SECRET-KEY-IN-PRODUCTION")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(user_id: int, role: str = "CLIENTE") -> str:
    """Create JWT token"""
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": user_id,
        "role": role,
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> Optional[Dict]:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Create FastAPI app
app = FastAPI(
    title="Ativo Real API",
    version="1.0.0",
    description="Backend for Ativo Real topography platform"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Ativo Real API",
        "status": "online",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    try:
        db = SessionLocal()
        db.execute(select(1))
        db.close()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

# ============================================================================
# AUTH ENDPOINTS
# ============================================================================

@app.post("/api/auth/login")
async def login(request: Request):
    """
    Login endpoint
    Body: {"email": "user@example.com", "password": "password"}
    """
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email e senha obrigatórios")
        
        db = SessionLocal()
        try:
            # Query user
            stmt = select(models.User).where(models.User.email == email)
            user = db.scalars(stmt).first()
            
            if not user:
                raise HTTPException(status_code=401, detail="Credenciais inválidas")
            
            # TODO: Verify password with bcrypt
            
            # Create tokens
            access_token = create_access_token(
                user_id=user.id,
                role=user.role.value if user.role else "CLIENTE"
            )
            
            return {
                "access_token": access_token,
                "token_type": "Bearer",
                "expires_in": 1800,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "nome": user.nome,
                    "role": user.role.value if user.role else "CLIENTE"
                }
            }
        finally:
            db.close()
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.post("/api/auth/register")
async def register(request: Request):
    """
    Register new user
    Body: {"email": "user@example.com", "password": "password", "nome": "Name", "role": "CLIENTE"}
    """
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")
        nome = data.get("nome", "")
        role = data.get("role", "CLIENTE")
        
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email e senha obrigatórios")
        
        db = SessionLocal()
        try:
            # Check if user exists
            stmt = select(models.User).where(models.User.email == email)
            existing = db.scalars(stmt).first()
            if existing:
                raise HTTPException(status_code=409, detail="Email já cadastrado")
            
            # Create new user
            new_user = models.User(
                email=email,
                password_hash=password,  # TODO: Use bcrypt
                nome=nome,
                role=models.UserRole[role] if role in models.UserRole.__members__ else models.UserRole.CLIENTE
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            return {
                "id": new_user.id,
                "email": new_user.email,
                "nome": new_user.nome,
                "role": new_user.role.value if new_user.role else "CLIENTE"
            }
        finally:
            db.close()
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.get("/api/auth/me")
async def get_current_user(request: Request):
    """Get current authenticated user"""
    try:
        # Extract token from header
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing authorization header")
        
        token = auth_header[7:]  # Remove "Bearer " prefix
        payload = verify_token(token)
        
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user_id = payload.get("sub")
        db = SessionLocal()
        try:
            user = db.query(models.User).filter(models.User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            
            return {
                "id": user.id,
                "email": user.email,
                "nome": user.nome,
                "role": user.role.value if user.role else "CLIENTE"
            }
        finally:
            db.close()
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.post("/api/auth/refresh")
async def refresh_token_endpoint(request: Request):
    """Refresh JWT token"""
    try:
        data = await request.json()
        refresh_token_val = data.get("refresh_token")
        
        if not refresh_token_val:
            raise HTTPException(status_code=400, detail="Refresh token required")
        
        payload = verify_token(refresh_token_val)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        user_id = payload.get("sub")
        role = payload.get("role", "CLIENTE")
        
        new_token = create_access_token(user_id=user_id, role=role)
        
        return {
            "access_token": new_token,
            "token_type": "Bearer",
            "expires_in": 1800
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

# ============================================================================
# PROJECT ENDPOINTS
# ============================================================================

@app.get("/api/projetos")
async def list_projetos(request: Request):
    """List all projects"""
    try:
        db = SessionLocal()
        try:
            projects = db.query(models.Project).all()
            return {
                "projetos": [
                    {
                        "id": p.id,
                        "nome": p.nome,
                        "tipo": p.tipo.value if p.tipo else None,
                        "status": p.status.value if p.status else None,
                        "created_at": p.created_at.isoformat() if p.created_at else None
                    }
                    for p in projects
                ]
            }
        finally:
            db.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.get("/api/projetos/{project_id}")
async def get_projeto(project_id: int, request: Request):
    """Get project by ID"""
    try:
        db = SessionLocal()
        try:
            project = db.query(models.Project).filter(models.Project.id == project_id).first()
            if not project:
                raise HTTPException(status_code=404, detail="Project not found")
            
            return {
                "id": project.id,
                "nome": project.nome,
                "tipo": project.tipo.value if project.tipo else None,
                "status": project.status.value if project.status else None,
                "created_at": project.created_at.isoformat() if project.created_at else None
            }
        finally:
            db.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.post("/api/projetos")
async def create_projeto(request: Request):
    """Create new project"""
    try:
        data = await request.json()
        nome = data.get("nome")
        tipo = data.get("tipo", "INDIVIDUAL")
        
        if not nome:
            raise HTTPException(status_code=400, detail="Nome do projeto obrigatório")
        
        db = SessionLocal()
        try:
            new_project = models.Project(
                nome=nome,
                tipo=models.ProjectType[tipo] if tipo in models.ProjectType.__members__ else models.ProjectType.INDIVIDUAL,
                status=models.ProjectStatus.CRIADO
            )
            db.add(new_project)
            db.commit()
            db.refresh(new_project)
            
            return {
                "id": new_project.id,
                "nome": new_project.nome,
                "tipo": new_project.tipo.value,
                "status": new_project.status.value,
                "created_at": new_project.created_at.isoformat() if new_project.created_at else None
            }
        finally:
            db.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


# ============================================================================
# LOT ENDPOINTS
# ============================================================================

@app.get("/api/lotes")
async def list_lotes(request: Request):
    """List all lots"""
    try:
        db = SessionLocal()
        try:
            lotes = db.query(models.Lot).all()
            return {
                "lotes": [
                    {
                        "id": l.id,
                        "project_id": l.project_id,
                        "nome_cliente": l.nome_cliente,
                        "status": l.status.value if l.status else None,
                        "area_ha": float(l.area_ha) if l.area_ha else 0
                    }
                    for l in lotes
                ]
            }
        finally:
            db.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.get("/api/lotes/{lot_id}")
async def get_lote(lot_id: int, request: Request):
    """Get lot by ID"""
    try:
        db = SessionLocal()
        try:
            lot = db.query(models.Lot).filter(models.Lot.id == lot_id).first()
            if not lot:
                raise HTTPException(status_code=404, detail="Lot not found")
            
            return {
                "id": lot.id,
                "project_id": lot.project_id,
                "nome_cliente": lot.nome_cliente,
                "status": lot.status.value if lot.status else None,
                "area_ha": float(lot.area_ha) if lot.area_ha else 0
            }
        finally:
            db.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@app.post("/api/lotes")
async def create_lote(request: Request):
    """Create new lot"""
    try:
        data = await request.json()
        project_id = data.get("project_id")
        nome_cliente = data.get("nome_cliente")
        
        if not project_id or not nome_cliente:
            raise HTTPException(status_code=400, detail="project_id e nome_cliente obrigatórios")
        
        db = SessionLocal()
        try:
            new_lot = models.Lot(
                project_id=project_id,
                nome_cliente=nome_cliente,
                status=models.LotStatus.PENDENTE
            )
            db.add(new_lot)
            db.commit()
            db.refresh(new_lot)
            
            return {
                "id": new_lot.id,
                "project_id": new_lot.project_id,
                "nome_cliente": new_lot.nome_cliente,
                "status": new_lot.status.value,
                "area_ha": float(new_lot.area_ha) if new_lot.area_ha else 0
            }
        finally:
            db.close()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
