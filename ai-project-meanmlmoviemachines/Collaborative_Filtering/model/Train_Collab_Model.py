#!/usr/bin/env python3
"""
Title: Collaborative Filtering Model Training and Evaluation
Author: Daniel Moody
Date: 11/03/2025
Description:
    This script trains and evaluates a collaborative filtering models epochs using the MovieLens dataset.

    The script performs the following tasks:
    1. Checks for GPU availability to accelerate training.
    2. Downloads and extracts two versions of the MovieLens dataset:
       - A small dataset (ml-latest-small) for quick experiments.
       - A large dataset (ml-latest) for more in-depth training.
    3. Loads and preprocesses the rating data:
       - Maps original user and movie IDs to continuous integer indices for embedding layers.
       - Normalizes ratings to the range [0, 1] for stable training.
    4. Defines a PyTorch model (RecommenderNet) that uses embeddings and bias terms.
    5. Trains and evaluates the model on both datasets (using a 90/10 train/validation split).
    6. Saves model checkpoints to avoid retraining (training can take hours on a GPU).
    7. Visualizes training/validation loss curves and generates movie recommendations.
    
    This file serves as a complete report of the training process.
"""

# ----------------------------------------------------------------------------------------
# Import Required Libraries
# ----------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
from torch.utils.tensorboard import SummaryWriter
import matplotlib.pyplot as plt
from pathlib import Path
from zipfile import ZipFile
import requests

# ----------------------------------------------------------------------------------------
# 1. Device Configuration
# ----------------------------------------------------------------------------------------
# Check for GPU availability. GPU acceleration can greatly speed up training.
print("GPU availability:", torch.cuda.is_available())
print("Current CUDA Device ID:", torch.cuda.current_device())
print("Current CUDA Device Name:", torch.cuda.get_device_name(torch.cuda.current_device()))
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# ----------------------------------------------------------------------------------------
# 2. Global Settings
# ----------------------------------------------------------------------------------------
# The RETRAIN flag determines whether to retrain the model or load existing pre-trained checkpoints.
# Since training can be time-consuming, it is typically set to False after the initial training.
RETRAIN = False

# ----------------------------------------------------------------------------------------
# 3. Dataset Downloading and Extraction
# ----------------------------------------------------------------------------------------
def download_and_extract(url, extract_to='.'):
    """
    Downloads a zip file from the provided URL and extracts its contents.
    
    Parameters:
        url (str): URL of the dataset zip file.
        extract_to (str): Directory to extract files into (default: current directory).
    
    This function downloads the file, writes it to disk as 'dataset.zip', extracts it,
    and then deletes the zip file to save disk space.
    """
    response = requests.get(url)
    zip_path = Path("dataset.zip")
    with open(zip_path, "wb") as file:
        file.write(response.content)
    with ZipFile(zip_path, 'r') as zipObj:
        zipObj.extractall(extract_to)
    zip_path.unlink()  # Remove the zip file after extraction

# ----------------------------------------------------------------------------------------
# 4. Dataset Paths and Verification
# ----------------------------------------------------------------------------------------
# The script works with two datasets:
#   - The smallest dataset: "ml-latest-small" for rapid experiments.
#   - The latest (large) dataset: "ml-latest" for more robust training.
# Check if each dataset is present locally; if not, download and extract them.

# Check and download the smallest dataset if not present
smallest_dataset_dir = Path("ml-latest-small")
if not smallest_dataset_dir.exists():
    smallest_dataset_url = "http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
    download_and_extract(smallest_dataset_url, "ml-latest-small")
# Define the ratings file path for the smallest dataset
smallest_ratings_file = Path("ml-latest-small/ml-latest-small/ratings.csv")

# Check and download the latest dataset if not present
latest_dataset_dir = Path("ml-latest")
if not latest_dataset_dir.exists():
    latest_dataset_url = "http://files.grouplens.org/datasets/movielens/ml-latest.zip"
    download_and_extract(latest_dataset_url, "ml-latest")
