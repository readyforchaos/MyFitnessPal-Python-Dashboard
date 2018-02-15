# -*- coding: utf-8 -*-

# Made by Anders Gill

from PyQt5 import QtCore, QtGui, QtWidgets
import time
import datetime
from datetime import timedelta
import myfitnesspal

# chart imports
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QGridLayout
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import random

# button imports
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import subprocess

myfitnesspal.keyring_utils.store_password_in_keyring("USERNAME", "PASSWORD")
localclient = myfitnesspal.Client("USERNAME")
client = localclient


# Globals
now = datetime.datetime.now()
day = client.get_date(now.year, now.month, now.day)
remaining = 0
goal = 0
food = 0
breakfastConsumed = 0
breakfastGoal = 0
lunchConsumed = 0
lunchGoal = 0
dinnerConsumed = 0
dinnerGoal = 0
snacksConsumed = 0
snacksGoal = 0

# Nutrition
carbohydratesConsumed = 0
carbohydratesGoal = 400
fatConsumed = 0
fatGoal = 71
proteinConsumed = 0
proteinGoal = 240
sodiumConsumed = 0
sodiumGoal = 2300
sugarConsumed = 0
sugarGoal = 98

# Current routine selection
# 0 = shred, 1 = lean, 2 = bulk
mealGoals = 1

# Shred/Cut Meal Goals
shredBreakfastGoal = 400
shredLunchGoal = 600
shredDinnerGoal = 800
shredSnacksGoal = 100

# Lean Mass Meal Goals
leanBreakfastGoal = 800
leanLunchGoal = 960
leanDinnerGoal = 1120
leanSnacksGoal = 320

# Bulk Meal Goals
bulkBreakfastGoal = 1000
bulkLunchGoal = 1100
bulkDinnerGoal = 1500
bulkSnacksGoal = 500

def _getRoutineSelectionGoals():
    print("inside _getRoutineSelectionGoals method")
    global mealGoals
    global breakfastGoal
    global lunchGoal
    global dinnerGoal
    global snacksGoal
    
    #routine globals
    global shredBreakfastGoal
    global shredLunchGoal
    global shredDinnerGoal
    global shredSnacksGoal
    global leanBreakfastGoal
    global leanLunchGoal
    global leanDinnerGoal
    global leanSnacksGoal
    global bulkBreakfastGoal
    global bulkLunchGoal
    global bulkDinnerGoal
    global bulkSnacksGoal
    
    if mealGoals == 0:
        breakfastGoal = shredBreakfastGoal
        lunchGoal = shredLunchGoal
        dinnerGoal = shredDinnerGoal
        snacksGoal = shredSnacksGoal
    elif mealGoals == 1:
        breakfastGoal = leanBreakfastGoal
        lunchGoal = leanLunchGoal
        dinnerGoal = leanDinnerGoal
        snacksGoal = leanSnacksGoal   
    elif mealGoals == 2:
        breakfastGoal = bulkBreakfastGoal
        lunchGoal = bulkLunchGoal
        dinnerGoal = bulkDinnerGoal
        snacksGoal = bulkSnacksGoal
        

def _calculateRemainingCal():
    print("inside _calculateRemainingCal method")
    if bool(day.totals) == False:
        localremaining = day.goals["calories"]
    else:
        localremaining = abs(day.totals["calories"] - day.goals["calories"])       
    global remaining
    remaining = localremaining
    
def _calculateFoodCal():
    print("inside _calculateFoodCal method")    
    if bool(day.totals) == False:
        localfood = 0
    else:
        localfood = abs(day.totals["calories"])
    global food
    food = localfood

def _calculateGoalCal():
    print("inside _calculateGoalCal method")
    localfood = abs(day.goals["calories"])
    global goal
    goal = localfood
    
    
def _getMealsConsumed():
    # Breakfast
    if bool(day.meals[0].totals) == False:
        localBreakfastConsumed = 0
    else:
        localBreakfastConsumed = day.meals[0].totals["calories"]
    global breakfastConsumed
    breakfastConsumed = localBreakfastConsumed
    
    #Lunch
    if bool(day.meals[1].totals) == False:
        localLunchConsumed = 0
    else:
        localLunchConsumed = day.meals[1].totals["calories"]
    global lunchConsumed
    lunchConsumed = localLunchConsumed
    
    #Dinner
    if bool(day.meals[2].totals) == False:
        localDinnerConsumed = 0
    else:
        localDinnerConsumed = day.meals[2].totals["calories"]
    global dinnerConsumed
    dinnerConsumed = localDinnerConsumed
    
    #Snacks
    if bool(day.meals[3].totals) == False:
        localSnacksConsumed = 0
    else:
        localSnacksConsumed = day.meals[3].totals["calories"]
    global snacksConsumed
    snacksConsumed = localSnacksConsumed

    
