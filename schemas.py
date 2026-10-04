from pydantic import BaseModel, Field
from typing import Optional, List


class OrderInfo(BaseModel):
    order_id: str = Field(
        description="The unique order ID"
    )

    product: str = Field(
        description="The product name"
    )

    status: str = Field(
        description="Current order status"
    )

    tracking_number: Optional[str] = Field(
        default=None,
        description="Tracking number if available"
    )

    delivery_date: Optional[str] = Field(
        default=None,
        description="Expected or actual delivery date if available"
    )

    refund_eligible: Optional[bool] = Field(
        default=None,
        description="Whether the order is currently eligible for a refund"
    )

    refund_amount: Optional[float] = Field(
        default=None,
        description="Refund amount if the order is eligible"
    )

    refund_reason: Optional[str] = Field(
        default=None,
        description="Reason explaining refund eligibility or ineligibility"
    )


class CustomerSupportResponse(BaseModel):
    intent: str = Field(
        description="The main intent of the customer's request"
    )

    message: str = Field(
        description="A concise natural-language response to the customer"
    )

    orders: List[OrderInfo] = Field(
        default_factory=list,
        description="Orders relevant to the customer's request"
    )