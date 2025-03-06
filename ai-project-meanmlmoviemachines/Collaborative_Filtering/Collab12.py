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

# Check if GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

# Function to download and extract dataset
def download_and_extract(url, extract_to='.'):
    response = requests.get(url)
    zip_path = Path("dataset.zip")
    with open(zip_path, "wb") as file:
        file.write(response.content)
    with ZipFile(zip_path, 'r') as zipObj:
        zipObj.extractall(extract_to)
    zip_path.unlink()

# Download and extract the smallest dataset
smallest_dataset_url = "http://files.grouplens.org/datasets/movielens/ml-latest-small.zip"
download_and_extract(smallest_dataset_url, "ml-latest-small")
smallest_ratings_file = Path("ml-latest-small/ml-latest-small/ratings.csv")

# Download and extract the latest dataset
latest_dataset_url = "http://files.grouplens.org/datasets/movielens/ml-latest.zip"
download_and_extract(latest_dataset_url, "ml-latest")
latest_ratings_file = Path("ml-latest/ml-latest/ratings.csv")

# Function to load and preprocess data
def load_and_preprocess_data(ratings_file):
    df = pd.read_csv(ratings_file)
    user_ids = df["userId"].unique().tolist()
    user2user_encoded = {x: i for i, x in enumerate(user_ids)}
    userencoded2user = {i: x for i, x in enumerate(user_ids)}
    movie_ids = df["movieId"].unique().tolist()
    movie2movie_encoded = {x: i for i, x in enumerate(movie_ids)}
    movie_encoded2movie = {i: x for i, x in enumerate(movie_ids)}
    df["user"] = df["userId"].map(user2user_encoded)
    df["movie"] = df["movieId"].map(movie2movie_encoded)

    num_users = len(user2user_encoded)
    num_movies = len(movie_encoded2movie)
    df["rating"] = df["rating"].values.astype(np.float32)
    min_rating = min(df["rating"])
    max_rating = max(df["rating"])

    # Normalize the targets between 0 and 1
    df["rating"] = df["rating"].apply(lambda x: (x - min_rating) / (max_rating - min_rating))
    return df, num_users, num_movies

# Define the model
EMBEDDING_SIZE = 50

class RecommenderNet(nn.Module):
    def __init__(self, num_users, num_movies, embedding_size):
        super(RecommenderNet, self).__init__()
        self.user_embedding = nn.Embedding(num_users, embedding_size)
        self.user_bias = nn.Embedding(num_users, 1)
        self.movie_embedding = nn.Embedding(num_movies, embedding_size)
        self.movie_bias = nn.Embedding(num_movies, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, inputs):
        user_vector = self.user_embedding(inputs[:, 0])
        user_bias = self.user_bias(inputs[:, 0])
        movie_vector = self.movie_embedding(inputs[:, 1])
        movie_bias = self.movie_bias(inputs[:, 1])
        dot_user_movie = torch.sum(user_vector * movie_vector, dim=1, keepdim=True)
        x = dot_user_movie + user_bias + movie_bias
        return self.sigmoid(x)

# Function to train and evaluate the model
def train_and_evaluate(df, num_users, num_movies, device, embedding_size=50, num_epochs=5, batch_size=64):
    # Shuffle and split the data
    df = df.sample(frac=1, random_state=42)
    x = df[["user", "movie"]].values
    y = df["rating"].values
    train_indices = int(0.9 * df.shape[0])
    x_train, x_val, y_train, y_val = (
        x[:train_indices],
        x[train_indices:],
        y[:train_indices],
        y[train_indices:]
    )

    # Convert to PyTorch tensors
    x_train_tensor = torch.tensor(x_train, dtype=torch.long).to(device)
    y_train_tensor = torch.tensor(y_train, dtype=torch.float32).to(device)
    x_val_tensor = torch.tensor(x_val, dtype=torch.long).to(device)
    y_val_tensor = torch.tensor(y_val, dtype=torch.float32).to(device)

    # Create DataLoader
    train_dataset = TensorDataset(x_train_tensor, y_train_tensor)
    val_dataset = TensorDataset(x_val_tensor, y_val_tensor)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

    # Instantiate the model
    model = RecommenderNet(num_users, num_movies, embedding_size).to(device)

    # Define loss function and optimizer
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # Initialize TensorBoard writer
    writer = SummaryWriter()

    # Training loop
    train_losses = []
    val_losses = []

    for epoch in range(num_epochs):
        model.train()
        train_loss = 0
        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            optimizer.zero_grad()
            outputs = model(inputs).squeeze()
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()
            train_loss += loss.item()
        train_losses.append(train_loss / len(train_loader))
        writer.add_scalar('Loss/train', train_losses[-1], epoch)

        model.eval()
        val_loss = 0
        with torch.no_grad():
            for inputs, targets in val_loader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs).squeeze()
                loss = criterion(outputs, targets)
                val_loss += loss.item()
        val_losses.append(val_loss / len(val_loader))
        writer.add_scalar('Loss/val', val_losses[-1], epoch)

        print(f"Epoch {epoch+1}/{num_epochs}, Train Loss: {train_losses[-1]}, Val Loss: {val_losses[-1]}")

    # Close the TensorBoard writer
    writer.close()

    return train_losses, val_losses

# Load and preprocess the smallest dataset
df_smallest, num_users_smallest, num_movies_smallest = load_and_preprocess_data(smallest_ratings_file)

# Train and evaluate on the smallest dataset
print("Training on the smallest dataset...")
train_losses_smallest, val_losses_smallest = train_and_evaluate(df_smallest, num_users_smallest, num_movies_smallest, device)

# Load and preprocess the latest dataset
df_latest, num_users_latest, num_movies_latest = load_and_preprocess_data(latest_ratings_file)

# Train and evaluate on the latest dataset
print("Training on the latest dataset...")
train_losses_latest, val_losses_latest = train_and_evaluate(df_latest, num_users_latest, num_movies_latest, device)

# Plot the results
plt.plot(train_losses_smallest, label="Train Loss (Smallest Dataset)")
plt.plot(val_losses_smallest, label="Validation Loss (Smallest Dataset)")
plt.plot(train_losses_latest, label="Train Loss (Latest Dataset)")
plt.plot(val_losses_latest, label="Validation Loss (Latest Dataset)")
plt.title("Model Loss vs. Dataset")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()
plt.show()