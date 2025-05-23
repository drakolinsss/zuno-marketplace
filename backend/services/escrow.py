from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
import logging

from db.models import Escrow, Dispute, User, Product
from schemas.escrow import EscrowCreate, DisputeCreate, DisputeResolve, EscrowStatus, DisputeStatus

logger = logging.getLogger(__name__)

class EscrowService:
    @staticmethod
    async def create_escrow(db: Session, escrow_data: EscrowCreate) -> Escrow:
        """Create a new escrow transaction."""
        try:
            # Validate buyer and seller exist
            buyer = db.query(User).filter(User.id == escrow_data.buyer_id).first()
            seller = db.query(User).filter(User.id == escrow_data.seller_id).first()
            product = db.query(Product).filter(Product.id == escrow_data.product_id).first()

            if not buyer or not seller:
                raise HTTPException(status_code=404, detail="Buyer or seller not found")
            if not product:
                raise HTTPException(status_code=404, detail="Product not found")

            # Create escrow record
            release_time = datetime.utcnow() + timedelta(days=14)  # Auto-release after 14 days
            db_escrow = Escrow(
                buyer_id=escrow_data.buyer_id,
                seller_id=escrow_data.seller_id,
                product_id=escrow_data.product_id,
                amount=escrow_data.amount,
                status=EscrowStatus.PENDING,
                release_time=release_time
            )

            db.add(db_escrow)
            db.commit()
            db.refresh(db_escrow)
            
            logger.info(f"Created escrow {db_escrow.id} for product {product.id}")
            return db_escrow

        except Exception as e:
            db.rollback()
            logger.error(f"Error creating escrow: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def confirm_receipt(db: Session, escrow_id: int, buyer_id: int) -> Escrow:
        """Confirm receipt of product and release funds to seller."""
        try:
            escrow = db.query(Escrow).filter(Escrow.id == escrow_id).first()
            if not escrow:
                raise HTTPException(status_code=404, detail="Escrow not found")

            # Verify the buyer is confirming
            if escrow.buyer_id != buyer_id:
                raise HTTPException(status_code=403, detail="Only the buyer can confirm receipt")

            # Check if escrow is in valid state
            if escrow.status != EscrowStatus.PENDING:
                raise HTTPException(status_code=400, detail="Escrow is not in pending state")

            # Release the funds
            escrow.status = EscrowStatus.RELEASED
            escrow.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(escrow)
            
            logger.info(f"Released escrow {escrow_id} to seller {escrow.seller_id}")
            return escrow

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error confirming receipt: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def open_dispute(db: Session, dispute_data: DisputeCreate) -> Dispute:
        """Open a dispute for an escrow transaction."""
        try:
            # Verify escrow exists and is in valid state
            escrow = db.query(Escrow).filter(Escrow.id == dispute_data.escrow_id).first()
            if not escrow:
                raise HTTPException(status_code=404, detail="Escrow not found")
            if escrow.status != EscrowStatus.PENDING:
                raise HTTPException(status_code=400, detail="Cannot open dispute for non-pending escrow")

            # Create dispute
            db_dispute = Dispute(
                escrow_id=dispute_data.escrow_id,
                complainant_id=dispute_data.complainant_id,
                description=dispute_data.description,
                status=DisputeStatus.OPEN
            )

            db.add(db_dispute)
            db.commit()
            db.refresh(db_dispute)
            
            logger.info(f"Opened dispute {db_dispute.id} for escrow {escrow.id}")
            return db_dispute

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error opening dispute: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def resolve_dispute(
        db: Session, 
        dispute_id: int, 
        resolution_data: DisputeResolve,
        admin_id: int
    ) -> Dispute:
        """Resolve a dispute and update escrow status."""
        try:
            dispute = db.query(Dispute).filter(Dispute.id == dispute_id).first()
            if not dispute:
                raise HTTPException(status_code=404, detail="Dispute not found")

            if dispute.status == DisputeStatus.RESOLVED:
                raise HTTPException(status_code=400, detail="Dispute is already resolved")

            # Update dispute
            dispute.status = DisputeStatus.RESOLVED
            dispute.resolution = resolution_data.resolution
            dispute.updated_at = datetime.utcnow()

            # Update associated escrow
            escrow = db.query(Escrow).filter(Escrow.id == dispute.escrow_id).first()
            if escrow:
                escrow.status = resolution_data.escrow_status
                escrow.updated_at = datetime.utcnow()

            db.commit()
            db.refresh(dispute)
            
            logger.info(f"Resolved dispute {dispute_id} with status {resolution_data.escrow_status}")
            return dispute

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            logger.error(f"Error resolving dispute: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def auto_release_overdue_escrow(db: Session) -> None:
        """Release funds for escrows that have passed their release time."""
        try:
            overdue_escrows = (
                db.query(Escrow)
                .filter(
                    Escrow.status == EscrowStatus.PENDING,
                    Escrow.release_time <= datetime.utcnow()
                )
                .all()
            )

            for escrow in overdue_escrows:
                # Check if there are any open disputes
                has_open_dispute = (
                    db.query(Dispute)
                    .filter(
                        Dispute.escrow_id == escrow.id,
                        Dispute.status != DisputeStatus.RESOLVED
                    )
                    .first()
                )

                if not has_open_dispute:
                    escrow.status = EscrowStatus.RELEASED
                    escrow.updated_at = datetime.utcnow()
                    logger.info(f"Auto-released escrow {escrow.id} to seller {escrow.seller_id}")

            db.commit()

        except Exception as e:
            db.rollback()
            logger.error(f"Error in auto-release: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
