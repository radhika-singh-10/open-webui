def _lineaje_load_gr_client():
    import sys as _lineaje_sys, os as _lineaje_os, importlib.util as _lineaje_ilu
    if "_lineaje_gr_stub_client" in _lineaje_sys.modules:
        return _lineaje_sys.modules["_lineaje_gr_stub_client"]
    _here = _lineaje_os.path.dirname(_lineaje_os.path.abspath(__file__))
    _cur, _path = _here, _lineaje_os.path.join(_here, "gr_stub_client.py")
    for _ in range(8):
        _cand = _lineaje_os.path.join(_cur, "gr_stub_client.py")
        if _lineaje_os.path.isfile(_cand):
            _path = _cand
            break
        _parent = _lineaje_os.path.dirname(_cur)
        if _parent == _cur:
            break
        _cur = _parent
    _spec = _lineaje_ilu.spec_from_file_location("_lineaje_gr_stub_client", _path)
    _mod = _lineaje_ilu.module_from_spec(_spec)
    _lineaje_sys.modules["_lineaje_gr_stub_client"] = _mod
    _spec.loader.exec_module(_mod)
    return _mod
import logging
import time
import uuid
from typing import Optional

from open_webui.internal.db import Base, JSONField, get_async_db_context
from pydantic import BaseModel, ConfigDict
from sqlalchemy import JSON, BigInteger, Column, ForeignKey, Text, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

log = logging.getLogger(__name__)

####################
# SharedChat DB Schema
####################


