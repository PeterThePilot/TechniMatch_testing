import numpy as np
import pandas as pd
from sklearn.decomposition import TruncatedSVD


def predict_rankings(password):
    # Load the course rankings data
    df = pd.read_csv("courses_rankings.csv")

    # Fill missing rankings (zeros) with the average ranking for each course
    df_filled = df.replace(0, np.nan)  # Replace 0 with NaN for proper calculation
    course_means = df_filled.mean(axis=0).fillna(0)  # Compute means, filling NaNs with 0 for courses never rated
    df_filled = df_filled.fillna(course_means)  # Fill missing data with means

    # Convert DataFrame to a matrix
    matrix = df_filled.values

    # Apply SVD for matrix factorization
    svd = TruncatedSVD(n_components=5, random_state=42)
    matrix_reduced = svd.fit_transform(matrix)  # Reduce dimensions
    matrix_predicted = svd.inverse_transform(matrix_reduced)  # Predict missing values

    # Update original matrix with predicted rankings for missing values
    original_matrix = df.values
    predicted_rankings = np.where(original_matrix == 0, matrix_predicted, original_matrix)

    # Find the predicted rankings for the student with index `password`
    student_rankings = predicted_rankings[int(password)]

    # Return the predicted rankings
    return student_rankings


# Example usage
password = 0  # Index of the student
predicted_rankings = predict_rankings(password)
print(predicted_rankings)