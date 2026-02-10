# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Payment requirements creation functions."""

from typing import Optional, Any
from x402.schemas import PaymentRequired, ResourceInfo, PaymentRequirements, Price


def create_payment_requirements(
    price: Price,
    pay_to_address: str,
    resource: str,
    network: str = "eip155:84532",
    description: str = "",
    mime_type: str = "application/json",
    scheme: str = "exact",
    max_timeout_seconds: int = 600,
    output_schema: Optional[Any] = None,
    **kwargs,
) -> PaymentRequirements:
    """Creates PaymentRequirements for A2A payment requests.

    Args:
        price: Payment price. Can be:
            - Money: USD amount as string/int (e.g., "$3.10", 0.10, "0.001") - defaults to USDC
            - TokenAmount: Custom token amount with asset information
        pay_to_address: Ethereum address to receive the payment
        resource: Resource identifier (e.g., "/generate-image")
        network: Blockchain network (default: "eip155:84532")
        description: Human-readable description
        mime_type: Expected response content type
        scheme: Payment scheme (default: "exact")
        max_timeout_seconds: Payment validity timeout
        output_schema: Response schema
        **kwargs: Additional fields passed to PaymentRequirements

    Returns:
        PaymentRequirements object ready for x402PaymentRequiredResponse
    """

    # max_amount_required, asset_address, eip712_domain = process_price_to_atomic_amount(
    #     price, network
    # )
    requirements = [
        PaymentRequirements(
            scheme=scheme,
            network=network,
            asset=price.asset, # TODO: get asset address from price data
            amount=price.amount, # TODO: extract atomic amount from price data
            pay_to=pay_to_address,
            max_timeout_seconds=max_timeout_seconds,
            **kwargs
        )
    ]
    return PaymentRequired(
        x402_version=2,
        error="Payment required",  # or None if not an error
        resource=ResourceInfo(
            url="https://mathcody.com/premium_request",
            description=description,
            mime_type=mime_type
        ),
        accepts=requirements,
        extensions=None  # Optional extensions
    )