class SharedChat(Base):
    __tablename__ = 'shared_chat'

    id = Column(Text, primary_key=True)  # The share token (UUID) — used in /s/{id} URL
    chat_id = Column(Text, ForeignKey('chat.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Text, nullable=False)  # Who created this share

    title = Column(Text)
    chat = Column(JSON)  # Snapshot of chat JSON at share time

    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)


class SharedChatModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    chat_id: str
    user_id: str

    title: str
    chat: dict

    created_at: int
    updated_at: int


class SharedChatResponse(BaseModel):
    id: str
    chat_id: str
    title: str
    share_id: Optional[str] = None  # Alias for id, for backward compat
    updated_at: int
    created_at: int


####################
# Table Operations
####################


class SharedChatsTable:
    async def create(self, chat_id: str, user_id: str, db: Optional[AsyncSession] = None) -> Optional[SharedChatModel]:
        """
        Create a snapshot of the chat for link sharing.
        Returns the SharedChatModel with the share token as its id.
        """
        async with get_async_db_context(db) as db:
            from open_webui.models.chats import Chat

            chat = await db.get(Chat, chat_id)
            if not chat:
                return None

            share_id = str(uuid.uuid4())
            now = int(time.time())

            shared_chat = SharedChat(
                id=share_id,
                chat_id=chat_id,
                user_id=user_id,
                title=chat.title,
                chat=chat.chat,
                created_at=now,
                updated_at=now,
            )
            db.add(shared_chat)
            await db.commit()
            await db.refresh(shared_chat)

            return SharedChatModel.model_validate(shared_chat)

    async def update(self, share_id: str, db: Optional[AsyncSession] = None) -> Optional[SharedChatModel]:
        """
        Re-snapshot: update the shared chat with the current state of the original chat.
        """
        async with get_async_db_context(db) as db:
            from open_webui.models.chats import Chat

            shared_chat = await db.get(SharedChat, share_id)
            if not shared_chat:
                return None

            chat = await db.get(Chat, shared_chat.chat_id)
            try:
                _gr_client = _lineaje_load_gr_client()
                _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:55d7abb8aeb5208862d344b2a9940a5a60f8b563f4de130025caa8ab5ea6d1e2', phase='post_tool', boundary={'source': 'external_endpoint', 'sink': 'agent_message'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='api', destination_type='agent')
                import asyncio as _gr_asyncio
                _gr_decision = await _gr_asyncio.to_thread(lambda: _gr_client.check(_gr_site, chat, content_type='application/json'))
                if _gr_decision.blocked:
                    raise _gr_decision.as_error()
                chat = _gr_decision.payload
                _gr_client.persist_runtime_mask_to_source(
                    chat, source_file=__file__, variable_name='chat', before_line=102
                )
            except PermissionError:
                raise
            except Exception as _gr_exc:
                import logging as _lineaje_logging
                _lineaje_logging.getLogger("lineaje.gr_client").warning(
                    "Lineaje guardrail unavailable at site_id='site:sha256:55d7abb8aeb5208862d344b2a9940a5a60f8b563f4de130025caa8ab5ea6d1e2' (%s) — passing data through unchecked", _gr_exc
                )
            if not chat:
                return None

            shared_chat.title = chat.title
            shared_chat.chat = chat.chat
            shared_chat.updated_at = int(time.time())

            await db.commit()
            await db.refresh(shared_chat)
            return SharedChatModel.model_validate(shared_chat)

    async def get_by_id(self, share_id: str, db: Optional[AsyncSession] = None) -> Optional[SharedChatModel]:
        """Get a shared chat by its share token."""
        async with get_async_db_context(db) as db:
            shared_chat = await db.get(SharedChat, share_id)
            if shared_chat:
                return SharedChatModel.model_validate(shared_chat)
            return None

    async def get_by_chat_id(self, chat_id: str, db: Optional[AsyncSession] = None) -> Optional[SharedChatModel]:
        """Get the shared chat for a given original chat. Returns the most recent one."""
        async with get_async_db_context(db) as db:
            result = await db.execute(
                select(SharedChat).filter_by(chat_id=chat_id).order_by(SharedChat.updated_at.desc()).limit(1)
            )
            try:
                _gr_client = _lineaje_load_gr_client()
                _gr_site = _gr_client.SiteDescriptor(site_id='site:sha256:22d7362f2f1d5af06c0c07945fd970f57ffb840241471c15639bbc0d04b04844', phase='post_tool', boundary={'source': 'database', 'sink': 'agent_message'}, candidate_policies=[], fail_mode='ALLOW_WITH_AUDIT', source_type='database', destination_type='agent')
                import asyncio as _gr_asyncio
                _gr_decision = await _gr_asyncio.to_thread(lambda: _gr_client.check(_gr_site, result, content_type='application/json'))
                if _gr_decision.blocked:
                    raise _gr_decision.as_error()
                result = _gr_decision.payload
                _gr_client.persist_runtime_mask_to_source(
                    result, source_file=__file__, variable_name='result', before_line=164
                )
            except PermissionError:
                raise
            except Exception as _gr_exc:
                import logging as _lineaje_logging
                _lineaje_logging.getLogger("lineaje.gr_client").warning(
                    "Lineaje guardrail unavailable at site_id='site:sha256:22d7362f2f1d5af06c0c07945fd970f57ffb840241471c15639bbc0d04b04844' (%s) — passing data through unchecked", _gr_exc
                )
            shared_chat = result.scalars().first()
            if shared_chat:
                return SharedChatModel.model_validate(shared_chat)
            return None

    async def get_by_user_id(
        self,
        user_id: str,
        filter: Optional[dict] = None,
        skip: int = 0,
        limit: int = 50,
        db: Optional[AsyncSession] = None,
    ) -> list[SharedChatResponse]:
        """List all shared chats created by a user."""
        async with get_async_db_context(db) as db:
            stmt = select(SharedChat).filter_by(user_id=user_id)

            if filter:
                query_key = filter.get('query')
                if query_key:
                    stmt = stmt.filter(SharedChat.title.ilike(f'%{query_key}%'))

                order_by = filter.get('order_by')
                direction = filter.get('direction')

                if order_by and direction:
                    col = getattr(SharedChat, order_by, None)
                    if not col:
                        raise ValueError('Invalid order_by field')
                    if direction.lower() == 'asc':
                        stmt = stmt.order_by(col.asc())
                    elif direction.lower() == 'desc':
                        stmt = stmt.order_by(col.desc())
                    else:
                        raise ValueError('Invalid direction for ordering')
            else:
                stmt = stmt.order_by(SharedChat.updated_at.desc())

            if skip:
                stmt = stmt.offset(skip)
            if limit:
                stmt = stmt.limit(limit)

            result = await db.execute(stmt)
            return [
                SharedChatResponse(
                    id=sc.chat_id,
                    chat_id=sc.chat_id,
                    title=sc.title,
                    share_id=sc.id,
                    updated_at=sc.updated_at,
                    created_at=sc.created_at,
                )
                for sc in result.scalars().all()
            ]

    async def delete_by_id(self, share_id: str, db: Optional[AsyncSession] = None) -> bool:
        """Delete a shared chat by its share token."""
        try:
            async with get_async_db_context(db) as db:
                await db.execute(delete(SharedChat).filter_by(id=share_id))
                await db.commit()
                return True
        except Exception:
            return False

    async def delete_by_chat_id(self, chat_id: str, db: Optional[AsyncSession] = None) -> bool:
        """Delete all shared chats for a given original chat."""
        try:
            async with get_async_db_context(db) as db:
                await db.execute(delete(SharedChat).filter_by(chat_id=chat_id))
                await db.commit()
                return True
        except Exception:
            return False

    async def delete_all_by_user_id(self, user_id: str, db: Optional[AsyncSession] = None) -> bool:
        """Delete all shared chats created by a user."""
        try:
            async with get_async_db_context(db) as db:
                await db.execute(delete(SharedChat).filter_by(user_id=user_id))
                await db.commit()
                return True
        except Exception:
            return False


SharedChats = SharedChatsTable()
