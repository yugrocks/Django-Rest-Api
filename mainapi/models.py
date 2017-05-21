from django.db import models

#The Object oriented database model, which is converted automatically
#to the sql based RDBMS model.
#Questions class corersponds to a record of the Questions table.
#Where Question, Option_A.......Corrct_Option are the columns.

class Questions(models.Model): 
    Question=models.CharField(max_length=500)
    Option_A=models.CharField(max_length=200)
    Option_B=models.CharField(max_length=200)
    Option_C=models.CharField(max_length=200)
    Option_D=models.CharField(max_length=200)
    Correct_Option=models.CharField(max_length=200)