def _getNutritionConsumed():
    #Carbohydrates
    global carbohydratesConsumed
    if bool(day.totals) == False:
        carbohydratesConsumed = 0
    else:
        carbohydratesConsumed = day.totals["carbohydrates"]
        
    #fat
    global fatConsumed
    if bool(day.totals) == False:
        fatConsumed = 0
    else:
        fatConsumed = day.totals["fat"]
        
    #protein
    global proteinConsumed
    if bool(day.totals) == False:
        proteinConsumed = 0
    else:
        proteinConsumed = day.totals["protein"]
        
    #sodium
    global sodiumConsumed
    if bool(day.totals) == False:
        sodiumConsumed = 0
    else:
        sodiumConsumed = day.totals["sodium"]
        
    #sugar
    global sugarConsumed
    if bool(day.totals) == False:
        sugarConsumed = 0
    else:
        sugarConsumed = day.totals["sugar"]
        
                
def _getNutritionProgressConsumed(**nutrition):
    if nutrition["nutrition"] == 'carbohydrates':
        global carbohydratesConsumed
        if bool(day.totals) == False:
            carbohydratesConsumed = 0
            return 0
        else:
            carbohydratesPercentage = abs(day.totals["carbohydrates"]/carbohydratesGoal*100)
            if carbohydratesConsumed >= carbohydratesGoal:
                return 100
            else:
                return carbohydratesPercentage
            
    elif nutrition["nutrition"] == 'fat':
            global fatConsumed
            if bool(day.totals) == False:
                fatConsumed = 0
                return 0
            else:
                fatPercentage = abs(day.totals["fat"]/fatGoal*100)
                if fatConsumed >= fatGoal:
                    return 100
                else:
                    return fatPercentage

    elif nutrition["nutrition"] == 'protein':
            global proteinConsumed
            if bool(day.totals) == False:
                proteinConsumed = 0
                return 0
            else:
                proteinPercentage = abs(day.totals["protein"]/proteinGoal*100)
                if proteinConsumed >= proteinGoal:
                    return 100
                else:
                    return proteinPercentage

    elif nutrition["nutrition"] == 'sodium':
            global sodiumConsumed
            if bool(day.totals) == False:
                sodiumConsumed = 0
                return 0
            else:
                sodiumPercentage = abs(day.totals["sodium"]/sodiumGoal*100)
                if sodiumConsumed >= sodiumGoal:
                    return 100
                else:
                    return sodiumPercentage

    elif nutrition["nutrition"] == 'sugar':
            global sugarConsumed
            if bool(day.totals) == False:
                sugarConsumed = 0
                return 0
            else:
                sugarPercentage = abs(day.totals["sugar"]/sugarGoal*100)
                if sugarConsumed >= sugarGoal:
                    return 100
                else:
                    return sugarPercentage

                
def _getMealsProgressConsumed(**meals):
    if meals["meals"] == 'breakfast':                
        if bool(day.meals[0].totals) == False:
            localBreakfastConsumed = 0
            return 0
        else:
            localBreakfastConsumed = abs(breakfastConsumed/breakfastGoal*100)
            if breakfastConsumed >= breakfastGoal:
                return 100
            else:
                return localBreakfastConsumed

    if meals["meals"] == 'lunch':                
        if bool(day.meals[1].totals) == False:
            localLunchConsumed = 0
            return 0
        else:
            localLunchConsumed = abs(lunchConsumed/lunchGoal*100)
            if lunchConsumed >= lunchGoal:
                return 100
            else:
                return localLunchConsumed

    if meals["meals"] == 'dinner':                
        if bool(day.meals[2].totals) == False:
            localDinnerConsumed = 0
            return 0
        else:
            localDinnerConsumed = abs(dinnerConsumed/dinnerGoal*100)
            if dinnerConsumed >= dinnerGoal:
                return 100
            else:
                return localDinnerConsumed

    if meals["meals"] == 'snacks':                
        if bool(day.meals[3].totals) == False:
            localSnacksConsumed = 0
            return 0
        else:
            localSnacksConsumed = abs(snacksConsumed/snacksGoal*100)
            if snacksConsumed >= snacksGoal:
                return 100
            else:
                return localSnacksConsumed        
    

class MplWaterCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8.3, height=4.8, dpi=96):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    
    def compute_initial_figure(self):
        pass

class MplWeightCanvas(FigureCanvas):
    def __init__(self, parent=None, width=8.3, height=4.8, dpi=96):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
    
    def compute_initial_figure(self):
        pass

