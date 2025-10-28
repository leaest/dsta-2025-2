#Milestone 1
##Exercise 1
###What is the dataset about?
The MNIST dataset is a combination of two datasets from the National Institute of Standards and Technology (NIST). Both parts are of equal size, one sourced from Census Bureau employees and the other from high school students. In total, the dataset contains 70,000 data points.
It includes only two columns: image and label. The image column contains a black-and-white picture of a single handwritten digit with a resolution of 28×28 pixels. The corresponding label indicates which of the ten classes the digit belongs to, representing the numbers 0 through 9. Each class contains 7’000 images, with 10% allocated to the test set. Overall, both the training and test sets follow the same distribution in terms of source and number of samples per digit.
This makes the dataset particularly useful for those who want to experiment with machine learning algorithms or pattern recognition techniques with minimal preparation and formatting effort.

###What problem is solved by the machine learning models trained on it?
Since the digits are treated as categorical labels rather than numerical values, the dataset is used to train machine learning models for classification, not regression.
Therefore, it is not suitable for predicting continuous numerical values or performing quantitative calculations. The use of this dataset enables models to learn how to classify handwritten digits, which can, for example, be applied to analyze handwritten text more quickly and efficiently.
