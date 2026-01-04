import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.services import user_service
from app.schemas.user import UserCreate
from app.models.user import UserRole
from app.core import security

logger = logging.getLogger(__name__)

async def init_db(db: AsyncSession) -> None:
    """
    Initialize the database with an admin user if it doesn't exist.
    """
    try:
        admin_email = "admin"
        admin_password = "1234"
        
        user = await user_service.get_by_email(db, email=admin_email)
        if not user:
            logger.info(f"Creating initial admin user: {admin_email}")
            user_in = UserCreate(
                email=admin_email,
                password=admin_password,
                name="Administrator",
                is_active=True
            )
            # Create user
            # We need to manually set role to ADMIN since UserCreate doesn't have role
            # user_service.create uses User model which has default role USER
            
            # Using user_service.create to handle password hashing
            # But we need to override the role after creation or do it manually here.
            
            # Let's do it manually to ensure role is set correctly
            db_obj = await user_service.create(db, user_in)
            
            # Update role to ADMIN
            db_obj.role = UserRole.ADMIN
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            
            logger.info("Admin user created successfully")
        else:
            logger.info(f"Admin user {admin_email} already exists")
            
    except Exception as e:
        logger.error(f"Error initializing database: {e}")

