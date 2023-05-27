\* Opportunity_/_Competition_Problem *\
Maximize
Objective_Function: - 0.15 Affordability + 0.2 Competition
 + 0.05 DiversityIndex + 0.2 FootTraffic + 0.1 Opportunity
 + 0.15 PopDensitySquareMile - 0.15 ProximityToCommercial
Subject To
test: DiversityIndex >= 0.25
Bounds
 Affordability <= 1
 Competition <= 1
 0.25 <= DiversityIndex <= 1
 FootTraffic <= 1
 Opportunity <= 1
 PopDensitySquareMile <= 1
 0.01 <= ProximityToCommercial <= 1
End