class WaterCanvas(MplWaterCanvas):
    def compute_initial_figure(self):
        Y = []
        X = []
        for element in range(0, 7):      
            d = datetime.datetime.now() - timedelta(days=element)
            day = str(d.year) + ", " + str(d.month) + ", " + str(d.day)
            clientDay = client.get_date(d.year, d.month, d.day)
            Y.append(clientDay.water)
        
        for item in range(0, 7):         
            d = datetime.datetime.now() - timedelta(days=item)
            X.append(d.strftime("%d-%m-%Y")) 
            
        for a,b in zip(X, Y):
            self.axes.text(a, b, str(b/1000), fontsize=20, bbox=dict(facecolor='red', alpha=0.5))
            
        y = Y
        x = X
        self.axes.plot(x, y) 
    
class WeightCanvas(MplWeightCanvas):
    def compute_initial_figure(self):
        Y = []
        X = []
        
        weightIndex = {k:i for i,k in enumerate(client.get_measurements('Weight').values())}
        for key in weightIndex:
            Y.append(key)
        
        for item in range(0,len(Y)):         
            d = datetime.datetime.now() - timedelta(days=item)
            X.append(d.strftime("%d-%m-%Y"))
            
        for a,b in zip(X, Y):
            self.axes.text(a, b, str(b), fontsize=20, bbox=dict(facecolor='red', alpha=0.5))
        
        y = Y
        x = X    
        self.axes.plot(x, y)
 
class Ui_Applikasjon(object):        
    def setupUi(self, Application):
        Application.setObjectName("Application")
        Application.resize(800, 480)
