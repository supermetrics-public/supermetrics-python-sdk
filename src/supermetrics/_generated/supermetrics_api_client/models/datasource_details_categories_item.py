from typing import Literal, cast

DatasourceDetailsCategoriesItem = Literal[
    "Ad Verification",
    "Affiliate",
    "Analytics",
    "Brand Reputation",
    "CRM/Sales",
    "Data Warehouses",
    "DSP",
    "Ecommerce",
    "Files",
    "Marketing Attribution",
    "Marketing Automation",
    "Mobile",
    "Other",
    "Paid Media",
    "Payments",
    "Retail Media",
    "Search",
    "SEO",
    "Social Media",
]

DATASOURCE_DETAILS_CATEGORIES_ITEM_VALUES: set[DatasourceDetailsCategoriesItem] = {
    "Ad Verification",
    "Affiliate",
    "Analytics",
    "Brand Reputation",
    "CRM/Sales",
    "Data Warehouses",
    "DSP",
    "Ecommerce",
    "Files",
    "Marketing Attribution",
    "Marketing Automation",
    "Mobile",
    "Other",
    "Paid Media",
    "Payments",
    "Retail Media",
    "Search",
    "SEO",
    "Social Media",
}


def check_datasource_details_categories_item(value: str) -> DatasourceDetailsCategoriesItem:
    if value in DATASOURCE_DETAILS_CATEGORIES_ITEM_VALUES:
        return cast(DatasourceDetailsCategoriesItem, value)
    raise TypeError(f"Unexpected value {value!r}. Expected one of {DATASOURCE_DETAILS_CATEGORIES_ITEM_VALUES!r}")
