# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:34:50 2021

@author: Mehran Azimbagirad
"""
import SimpleITK as sitk
import numpy as np
import matplotlib.pyplot as plt
moving=sitk.ReadImage('Slice_1.nii.gz',sitk.sitkFloat32)
fixed=sitk.ReadImage('Slice_2.nii.gz',sitk.sitkFloat32)
R = sitk.ImageRegistrationMethod()
#------------- Similarity metrics-------------------------
R.SetMetricAsMeanSquares()
#R.SetMetricAsMattesMutualInformation()
#R.SetMetricAsANTSNeighborhoodCorrelation(3)
#R.SetMetricAsMattesMutualInformation(numberOfHistogramBins=50)
#------------- Optimizer -----------------------------------
R.SetOptimizerAsRegularStepGradientDescent(learningRate=0.5,minStep=1e-6,numberOfIterations=200,gradientMagnitudeTolerance=1e-8)
#R.SetOptimizerAsGradientDescent(learningRate=0.5, numberOfIterations=200, estimateLearningRate = R.EachIteration)
#R.SetOptimizerAsLBFGS2() 
#R.SetOptimizerAsLBFGSB() 
#R.SetOptimizerAsExhaustive(numberOfSteps=1, stepLength=1.0)
#R.SetOptimizerAsGradientDescentLineSearch(learningRate=0.5,numberOfIterations=200,convergenceMinimumValue=1e-6,convergenceWindowSize=4)
#R.SetOptimizerScalesFromPhysicalShift()
#R.SetOptimizerAsGradientDescentLineSearch(learningRate=0.1,numberOfIterations=400,convergenceMinimumValue=1e-7,convergenceWindowSize=4)
#-------------- Interpolator --------------------------------
R.SetInterpolator(sitk.sitkLinear)
#R.SetInterpolator(sitk.sitkBSpline())
#-------------- Transformer --------------------------------
#R.SetInitialTransform(sitk.TranslationTransform(fixed.GetDimension()))
#initialTx = sitk.CenteredTransformInitializer(fixed, moving,sitk.AffineTransform(fixed.GetDimension()))
#initialTx = sitk.TranslationTransform(fixed.GetDimension())
initialTx = sitk.CenteredTransformInitializer(fixed, moving,sitk.Similarity2DTransform())
#initialTx = sitk.Similarity2DTransform()
#-------------------------------------------
R.SetInitialTransform(initialTx)
outTx = R.Execute(fixed, moving)
#--------------------------------------------
moving_array=sitk.GetArrayFromImage(moving)
x,y=np.where(moving_array!=0)
Xt=[]
Yt=[]
ind2physX=[]
ind2physY=[]
for j in range(len(x)):
   ind2physx,ind2physy=moving.TransformIndexToPhysicalPoint((int(y[j]),int(x[j])))
   ind2physX.append(ind2physx)
   ind2physY.append(ind2physy)
for j in range(len(x)):
    xt,yt=outTx.GetInverse().TransformPoint((ind2physX[j],ind2physY[j]))
    ind2physx,ind2physy=fixed.TransformPhysicalPointToIndex((xt,yt))
    Xt.append(ind2physx)
    Yt.append(ind2physy)
fixed_array=sitk.GetArrayFromImage(fixed)
x2,y2=np.where(fixed_array!=0)
fig, ax=plt.subplots(2)
ax[0].plot(x2, y2, 'b.')
ax[0].plot(x,y,'ro')
ax[1].plot(x2, y2, 'b.')
ax[1].plot(Yt,Xt,'ro')
