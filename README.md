# SimpleITK-registration-documentation
SimpleITK Registration for point transformation
SimpleITK Registration for Points (cloud points):

In order to use SimpleITK registration tools on points (cloud points), we can convert the points to images. Then the images can be registered using SimpleITK package and then extract the points from registered images. However, the calculation time increases considerably. Let's have an example:

R = sitk.ImageRegistrationMethod() # introduce a registration method

R.SetMetricAsMeanSquares() # introduce a metric for similarity calculation between registered image and fixed image

R.SetOptimizerAsRegularStepGradientDescent(learningRate=0.5,minStep=1e-6,numberOfIterations=200,gradientMagnitudeTolerance=1e-8) # introduce optimizer of similarity

R.SetInterpolator(sitk.sitkLinear) # introduce a method for interpolating points though we do not need it finally

initialTx = sitk.CenteredTransformInitializer(fixed, moving,sitk.Similarity2DTransform()) # introduce a transformer which here is 2D

R.SetInitialTransform(initialTx) # set the transformer to the registration method

outTx = R.Execute(fixed, moving) # run the registration method to find the best parameters for the transformer

So far, we registered an image to another. Nevertheless, we do not know each point of the moving image was transformed to which point of the registered image yet. In order to have control on each point (or using transformation on cloud points), ** outTx** (transformer) can be used. let the moving image is 512x512 and P1=(x1,y1) is a point on it. The way that we can find the indexes of P on the registered image (P2=(x2,y2)) is that, firstly extract the physical index of the point P1 on moving as:

x1p,y1p=moving.TransformIndexToPhysicalPoint((x,y)) # transform the index of moving image to physical point

Then transform the physical points to registered image using inverse of the transformer (outTx):

x2p,y2p=outTx.GetInverse().TransformPoint((x1p,y1p)) # transform the physical point of the moving image to fixed coordinate

Then again we have to change the coordination to P2 index by:

x2,y2=fixed.TransformPhysicalPointToIndex((x2p,y2p)) # transform the registered physical points to index Now we have the index of the transformed point on the fixed image coordinate.