# Define the ratings file path for the latest dataset
latest_ratings_file = Path("ml-latest/ml-latest/ratings.csv")

# ----------------------------------------------------------------------------------------
# 5. Data Loading and Preprocessing
# ----------------------------------------------------------------------------------------
def load_and_preprocess_data(ratings_file, subset_size=None):
    """
    Loads and preprocesses the ratings data from a CSV file.
    
    Steps:
    - Reads the CSV file into a DataFrame.
    - Optionally samples a subset of the data (useful for debugging).
    - Creates mappings for userId and movieId to a continuous index (required for embedding layers).
    - Normalizes the rating values to the range [0, 1] to stabilize training.
    
    Parameters:
        ratings_file (Path): Path to the ratings CSV file.
        subset_size (int, optional): If provided, randomly sample this number of rows.
    
    Returns:
        df (DataFrame): Preprocessed DataFrame.
        num_users (int): Total number of unique users.
        num_movies (int): Total number of unique movies.
        user2user_encoded (dict): Mapping from original userId to encoded index.
        movie2movie_encoded (dict): Mapping from original movieId to encoded index.
        movie_encoded2movie (dict): Reverse mapping from encoded index to original movieId.
        min_rating (float): Minimum rating before normalization.
        max_rating (float): Maximum rating before normalization.
    """
    df = pd.read_csv(ratings_file)
    if subset_size:
        df = df.sample(n=subset_size, random_state=42)

    # Create a mapping for user IDs to a contiguous range of integers
    user_ids = df["userId"].unique().tolist()
    user2user_encoded = {x: i for i, x in enumerate(user_ids)}
    userencoded2user = {i: x for i, x in enumerate(user_ids)}

    # Create a mapping for movie IDs similarly
    movie_ids = df["movieId"].unique().tolist()
    movie2movie_encoded = {x: i for i, x in enumerate(movie_ids)}
    movie_encoded2movie = {i: x for i, x in enumerate(movie_ids)}

    # Add new columns with the encoded user and movie IDs
    df["user"] = df["userId"].map(user2user_encoded)
    df["movie"] = df["movieId"].map(movie2movie_encoded)

    # Compute the total number of unique users and movies
    num_users = len(user2user_encoded)
    num_movies = len(movie_encoded2movie)

    # Convert ratings to float32 and determine the minimum and maximum ratings
    df["rating"] = df["rating"].values.astype(np.float32)
    min_rating = min(df["rating"])
    max_rating = max(df["rating"])

    # Normalize the ratings to the range [0, 1]
    df["rating"] = df["rating"].apply(lambda x: (x - min_rating) / (max_rating - min_rating))

    return df, num_users, num_movies, user2user_encoded, movie2movie_encoded, movie_encoded2movie, min_rating, max_rating

# ----------------------------------------------------------------------------------------
# 6. Model Definition: RecommenderNet
# ----------------------------------------------------------------------------------------
class RecommenderNet(nn.Module):
    """
    Collaborative Filtering Model using Embeddings.
    
    The model includes:
        - An embedding layer for users.
        - An embedding layer for movies.
        - Bias terms for both users and movies.
        - A sigmoid activation to constrain predictions between 0 and 1.
    
    The forward pass computes the dot product between user and movie embeddings, adds bias terms,
    and applies a sigmoid to generate a prediction.
    """
    def __init__(self, num_users, num_movies, embedding_size):
        super(RecommenderNet, self).__init__()
        self.user_embedding = nn.Embedding(num_users, embedding_size)
        self.user_bias = nn.Embedding(num_users, 1)
        self.movie_embedding = nn.Embedding(num_movies, embedding_size)
        self.movie_bias = nn.Embedding(num_movies, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, inputs):
        # Extract user and movie embeddings along with their biases
        user_vector = self.user_embedding(inputs[:, 0])
        user_bias = self.user_bias(inputs[:, 0])
        movie_vector = self.movie_embedding(inputs[:, 1])
        movie_bias = self.movie_bias(inputs[:, 1])
        # Compute dot product between user and movie embeddings
        dot_user_movie = torch.sum(user_vector * movie_vector, dim=1, keepdim=True)
        # Add biases and apply sigmoid activation
        x = dot_user_movie + user_bias + movie_bias
        return self.sigmoid(x)

