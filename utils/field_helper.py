from bson import ObjectId
from fastapi import HTTPException

from constants.common import RequestMethod
from genric.datetime_helpers import get_current_utc_datetime


def register_field_helper(
    user_id, company_id, request_data, request_type: RequestMethod
):
    """
    Helper function to set common fields for project-related requests.
    """
    if not company_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid token: Company ID is missing.",
        )
    if request_type == RequestMethod.PUT:
        if request_data.user_details:
            request_data.user_details.record_id = ObjectId(user_id)
            request_data.user_details.updated_by = ObjectId(user_id)
            request_data.user_details.updated_at = get_current_utc_datetime()
            request_data.user_details.company_id = ObjectId(company_id)
        if request_data.company_details:
            request_data.company_details.updated_by = ObjectId(user_id)
            request_data.company_details.updated_at = get_current_utc_datetime()
            request_data.company_details.record_id = ObjectId(company_id)
    return request_data


def project_field_helper(
    user_id, company_id, request_data, request_type: RequestMethod
):
    """
    Helper function to set common fields for project-related requests.
    """
    if not company_id:
        raise HTTPException(
            status_code=400,
            detail="Invalid token: Company ID is missing.",
        )
    if request_type == RequestMethod.POST:
        request_data.created_at = get_current_utc_datetime()
        request_data.updated_at = get_current_utc_datetime()
        request_data.created_by = ObjectId(user_id)
        request_data.updated_by = ObjectId(user_id)
        request_data.company_id = ObjectId(company_id)
        request_data.owner_id = ObjectId(user_id)
    if request_type == RequestMethod.PUT:
        request_data.updated_by = ObjectId(user_id)
        request_data.updated_at = get_current_utc_datetime()
        request_data.company_id = ObjectId(company_id)
    return request_data
