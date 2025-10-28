from src.dto.size import SizeCreate, SizeUpdate, SizeResponse, SizeListResponse
from src.dao.models.product import Size
from fastapi.encoders import jsonable_encoder


class Converter:
    def size_db_to_dto(size_response: SizeResponse):
        """
        Convert a size database model to a SizeResponse DTO.
        :param size_response: SizeResponse database model
        :return: SizeResponse DTO
        """
        size_dict = jsonable_encoder(size_response)
        return SizeResponse(**size_dict)

    def size_response_db_to_dto(size_response: SizeListResponse):
        """
        Convert a size database model to a SizeListResponse DTO.
        :param size_response: Size database model
        :return: SizeListResponse DTO
        """
        return SizeListResponse(
            total_size_count=len(size_response["sizes"]),
            sizes=[Converter.size_db_to_dto(size) for size in size_response["sizes"]],
        )

    def size_create_dto_to_db(size_create: SizeCreate):
        """
        Convert a SizeCreate DTO to a size database model.
        :param size_create: SizeCreate DTO
        :return: size database model
        """
        return Size(id=size_create.id, size=size_create.size, data=size_create.data)

    def size_update_dto_to_db(size_update: SizeUpdate, size: Size):
        """
        Convert a SizeUpdate DTO to a Size database model (updating an existing Size).
        :param size_update: SizeUpdate DTO
        :param size: Existing size database model
        :return: Updated Size database model
        """
        for key, value in size_update.model_dump(exclude_unset=True).items():
            setattr(size, key, value)
        return size