# ----------------------------------------------------------------------------------------
# 7. Training and Evaluation Function
# ----------------------------------------------------------------------------------------
def train_and_evaluate(df, num_users, num_movies, device, model_path, embedding_size=50, num_epochs=7, batch_size=64):
    """
    Trains the RecommenderNet model and evaluates it on a validation set.
    
    The function performs the following steps:
        1. Shuffles the dataset and splits it into training (90%) and validation (10%) sets.
        2. Converts data into PyTorch tensors and wraps them in DataLoaders.
        3. Instantiates the model, loss function (Binary Cross-Entropy), and optimizer (Adam).
        4. Trains the model over several epochs, logging training and validation loss.
        5. Saves model checkpoints after each epoch.
    
    Parameters:
        df (DataFrame): Preprocessed ratings data.
        num_users (int): Number of unique users.
        num_movies (int): Number of unique movies.
        device (torch.device): Device to perform computations on.
        model_path (str): File path to save the trained model.
        embedding_size (int): Dimensionality of the embedding vectors.
        num_epochs (int): Number of epochs to train.
        batch_size (int): Batch size for training.
    
    Returns:
        train_losses (list): Average training loss per epoch.
        val_losses (list): Average validation loss per epoch.
        model (RecommenderNet): The trained model.
    """
    # Shuffle the dataset and split into training and validation sets
    df = df.sample(frac=1, random_state=42)
    x = df[["user", "movie"]].values
    y = df["rating"].values
    train_indices = int(0.9 * df.shape[0])
    x_train, x_val, y_train, y_val = (x[:train_indices],
                                      x[train_indices:],
                                      y[:train_indices],
                                      y[train_indices:])

    # Convert data to PyTorch tensors
    x_train_tensor = torch.tensor(x_train, dtype=torch.long).to(device)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32).to(device)
    x_val_tensor = torch.tensor(x_val, dtype=torch.long).to(device)
    y_val_tensor = torch.tensor(y_val, dtype=torch.float32).to(device)

    # Create DataLoaders for batching data during training and evaluation
    train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
    val_dataset = TensorDataset(x_val_tensor, y_val_tensor)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    # Instantiate the model
    model = RecommenderNet(num_users, num_movies, embedding_size).to(device)

    # Define the loss function and optimizer
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Initialize TensorBoard writer to log metrics
    writer = SummaryWriter()

    train_losses = []
    val_losses = []

    # Training loop
    for epoch in range(num_epochs):
        model.train()  # Set model to training mode
        train_loss = 0
        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            optimizer.zero_grad()  # Zero the gradients
            outputs = model(inputs).squeeze()  # Forward pass
            loss = criterion(outputs, targets)  # Compute loss
            loss.backward()  # Backward pass
            optimizer.step()  # Update weights
            train_loss += loss.item()
        # Average training loss for the epoch
        train_losses.append(train_loss / len(train_loader))
        writer.add_scalar('Loss/train', train_losses[-1], epoch)

        # Evaluate on the validation set
        model.eval()  # Set model to evaluation mode
        val_loss = 0
        with torch.no_grad():
            for inputs, targets in val_loader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs).squeeze()
                loss = criterion(outputs, targets)
                val_loss += loss.item()
        # Average validation loss for the epoch
        val_losses.append(val_loss / len(val_loader))
        writer.add_scalar('Loss/val', val_losses[-1], epoch)

        # Output training progress to console
        print(f"Epoch {epoch+1}/{num_epochs}, Train Loss: {train_losses[-1]}, Val Loss: {val_losses[-1]}")
        # Save the model checkpoint after each epoch
        torch.save(model.state_dict(), model_path)

    writer.close()  # Close the TensorBoard writer after training

    return train_losses, val_losses, model

