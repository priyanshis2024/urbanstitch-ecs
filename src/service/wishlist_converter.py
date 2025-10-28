from src.dto.wishlist import (
    WishlistCreate,
    WishlistDetailResponse,
    WishlistListDetailResponse,
)
from src.dao.models.product import Wishlist


class Converter:
    def wishlist_create_dto_to_db(wishlist_create: WishlistCreate):
        """
        Convert a WishlistCreate DTO to a wishlist database model.
        :param wishlist_create: WishlistCreate DTO
        :return: wishlist database model
        """
        return Wishlist(subproduct_id=wishlist_create.subproduct_id)

    def wishlist_detail_dto_to_db(wishlist: Wishlist):
        """
        Convert a Wishlist to WishlistDetailResponse DTO.
        """
        subproduct = wishlist.subproducts
        product = subproduct.products

        return WishlistDetailResponse(
            id=wishlist.id,
            subproduct_id=subproduct.id,
            name=product.name,
            description=product.description,
            price=subproduct.price,
            rating=product.rating,
            images=(
                subproduct.images.split(",")
                if isinstance(subproduct.images, str)
                else subproduct.images
            ),
        )

    def wishlist_detail_list_response_db_to_dto(wishlist_data):
        """
        Convert wishlist query response to DTO.
        """
        return WishlistListDetailResponse(
            total_wishlist_product_count=wishlist_data["total_wishlist_product_count"],
            wishlist_products=[
                Converter.wishlist_detail_dto_to_db(wishlist)
                for wishlist in wishlist_data["wishlist_products"]
            ],
        )
