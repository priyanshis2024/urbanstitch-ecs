from src.dto.color import ColorResponse


class Converter:
    def color_db_to_dto(color_response):
        return ColorResponse(color=color_response)
