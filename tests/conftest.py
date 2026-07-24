import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("BEDROCK_MODEL_ID", "test-model")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import Base, get_db
from app.dependencies import get_bedrock_service
from app.main import app
from app.services.aws.bedrock_service import FakeBedrockService


@pytest.fixture
def db_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    try:
        yield engine
    finally:
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine):
    TestingSessionLocal = sessionmaker(bind=db_engine, autoflush=False, expire_on_commit=False)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_engine):
    TestingSessionLocal = sessionmaker(bind=db_engine, autoflush=False, expire_on_commit=False)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_bedrock_service] = lambda: FakeBedrockService()

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
