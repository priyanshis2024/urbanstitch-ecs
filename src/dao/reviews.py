from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.dto.review import ReviewCreate, ReviewUpdate
from uuid import UUID
from typing import Optional
from src.dao.models.product import Review
from sqlalchemy import func
from datetime import datetime


class review_dao:
    async def get_review_by_id(db_obj: AsyncSession, review_id: UUID):
        """
        This function gets a review details from the database by using their review id.
        :param review_id: Id of the review.
        :param db_obj: AsyncSession: Pass the database asynchronous session object to the function
        """
        result = await db_obj.execute(select(Review).where(Review.id == review_id))
        return result.scalars().first()

    async def create_review(db_obj: AsyncSession, review: ReviewCreate):
        """
        This function creates a review in the database.

        :param review: review creation request payload schema.
        :param db_obj: database object
        """
        db_obj.add(review)
        await db_obj.commit()
        await db_obj.refresh(review)
        return review

    async def update_review(
        db_obj: AsyncSession, review_db: Review, review: ReviewUpdate
    ):
        """
        This function update a review details in the database.

        :param review: review update request payload schema.
        :param review_db: review update request payload schema.
        :param db_obj: database object
        """
        review_db.updated_at = datetime.now()
        for key, value in review.dict(exclude_unset=True).items():
            setattr(review_db, key, value)
        return review_db

    async def delete_review(db_obj: AsyncSession, review: Review):
        """
        This function deletes the review details from the database.
        :param review: review payload.
        :param db_obj: database object
        """
        await db_obj.delete(review)

    async def all_review(
        db_obj: AsyncSession,
        product_id: UUID = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[str] = "asc",
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
    ):
        """
        Fetch all reviews from the database with optional filtering, sorting, and pagination.
        The all_review function is used to retrieve all the review in the database.
        It takes in a number of parameters that are used to filter and sort the results.
        :param search: Used to searching
        :param sort_order: Determine if the query should be sorted in ascending or descending order
        :param sort_by: Sort the results by a particular column
        :param limit: Limit the number of results returned
        :param offset: Skip the first n records
        :param db_obj: database object

        :return: all review by applying filter and sorting
        """

        filters = [Review.product_id == product_id] if product_id else []
        if search:
            filters.append(Review.review.ilike(f"%{search}%"))

        count_query = select(func.count()).select_from(Review)
        if filters:
            count_query = count_query.where(*filters)

        count_result = await db_obj.execute(count_query)
        total_review_count = count_result.scalar()

        query = select(Review)
        if filters:
            query = query.where(*filters)

        if sort_by:
            if sort_order == "asc":
                query = query.order_by(getattr(Review, sort_by).asc())
            elif sort_order == "desc":
                query = query.order_by(getattr(Review, sort_by).desc())

        query = query.limit(limit).offset(offset)
        result = await db_obj.execute(query)

        return {
            "total_review_count": total_review_count,
            "reviews": result.scalars().all(),
        }