# ----------------------------------------------------------------------------------------
# 8. Training/Evaluation for Small and Large Datasets
# ----------------------------------------------------------------------------------------
# Initialize lists to hold loss histories for each dataset.
train_losses_smallest, val_losses_smallest = [], []
train_losses_latest, val_losses_latest = [], []

# ---------------------------
# Small Dataset
# ---------------------------
# Load and preprocess the smallest dataset.
df_smallest, num_users_smallest, num_movies_smallest, user2user_encoded_smallest, movie2movie_encoded_smallest, movie_encoded2movie_smallest, min_rating_smallest, max_rating_smallest = load_and_preprocess_data(smallest_ratings_file)
smallest_model_path = "recommender_smallest.pth"
smallest_embedding_size = 50  # Use a smaller embedding size for the small dataset

# If retraining is enabled or no checkpoint exists, train the model; otherwise, load the saved model.
if RETRAIN or not Path(smallest_model_path).exists():
    print("Training on the smallest dataset...")
    train_losses_smallest, val_losses_smallest, model_smallest = train_and_evaluate(
        df_smallest, num_users_smallest, num_movies_smallest, device, smallest_model_path, embedding_size=smallest_embedding_size)
else:
    print("Loading the smallest dataset model...")
    model_smallest = RecommenderNet(num_users_smallest, num_movies_smallest, smallest_embedding_size).to(device)
    model_smallest.load_state_dict(torch.load(smallest_model_path))

# ---------------------------
# Large Dataset
# ---------------------------
# Load and preprocess the latest (large) dataset.
df_latest, num_users_latest, num_movies_latest, user2user_encoded_latest, movie2movie_encoded_latest, movie_encoded2movie_latest, min_rating_latest, max_rating_latest = load_and_preprocess_data(latest_ratings_file)
latest_model_path = "recommender_latest.pth"
latest_embedding_size = 60  # Use a larger embedding size for the large dataset

# Similarly, decide to train or load the large dataset model based on the RETRAIN flag.
if RETRAIN or not Path(latest_model_path).exists():
    print("Training on the latest dataset...")
    train_losses_latest, val_losses_latest, model_latest = train_and_evaluate(
        df_latest, num_users_latest, num_movies_latest, device, latest_model_path, embedding_size=latest_embedding_size)
else:
    print("Loading the latest dataset model...")
    model_latest = RecommenderNet(num_users_latest, num_movies_latest, latest_embedding_size).to(device)
    model_latest.load_state_dict(torch.load(latest_model_path))

# ----------------------------------------------------------------------------------------
# 9. Visualization of Training and Validation Loss
# ----------------------------------------------------------------------------------------
# If loss histories are available (indicating training was performed), plot them for comparison.
if train_losses_smallest and val_losses_smallest and train_losses_latest and val_losses_latest:
    plt.plot(train_losses_smallest, label="Train Loss (Smallest Dataset)")
    plt.plot(val_losses_smallest, label="Validation Loss (Smallest Dataset)")
    plt.plot(train_losses_latest, label="Train Loss (Latest Dataset)")
    plt.plot(val_losses_latest, label="Validation Loss (Latest Dataset)")
    plt.title("Model Loss vs. Dataset")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.show()

# ----------------------------------------------------------------------------------------
# 10. Recommendation Generation
# ----------------------------------------------------------------------------------------
# Load movie metadata containing movie titles and genres (used for displaying recommendations)
movie_df = pd.read_csv("ml-latest/ml-latest/movies.csv")

