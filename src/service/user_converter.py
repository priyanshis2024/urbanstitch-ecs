from src.dao.models.user import UserRole, User
from src.dto.user_role import UserRoleCreate, UserRoleResponse, UserRoleUpdate
from src.dao.models.user import User, UserRole, ContactUs, CustomerDetails
from src.dto.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserUpdateStatus,
    UserListResponse,
    UserCreationResponse,
)
from src.dto.contact_us import ContactUsCreate, ContactUsUpdate, ContactUsResponse
from src.dto.customer_details import (
    CustomerDetailCreate,
    CustomerDetailUpdate,
    CustomerDetailResponse,
    CustomerDetailListResponse,
)
from fastapi.encoders import jsonable_encoder


class Converter:
    def user_role_db_to_dto(user_role_response: UserRoleResponse):
        """
        Convert a User role database model to a UserRoleResponse DTO.
        :param user_role: User role database model
        :return: UserRoleResponse DTO
        """
        user_role_dict = jsonable_encoder(user_role_response)
        return UserRoleResponse(**user_role_dict)

    def user_role_create_dto_to_db(user_role_create: UserRoleCreate):
        """
        Convert a UserRoleCreate DTO to a User Role database model.
        :param user_role_create: UserRoleCreate DTO
        :return: User role database model
        """
        return UserRole(id=user_role_create.id, role=user_role_create.role)

    def user_role_update_dto_to_db(
        user_role_update: UserRoleUpdate, user_role: UserRole
    ):
        """
        Convert a UserRoleUpdate DTO to a User role database model (updating an existing user role).
        :param user_role_update: UserRoleUpdate DTO
        :param user_role: Existing User role database model
        :return: Updated User role database model
        """
        for key, value in user_role_update.model_dump(exclude_unset=True).items():
            setattr(user_role, key, value)
        return user_role

    def user_creation_response_db_to_dto(
        user: UserCreationResponse, is_user_created: bool
    ):
        """
        Convert a User database model to a UserCreationResponse DTO.
        :param user: User database model
        :return: UserCreationResponse DTO
        """
        user_dict = jsonable_encoder(user)
        user_dict["is_user_created"] = is_user_created
        return UserCreationResponse(**user_dict)

    def user_db_to_dto(user: UserResponse):
        """
        Convert a User database model to a UserResponse DTO.
        :param user: User database model
        :return: UserResponse DTO
        """
        user_dict = jsonable_encoder(user)
        return UserResponse(**user_dict)

    def user_create_dto_to_db(user_create: UserCreate):
        """
        Convert a UserCreate DTO to a User database model.
        :param user_create: UserCreate DTO
        :return: User database model
        """
        return User(
            id=user_create.id,
            user_role_id=user_create.user_role_id,
            contact=user_create.contact,
            email=user_create.email,
            password=user_create.password,
            username=user_create.username,
            image=user_create.image,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            gender=user_create.gender,
            dob=user_create.dob,
            status=user_create.status,
        )

    def user_update_dto_to_db(user_update: UserUpdate, user: User):
        """
        Convert a UserUpdate DTO to a User database model (updating an existing user).
        :param user_update: UserUpdate DTO
        :param user: Existing User database model
        :return: Updated User database model
        """
        for key, value in user_update.model_dump(exclude_unset=True).items():
            setattr(user, key, value)
        return user

    def user_response_db_to_dto(user_response: UserListResponse):
        """
        Convert a User database model to a UserResponse DTO.
        :param user_response: User database model
        :return: UserResponse DTO
        """
        return UserListResponse(
            total_user_count=len(user_response["users"]),
            users=[Converter.user_db_to_dto(user) for user in user_response["users"]],
        )

    def user_update_status_dto_to_db(user_update_status: UserUpdateStatus, user: User):
        """
        Convert a UserUpdateStatus DTO to a User database model (updating only the status).
        :param user_update_status: UserUpdateStatus DTO
        :param user: Existing User database model
        :return: Updated User database model
        """
        user.status = user_update_status.status
        return user

    def contact_us_db_to_dto(contact_us_response: ContactUsResponse):
        """
        Convert a contact us database model to a ContactUsResponse DTO.
        :param contact_us_response: ContactUsResponse database model
        :return: ContactUsResponse DTO
        """
        contact_us_dict = jsonable_encoder(contact_us_response)
        return ContactUsResponse(**contact_us_dict)

    def contact_us_create_dto_to_db(contact_us_create: ContactUsCreate):
        """
        Convert a ContactUsCreate DTO to a contact us database model.
        :param contact_us_create: ContactUsCreate DTO
        :return: contact us database model
        """
        return ContactUs(
            user_id=contact_us_create.user_id, message=contact_us_create.message
        )

    def contact_us_update_dto_to_db(
        contact_us_update: ContactUsUpdate, contact_us: ContactUs
    ):
        """
        Convert a ContactUsUpdate DTO to a Contact us database model (updating an existing contact us).
        :param contact_us_update: ContactUsUpdate DTO
        :param contact_us: Existing ContactUs database model
        :return: Updated Contact us database model
        """
        for key, value in contact_us_update.model_dump(exclude_unset=True).items():
            setattr(contact_us, key, value)
        return contact_us

    def customer_detail_db_to_dto(customer_detail_response: CustomerDetailResponse):
        """
        Convert a customer_detail database model to a CustomerDetailResponse DTO.
        :param customer_detail_response: CustomerDetailResponse database model
        :return: CustomerDetailResponse DTO
        """
        customer_detail_dict = jsonable_encoder(customer_detail_response)
        return CustomerDetailResponse(**customer_detail_dict)

    def customer_detail_create_dto_to_db(customer_detail_create: CustomerDetailCreate):
        """
        Convert a CustomerDetailCreate DTO to a customer_detail database model.
        :param customer_detail_create: CustomerDetailCreate DTO
        :return: customer_detail database model
        """
        return CustomerDetails(
            address_type=customer_detail_create.address_type,
            address=customer_detail_create.address,
            landmark=customer_detail_create.landmark,
            city=customer_detail_create.city,
            state=customer_detail_create.state,
            country=customer_detail_create.country,
            pincode=customer_detail_create.pincode,
            contact=customer_detail_create.contact,
            email=customer_detail_create.email,
            first_name=customer_detail_create.first_name,
            last_name=customer_detail_create.last_name,
        )

    def customer_detail_update_dto_to_db(
        customer_detail_update: CustomerDetailUpdate, customer_detail: CustomerDetails
    ):
        """
        Convert a CustomerDetailUpdate DTO to a User role database model (updating an existing user role).
        :param customer_detail_update: CustomerDetailUpdate DTO
        :param customer_detail: Existing customer_detail database model
        :return: Updated User role database model
        """
        for key, value in customer_detail_update.model_dump(exclude_unset=True).items():
            setattr(customer_detail, key, value)
        return customer_detail

    def customers_details_summary_db_to_dto(customer_response: list):
        """
        Convert a customers_details database model to a CustomerDetailResponse DTO.
        """
        total_customer_details_count = len(customer_response)
        customer_details = [
            Converter.customer_detail_db_to_dto(customer)
            for customer in customer_response
        ]
        return CustomerDetailListResponse(
            total_customer_details_count=total_customer_details_count,
            customer_details=customer_details,
        )