#       Application.setMaximumSize(QtCore.QSize(800, 480))
#       Application.setWindowState(QtCore.Qt.WindowMaximized)
#       Application.showFullScreen()
        self.Frame = QtWidgets.QFrame(Application)
        self.Frame.setGeometry(QtCore.QRect(0, 0, 1061, 1661))
        self.Frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Frame.setObjectName("Frame")
        
        self.Tabs = QtWidgets.QTabWidget(self.Frame)
        self.Tabs.setGeometry(QtCore.QRect(0, 0, 800, 1701))
        self.Tabs.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.Tabs.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.Tabs.setTabPosition(QtWidgets.QTabWidget.North)
        self.Tabs.setObjectName("Tabs")
        
        self.Today = QtWidgets.QWidget()
        self.Today.setObjectName("Today")
        
        self.Goal = QtWidgets.QLabel(self.Today)
        self.Goal.setGeometry(QtCore.QRect(30, 70, 103, 29))
        self.Goal.setAlignment(QtCore.Qt.AlignCenter)
        self.Goal.setObjectName("Goal")
        
        self.Food = QtWidgets.QLabel(self.Today)
        self.Food.setGeometry(QtCore.QRect(240, 70, 103, 29))
        self.Food.setAlignment(QtCore.Qt.AlignCenter)
        self.Food.setObjectName("Food")
        
        self.RemainingCalories = QtWidgets.QLabel(self.Today)
        self.RemainingCalories.setGeometry(QtCore.QRect(522, 70, 251, 29))
        self.RemainingCalories.setAlignment(QtCore.Qt.AlignCenter)
        self.RemainingCalories.setObjectName("RemainingCalories")
        
        self.line = QtWidgets.QFrame(self.Today)
        self.line.setGeometry(QtCore.QRect(27, 110, 741, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        
        self.lcdNumberGoal = QtWidgets.QLCDNumber(self.Today)
        self.lcdNumberGoal.setGeometry(QtCore.QRect(11, 20, 84, 47))
        self.lcdNumberGoal.setBaseSize(QtCore.QSize(0, 0))
        
        font = QtGui.QFont()
        font.setPointSize(10)
        
        self.lcdNumberGoal.setFont(font)
        self.lcdNumberGoal.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumberGoal.setAutoFillBackground(False)
        self.lcdNumberGoal.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumberGoal.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdNumberGoal.setLineWidth(0)
        self.lcdNumberGoal.setSmallDecimalPoint(False)
        self.lcdNumberGoal.setDigitCount(4)
        self.lcdNumberGoal.setProperty("value", goal)
        self.lcdNumberGoal.setObjectName("lcdNumberGoal")
        self.lcdNumberFood = QtWidgets.QLCDNumber(self.Today)
        self.lcdNumberFood.setGeometry(QtCore.QRect(220, 20, 84, 47))
        self.lcdNumberFood.setBaseSize(QtCore.QSize(0, 0))
        
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        
        self.lcdNumberFood.setFont(font)
        self.lcdNumberFood.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumberFood.setAutoFillBackground(False)
        self.lcdNumberFood.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumberFood.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdNumberFood.setLineWidth(0)
        self.lcdNumberFood.setSmallDecimalPoint(False)
        self.lcdNumberFood.setDigitCount(4)
        self.lcdNumberFood.setProperty("value", food)
        self.lcdNumberFood.setObjectName("lcdNumberFood")
        
        self.minus = QtWidgets.QLabel(self.Today)
        self.minus.setGeometry(QtCore.QRect(158, 18, 63, 61))
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.minus.sizePolicy().hasHeightForWidth())
        
        self.minus.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setUnderline(False)
        
        self.minus.setFont(font)
        self.minus.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.minus.setObjectName("minus")
        
        self.equal = QtWidgets.QLabel(self.Today)
        self.equal.setGeometry(QtCore.QRect(460, 20, 63, 61))
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.equal.sizePolicy().hasHeightForWidth())
        
        self.equal.setSizePolicy(sizePolicy)
        
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setUnderline(False)
        
        self.equal.setFont(font)
        self.equal.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.equal.setObjectName("equal")
        
        self.lcdNumberRemaining = QtWidgets.QLCDNumber(self.Today)
        self.lcdNumberRemaining.setGeometry(QtCore.QRect(561, 23, 176, 47))
        self.lcdNumberRemaining.setBaseSize(QtCore.QSize(0, 0))
        
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(25, 200, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        
        self.lcdNumberRemaining.setPalette(palette)
        
        font = QtGui.QFont()
        font.setPointSize(10)
        
        self.lcdNumberRemaining.setFont(font)
        self.lcdNumberRemaining.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumberRemaining.setAutoFillBackground(False)
        self.lcdNumberRemaining.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lcdNumberRemaining.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdNumberRemaining.setLineWidth(0)
        self.lcdNumberRemaining.setSmallDecimalPoint(False)
        self.lcdNumberRemaining.setDigitCount(4)
        
        
        # Set Calories remaining LCD
         
        self.lcdNumberRemaining.setProperty("value", remaining)
        self.lcdNumberRemaining.setObjectName("lcdNumberRemaining")
        
        
        self.Breakfast = QtWidgets.QLabel(self.Today)
        self.Breakfast.setGeometry(QtCore.QRect(30, 130, 111, 31))
        self.Breakfast.setObjectName("Breakfast")
        
        self.line_2 = QtWidgets.QFrame(self.Today)
        self.line_2.setGeometry(QtCore.QRect(30, 190, 741, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        
        self.progressBarBreakfast = QtWidgets.QProgressBar(self.Today)
        self.progressBarBreakfast.setGeometry(QtCore.QRect(180, 140, 591, 31))
        self.progressBarBreakfast.setProperty("value", _getMealsProgressConsumed(meals="breakfast"))
        self.progressBarBreakfast.setObjectName("progressBarBreakfast")
        
        self.BreakfastCalConsumed = QtWidgets.QLabel(self.Today)
        self.BreakfastCalConsumed.setGeometry(QtCore.QRect(30, 160, 61, 31))
        self.BreakfastCalConsumed.setObjectName("BreakfastCalConsumed")
        
        self.BreakfastCalGoal = QtWidgets.QLabel(self.Today)
        self.BreakfastCalGoal.setGeometry(QtCore.QRect(110, 160, 61, 31))
        self.BreakfastCalGoal.setObjectName("BreakfastCalGoal")
        
        self.slash_1 = QtWidgets.QLabel(self.Today)
        self.slash_1.setGeometry(QtCore.QRect(90, 160, 21, 31))
        self.slash_1.setObjectName("slash_1")
        
        self.LunchCaloriesConsumed = QtWidgets.QLabel(self.Today)
        self.LunchCaloriesConsumed.setGeometry(QtCore.QRect(30, 230, 61, 31))
        self.LunchCaloriesConsumed.setObjectName("LunchCaloriesConsumed")
        
        self.progressBarLunch = QtWidgets.QProgressBar(self.Today)
        self.progressBarLunch.setGeometry(QtCore.QRect(180, 210, 591, 31))
        self.progressBarLunch.setProperty("value", _getMealsProgressConsumed(meals="lunch"))
        self.progressBarLunch.setObjectName("progressBarLunch")
        
        self.slash_2 = QtWidgets.QLabel(self.Today)
        self.slash_2.setGeometry(QtCore.QRect(90, 230, 21, 31))
        self.slash_2.setObjectName("slash_2")
        
        self.Lunch = QtWidgets.QLabel(self.Today)
        self.Lunch.setGeometry(QtCore.QRect(30, 200, 111, 31))
        self.Lunch.setObjectName("Lunch")
        
        self.LunchCaloriesGoal = QtWidgets.QLabel(self.Today)
        self.LunchCaloriesGoal.setGeometry(QtCore.QRect(110, 230, 61, 31))
        self.LunchCaloriesGoal.setObjectName("LunchCaloriesGoal")
        
        self.line_3 = QtWidgets.QFrame(self.Today)
        self.line_3.setGeometry(QtCore.QRect(30, 260, 741, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        
        self.slash_3 = QtWidgets.QLabel(self.Today)
        self.slash_3.setGeometry(QtCore.QRect(90, 300, 21, 31))
        self.slash_3.setObjectName("slash_3")
        
        self.DinnerCaloriesGoal = QtWidgets.QLabel(self.Today)
        self.DinnerCaloriesGoal.setGeometry(QtCore.QRect(110, 300, 61, 31))
        self.DinnerCaloriesGoal.setObjectName("DinnerCaloriesGoal")
        
        self.Dinner = QtWidgets.QLabel(self.Today)
        self.Dinner.setGeometry(QtCore.QRect(30, 270, 111, 31))
        self.Dinner.setObjectName("Dinner")
        
        self.line_4 = QtWidgets.QFrame(self.Today)
        self.line_4.setGeometry(QtCore.QRect(30, 330, 741, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        
        self.progressBarDinner = QtWidgets.QProgressBar(self.Today)
        self.progressBarDinner.setGeometry(QtCore.QRect(180, 280, 591, 31))
        self.progressBarDinner.setProperty("value", _getMealsProgressConsumed(meals="dinner"))
        self.progressBarDinner.setObjectName("progressBarDinner")
        
        self.DinnerCaloriesConsumed = QtWidgets.QLabel(self.Today)
        self.DinnerCaloriesConsumed.setGeometry(QtCore.QRect(30, 300, 61, 31))
        self.DinnerCaloriesConsumed.setObjectName("DinnerCaloriesConsumed")
        
        self.SnacksCaloriesGoal = QtWidgets.QLabel(self.Today)
        self.SnacksCaloriesGoal.setGeometry(QtCore.QRect(110, 380, 61, 31))
        self.SnacksCaloriesGoal.setObjectName("SnacksCaloriesGoal")
        
        self.slash_4 = QtWidgets.QLabel(self.Today)
        self.slash_4.setGeometry(QtCore.QRect(90, 380, 21, 31))
        self.slash_4.setObjectName("slash_4")
        
        self.progressBarSnacks = QtWidgets.QProgressBar(self.Today)
        self.progressBarSnacks.setGeometry(QtCore.QRect(180, 360, 591, 31))
        self.progressBarSnacks.setProperty("value", _getMealsProgressConsumed(meals="snacks"))
        self.progressBarSnacks.setObjectName("progressBarSnacks")
        
        self.SnacksCaloriesConsumed = QtWidgets.QLabel(self.Today)
        self.SnacksCaloriesConsumed.setGeometry(QtCore.QRect(30, 380, 61, 31))
        self.SnacksCaloriesConsumed.setObjectName("SnacksCaloriesConsumed")
        
        self.Snacks = QtWidgets.QLabel(self.Today)
        self.Snacks.setGeometry(QtCore.QRect(30, 350, 111, 31))
        self.Snacks.setObjectName("Snacks")
        
        self.Tabs.addTab(self.Today, "")
        
        self.NutritionToday = QtWidgets.QWidget()
        self.NutritionToday.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.NutritionToday.setObjectName("NutritionToday")
        
        self.scrollArea = QtWidgets.QScrollArea(self.NutritionToday)
        self.scrollArea.setGeometry(QtCore.QRect(10, 10, 791, 480))
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scrollArea.setLineWidth(0)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.scrollArea.setObjectName("scrollArea")
        
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 753, 480))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 480))
        self.scrollAreaWidgetContents.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        
        self.progressBarProteins = QtWidgets.QProgressBar(self.scrollAreaWidgetContents)
        self.progressBarProteins.setGeometry(QtCore.QRect(160, 20, 591, 31))
        self.progressBarProteins.setProperty("value", _getNutritionProgressConsumed(nutrition="protein"))
        self.progressBarProteins.setObjectName("progressBarProteins")
        
        self.line_5 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_5.setGeometry(QtCore.QRect(10, 70, 741, 20))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_7 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_7.setGeometry(QtCore.QRect(10, 210, 741, 20))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        
        self.SugarConsumed = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.SugarConsumed.setGeometry(QtCore.QRect(10, 250, 61, 31))
        self.SugarConsumed.setObjectName("SugarConsumed")
        
        self.Proteins = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.Proteins.setGeometry(QtCore.QRect(10, 10, 111, 31))
        self.Proteins.setObjectName("Proteins")
        
    
        
        self.line_8 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_8.setGeometry(QtCore.QRect(10, 280, 741, 20))
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        
        self.Fats = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.Fats.setGeometry(QtCore.QRect(10, 150, 111, 31))
        self.Fats.setObjectName("Fats")
        
        self.FatsGoal = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.FatsGoal.setGeometry(QtCore.QRect(90, 180, 61, 31))
        self.FatsGoal.setObjectName("FatsGoal")
        
        self.slash_7 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.slash_7.setGeometry(QtCore.QRect(70, 180, 21, 31))
        self.slash_7.setObjectName("slash_7")
        
        self.CarbsGoal = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.CarbsGoal.setGeometry(QtCore.QRect(90, 110, 61, 31))
        self.CarbsGoal.setObjectName("CarbsGoal")
        
        self.line_6 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_6.setGeometry(QtCore.QRect(10, 140, 741, 20))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        

        
        self.line_9 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_9.setGeometry(QtCore.QRect(10, 350, 741, 20))
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        
        self.slash_9 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.slash_9.setGeometry(QtCore.QRect(70, 250, 21, 31))
        self.slash_9.setObjectName("slash_9")
        
        self.ProteinsGoal = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ProteinsGoal.setGeometry(QtCore.QRect(90, 40, 61, 31))
        self.ProteinsGoal.setObjectName("ProteinsGoal")
        
        self.Carbs = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.Carbs.setGeometry(QtCore.QRect(10, 80, 111, 31))
        self.Carbs.setObjectName("Carbs")
        
        self.CarbsConsumed = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.CarbsConsumed.setGeometry(QtCore.QRect(10, 110, 61, 31))
        self.CarbsConsumed.setObjectName("CarbsConsumed")
        
        self.slash_6 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.slash_6.setGeometry(QtCore.QRect(70, 110, 21, 31))
        self.slash_6.setObjectName("slash_6")

        
        self.Sugar = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.Sugar.setGeometry(QtCore.QRect(10, 220, 111, 31))
        self.Sugar.setObjectName("Sugar")
        
        self.SugarGoal = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.SugarGoal.setGeometry(QtCore.QRect(90, 250, 61, 31))
        self.SugarGoal.setObjectName("SugarGoal")
        
        self.FatsConsumed = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.FatsConsumed.setGeometry(QtCore.QRect(10, 180, 61, 31))
        self.FatsConsumed.setObjectName("FatsConsumed")
        
        self.ProteinsConsumed = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.ProteinsConsumed.setGeometry(QtCore.QRect(10, 40, 61, 31))
        self.ProteinsConsumed.setObjectName("ProteinsConsumed")
        
        self.progressBarSugar = QtWidgets.QProgressBar(self.scrollAreaWidgetContents)
        self.progressBarSugar.setGeometry(QtCore.QRect(160, 230, 591, 31))
        self.progressBarSugar.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.progressBarSugar.setFocusPolicy(QtCore.Qt.TabFocus)
        self.progressBarSugar.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.progressBarSugar.setProperty("value", _getNutritionProgressConsumed(nutrition="sugar"))
        self.progressBarSugar.setObjectName("progressBarSugar")
        
        self.slash_5 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.slash_5.setGeometry(QtCore.QRect(70, 40, 21, 31))
        self.slash_5.setObjectName("slash_5")
        
        self.progressBarCarbs = QtWidgets.QProgressBar(self.scrollAreaWidgetContents)
        self.progressBarCarbs.setGeometry(QtCore.QRect(160, 90, 591, 31))
        self.progressBarCarbs.setProperty("value", _getNutritionProgressConsumed(nutrition="carbohydrates"))
        self.progressBarCarbs.setObjectName("progressBarCarbs")
        
        self.progressBarFats = QtWidgets.QProgressBar(self.scrollAreaWidgetContents)
        self.progressBarFats.setGeometry(QtCore.QRect(160, 160, 591, 31))
        self.progressBarFats.setProperty("value", _getNutritionProgressConsumed(nutrition="fat"))
        self.progressBarFats.setObjectName("progressBarFats")
        

        
        self.line_10 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_10.setGeometry(QtCore.QRect(10, 430, 741, 20))
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.line_11 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_11.setGeometry(QtCore.QRect(10, 510, 741, 20))
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        
        self.SodiumConsumed = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.SodiumConsumed.setGeometry(QtCore.QRect(10, 320, 61, 31))
        self.SodiumConsumed.setObjectName("SodiumConsumed")
        
        self.Sodium = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.Sodium.setGeometry(QtCore.QRect(10, 290, 131, 31))
        self.Sodium.setObjectName("Sodium")
        
        self.slash_11 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.slash_11.setGeometry(QtCore.QRect(70, 320, 21, 31))
        self.slash_11.setObjectName("slash_11")
        
        self.SodiumGoal = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.SodiumGoal.setGeometry(QtCore.QRect(90, 320, 61, 31))
        self.SodiumGoal.setObjectName("SodiumGoal")
        
        self.progressBarSodium = QtWidgets.QProgressBar(self.scrollAreaWidgetContents)
        self.progressBarSodium.setGeometry(QtCore.QRect(160, 300, 591, 31))
        self.progressBarSodium.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.progressBarSodium.setFocusPolicy(QtCore.Qt.TabFocus)
        self.progressBarSodium.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.progressBarSodium.setProperty("value", _getNutritionProgressConsumed(nutrition="sodium"))
        self.progressBarSodium.setObjectName("progressBarSodium")
        
        
        self.line_12 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_12.setGeometry(QtCore.QRect(10, 580, 741, 20))
        self.line_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        
        self.slash_13 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.slash_13.setGeometry(QtCore.QRect(70, 620, 21, 31))
        self.slash_13.setObjectName("slash_13")
        
        
        self.line_13 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_13.setGeometry(QtCore.QRect(10, 650, 741, 20))
        self.line_13.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_13.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_13.setObjectName("line_13")
        

        
        self.slash_14 = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.slash_14.setGeometry(QtCore.QRect(70, 690, 21, 31))
        self.slash_14.setObjectName("slash_14")

        self.line_14 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_14.setGeometry(QtCore.QRect(10, 720, 741, 20))
        self.line_14.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_14.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_14.setObjectName("line_14")
        

        
        self.line_15 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.line_15.setGeometry(QtCore.QRect(10, 790, 741, 20))
        self.line_15.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_15.setObjectName("line_15")
        

        
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        
        self.Tabs.addTab(self.NutritionToday, "")
        
        self.WaterToday = QtWidgets.QWidget()
        self.WaterToday.setObjectName("WaterToday")
        
        
        self.lcdNumberWater = QtWidgets.QLCDNumber(self.WaterToday)
        self.lcdNumberWater.setGeometry(QtCore.QRect(40, 120, 381, 231))
        
        font = QtGui.QFont()
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        
        self.lcdNumberWater.setFont(font)
        self.lcdNumberWater.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lcdNumberWater.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lcdNumberWater.setLineWidth(0)
        self.lcdNumberWater.setMode(QtWidgets.QLCDNumber.Dec)
        self.lcdNumberWater.setProperty("value", day.water/1000)
        self.lcdNumberWater.setObjectName("lcdNumberWater")
        
        self.liters = QtWidgets.QLabel(self.WaterToday)
        self.liters.setGeometry(QtCore.QRect(480, 230, 171, 91))
        
        font = QtGui.QFont()
        font.setPointSize(19)
        self.liters.setFont(font)
        self.liters.setObjectName("liters")
        
        
        self.Tabs.addTab(self.WaterToday, "")

        
        #Water chart
        self.WaterChart = QtWidgets.QWidget()
        layoutWater = QGridLayout(self.WaterChart)
        layoutWater.setRowStretch(1, 1)
        self.WaterChart.resize(800, 400)    
        lWater = QVBoxLayout(self.WaterChart)
        canvasWater = WaterCanvas(self.WaterChart, width=8.3, height=4.8, dpi=96)
        lWater.addWidget(canvasWater)    
        
        self.Tabs.addTab(self.WaterChart, "")
        
                
        #Weight chart
        self.WeightChart = QtWidgets.QWidget()
        layoutWeight = QGridLayout(self.WeightChart)
        layoutWeight.setRowStretch(1, 1)
        self.WeightChart.resize(800, 400)    
        lWeight = QVBoxLayout(self.WeightChart)
        canvasWeight = WeightCanvas(self.WeightChart, width=8.3, height=4.8, dpi=96)
        lWeight.addWidget(canvasWeight) 
        
        self.Tabs.addTab(self.WeightChart, "")
        
        
        # Settings tab
        self.Settings = QtWidgets.QWidget()
        self.Settings.setObjectName("Settings")
        self.Tabs.addTab(self.Settings, "")
        
        

        self.retranslateUi(Application)
        self.Tabs.setCurrentIndex(0) #Set startup tab (was 2)
        QtCore.QMetaObject.connectSlotsByName(Application)
        
        
        # Restart Button
        button = QPushButton('Restart app', self.Settings)
        button.setToolTip('Restart app')
        button.move(50,50) 
        button.clicked.connect(self.restart_click)
        
        # Exit Button
        button = QPushButton('Exit app', self.Settings)
        button.setToolTip('Exit app')
        button.move(250,50) 
        button.clicked.connect(self.exit_click)
        
        
    def restart_click(self):
        Application.close()
        subprocess.call("Python calorietracker.py", shell=True)
        
    def exit_click(self):
        print('EXITING!')
        sys.exit(app.exec_()) 

    def retranslateUi(self, Application):
        _translate = QtCore.QCoreApplication.translate
        Application.setWindowTitle(_translate("Application", "Calorie dashboard"))
        self.Goal.setText(_translate("Application", "Goal"))
        self.Food.setText(_translate("Application", "Food"))
        self.RemainingCalories.setText(_translate("Application", "Remaining calories"))
        self.minus.setText(_translate("Application", "-"))
        self.equal.setText(_translate("Application", "="))
        self.Breakfast.setText(_translate("Application", "Breakfast"))
        self.BreakfastCalConsumed.setText(_translate("Application", str(breakfastConsumed)))
        self.BreakfastCalGoal.setText(_translate("Application", str(breakfastGoal)))
        self.slash_1.setText(_translate("Application", "/"))
        self.LunchCaloriesConsumed.setText(_translate("Application", str(lunchConsumed)))
        self.slash_2.setText(_translate("Application", "/"))
        self.Lunch.setText(_translate("Application", "Lunch"))
        self.LunchCaloriesGoal.setText(_translate("Application", str(lunchGoal)))
        self.slash_3.setText(_translate("Application", "/"))
        self.DinnerCaloriesGoal.setText(_translate("Application", str(dinnerGoal)))
        self.Dinner.setText(_translate("Application", "Dinner"))
        self.DinnerCaloriesConsumed.setText(_translate("Application", str(dinnerConsumed)))
        self.SnacksCaloriesGoal.setText(_translate("Application", str(snacksGoal)))
        self.slash_4.setText(_translate("Application", "/"))
        self.SnacksCaloriesConsumed.setText(_translate("Application", str(snacksConsumed)))
        self.Snacks.setText(_translate("Application", "Snacks"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.Today), _translate("Application", "Today"))
        self.SugarConsumed.setText(_translate("Application", str(sugarConsumed)))
        self.Proteins.setText(_translate("Application", "Proteins"))
        self.Fats.setText(_translate("Application", "Fats"))
        self.FatsGoal.setText(_translate("Application", str(fatGoal)))
        self.slash_7.setText(_translate("Application", "/"))
        self.CarbsGoal.setText(_translate("Application", str(carbohydratesGoal)))
        self.slash_9.setText(_translate("Application", "/"))
        self.ProteinsGoal.setText(_translate("Application", str(proteinGoal)))
        self.Carbs.setText(_translate("Application", "Carbs"))
        self.CarbsConsumed.setText(_translate("Application", str(carbohydratesConsumed)))
        self.slash_6.setText(_translate("Application", "/"))
        self.Sugar.setText(_translate("Application", "Sugar"))
        self.SugarGoal.setText(_translate("Application", str(sugarGoal)))
        self.FatsConsumed.setText(_translate("Application", str(fatConsumed)))
        self.ProteinsConsumed.setText(_translate("Application", str(proteinConsumed)))
        self.slash_5.setText(_translate("Application", "/"))

        self.SodiumConsumed.setText(_translate("Application", str(sodiumConsumed)))
        self.Sodium.setText(_translate("Application", "Sodium"))
        self.slash_11.setText(_translate("Application", "/"))
        self.SodiumGoal.setText(_translate("Application", str(sodiumGoal)))

        self.Tabs.setTabText(self.Tabs.indexOf(self.NutritionToday), _translate("Application", "Nutrition today"))
        self.liters.setText(_translate("Application", "liters"))        
        self.Tabs.setTabText(self.Tabs.indexOf(self.WaterToday), _translate("Application", "Water today"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.WaterChart), _translate("Application", "Water chart"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.WeightChart), _translate("Application", "Weight chart"))
        self.Tabs.setTabText(self.Tabs.indexOf(self.Settings), _translate("Application", "Settings"))

from PyQt5 import QtQuickWidgets

if __name__ == "__main__":
    import sys
    
    print("inside Main")
    
    _calculateRemainingCal()
    _calculateFoodCal()
    _calculateGoalCal()
    _getMealsConsumed()
    _getRoutineSelectionGoals()
    _getNutritionConsumed()
    
    print("done with calculation and get methods")
    
    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
    else:
        print('QApplication instance already exists: %s' % str(app))
        
    Application = QtWidgets.QDialog()
    ui = Ui_Applikasjon()
    ui.setupUi(Application) 
    
    print("About to launch")
    Application.show()
    sys.exit(app.exec_())