def generate_recommendations(df, model, user2user_encoded, movie2movie_encoded, movie_encoded2movie, min_rating, max_rating, user_id=None):
    """
    Generates and displays movie recommendations for a specified user.
    
    Steps:
        1. If no user is specified, select one randomly.
        2. Determine which movies the user has not watched.
        3. Prepare input data pairing the user with each unwatched movie.
        4. Use the model to predict ratings for each candidate movie.
        5. Select the top 10 movies with the highest predicted ratings.
        6. Denormalize the ratings to the original scale.
        7. Display both the movies the user liked and the recommended movies.
    
    Parameters:
        df (DataFrame): The ratings DataFrame.
        model (RecommenderNet): The trained model for making predictions.
        user2user_encoded (dict): Mapping from original userId to encoded index.
        movie2movie_encoded (dict): Mapping from original movieId to encoded index.
        movie_encoded2movie (dict): Reverse mapping for movie IDs.
        min_rating (float): Original minimum rating (for denormalization).
        max_rating (float): Original maximum rating (for denormalization).
        user_id (int, optional): Specific user ID for which to generate recommendations.
    """
    # If no user is specified, choose one at random from the dataset.
    if user_id is None:
        user_id = df.userId.sample(1).iloc[0]
    else:
        if user_id not in user2user_encoded:
            print(f"User ID {user_id} not found in the dataset.")
            return
    # Identify movies already watched by the user.
    movies_watched_by_user = df[df.userId == user_id]
    # Identify movies not watched by comparing against the movie metadata.
    movies_not_watched = movie_df[~movie_df["movieId"].isin(movies_watched_by_user.movieId.values)]["movieId"]
    # Ensure that these movies are present in our encoded mapping.
    movies_not_watched = list(set(movies_not_watched).intersection(set(movie2movie_encoded.keys())))
    # Convert the movie IDs to their encoded format.
    movies_not_watched = [[movie2movie_encoded.get(x)] for x in movies_not_watched]

    # Retrieve the encoded user index.
    user_encoder = user2user_encoded.get(user_id)
    # Create an array pairing the user with each candidate movie.
    user_movie_array = np.hstack(([[user_encoder]] * len(movies_not_watched), movies_not_watched))
    # Predict ratings for each candidate movie using the trained model.
    ratings = model(torch.tensor(user_movie_array).to(device)).detach().cpu().numpy().flatten()
    # Identify indices of the top 10 predicted ratings.
    top_ratings_indices = ratings.argsort()[-10:][::-1]
    # Map these indices back to the original movie IDs.
    recommended_movie_ids = [movie_encoded2movie.get(movies_not_watched[x][0]) for x in top_ratings_indices]
    recommended_ratings = [ratings[x] for x in top_ratings_indices]

    # Denormalize ratings to reflect the original rating scale.
    recommended_ratings = [rating * (max_rating - min_rating) + min_rating for rating in recommended_ratings]

    # Display the recommendations.
    print("Showing recommendations for user: {}".format(user_id))
    print("====" * 9)
    print("Movies with high ratings from user")
    print("----" * 8)
    # Retrieve top movies the user has already rated highly.
    top_movies_user = movies_watched_by_user.sort_values(by="rating", ascending=False).head(5).movieId.values
    movie_df_rows = movie_df[movie_df["movieId"].isin(top_movies_user)]
    for row in movie_df_rows.itertuples():
        print(row.title, ":", row.genres)

    print("----" * 8)
    print("Top 10 movie recommendations")
    print("----" * 8)
    recommended_movies = movie_df[movie_df["movieId"].isin(recommended_movie_ids)]
    for row, rating in zip(recommended_movies.itertuples(), recommended_ratings):
        print(f"{row.title} ({row.genres}): {rating:.2f}")

# ----------------------------------------------------------------------------------------
# 11. Generate Recommendations for Evaluation
# ----------------------------------------------------------------------------------------
# Display recommendations for a randomly selected user from both datasets.
print("\nRecommendations for the smallest dataset:")
generate_recommendations(df_smallest, model_smallest, user2user_encoded_smallest, movie2movie_encoded_smallest, movie_encoded2movie_smallest, min_rating_smallest, max_rating_smallest)

print("\nRecommendations for the latest dataset:")
generate_recommendations(df_latest, model_latest, user2user_encoded_latest, movie2movie_encoded_latest, movie_encoded2movie_latest, min_rating_latest, max_rating_latest)
