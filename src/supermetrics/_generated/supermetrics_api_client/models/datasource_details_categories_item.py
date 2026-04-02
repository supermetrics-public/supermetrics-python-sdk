from enum import Enum


class DatasourceDetailsCategoriesItem(str, Enum):
    AD_VERIFICATION = "Ad Verification"
    AFFILIATE = "Affiliate"
    ANALYTICS = "Analytics"
    BRAND_REPUTATION = "Brand Reputation"
    CRM_SALES = "CRM/Sales"
    DATA_WAREHOUSES = "Data Warehouses"
    DSP = "DSP"
    ECOMMERCE = "Ecommerce"
    FILES = "Files"
    MARKETING_ATTRIBUTION = "Marketing Attribution"
    MARKETING_AUTOMATION = "Marketing Automation"
    MOBILE = "Mobile"
    OTHER = "Other"
    PAID_MEDIA = "Paid Media"
    PAYMENTS = "Payments"
    RETAIL_MEDIA = "Retail Media"
    SEARCH = "Search"
    SEO = "SEO"
    SOCIAL_MEDIA = "Social Media"

    def __str__(self) -> str:
        return str(self.value)
