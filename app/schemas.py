from pydantic import BaseModel

class PredictionInput(BaseModel):
    Age: int
    Gender: int
    AnnualIncome: float
    NumberOfPurchases: int
    ProductCategory: int
    TimeSpentOnWebsite: float
    LoyaltyProgram: int
    DiscountsAvailed: int

class PredictionOutput(BaseModel):
    prediction: int