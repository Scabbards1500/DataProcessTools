import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

def load_images_from_folder(folder, max_images=25, size=(512, 512)):
    """Load grayscale images from folder and resize."""
    images = []
    for fname in os.listdir(folder):
        fpath = os.path.join(folder, fname)
        try:
            img = Image.open(fpath).convert('L')
            img = img.resize(size)
            images.append(np.array(img))
            if len(images) >= max_images:
                break
        except:
            continue
    return np.stack(images, axis=0)

def compute_avg_low_freq_distribution(images, cutoff_ratio=0.5, enhance='log'):
    """
    Compute average low-frequency distribution.
    enhance: 'log' for log1p, 'sqrt' for sqrt, None for linear
    """
    N, H, W = images.shape
    center_y, center_x = H // 2, W // 2
    radius = int(min(H, W) * cutoff_ratio / 2)

    y, x = np.ogrid[:H, :W]
    mask = (x - center_x)**2 + (y - center_y)**2 <= radius**2

    low_freq_sum = np.zeros((H, W))
    for img in images:
        F = np.fft.fft2(img)
        F_shift = np.fft.fftshift(F)
        amp = np.abs(F_shift)
        low_freq_sum += amp * mask  # Only accumulate low-frequency region

    avg_low = low_freq_sum / N

    # Enhance visualization contrast
    if enhance == 'log':
        avg_low = np.log1p(avg_low)
    elif enhance == 'sqrt':
        avg_low = np.sqrt(avg_low)

    # Normalize to 0-1
    avg_low = (avg_low - avg_low.min()) / (avg_low.max() - avg_low.min())
    return avg_low, mask

def visualize_low_freq_heatmaps(folders, labels=None, cutoff_ratio=0.5, save_path=None):
    n = len(folders)
    plt.figure(figsize=(4*n, 4))

    for i, folder in enumerate(folders):
        imgs = load_images_from_folder(folder)
        avg_low, mask = compute_avg_low_freq_distribution(imgs, cutoff_ratio=cutoff_ratio, enhance='log')

        # Only display low-frequency region
        display_map = np.zeros_like(avg_low)
        display_map[mask] = avg_low[mask]

        plt.subplot(1, n, i+1)
        im = plt.imshow(display_map, cmap='inferno', origin='lower')
        plt.axis('off')
        if labels:
            plt.title(labels[i], fontsize=16, fontweight='bold')

    cbar = plt.colorbar(im, fraction=0.046, pad=0.04)
    cbar.set_label('Normalized Low-Frequency Energy', fontsize=14, fontweight='medium')
    cbar.ax.tick_params(labelsize=12)
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.show()

def extract_spectral_features(images, cutoff_ratio=0.5):
    """
    Extract spectral feature vector for each image.
    Returns: (N, feature_dim) feature matrix
    """
    N, H, W = images.shape
    center_y, center_x = H // 2, W // 2
    radius = int(min(H, W) * cutoff_ratio / 2)
    
    y, x = np.ogrid[:H, :W]
    mask = (x - center_x)**2 + (y - center_y)**2 <= radius**2
    
    features = []
    for img in images:
        # Compute FFT
        F = np.fft.fft2(img)
        F_shift = np.fft.fftshift(F)
        amp = np.abs(F_shift)
        phase = np.angle(F_shift)
        
        # Extract low-frequency region
        low_freq_amp = amp[mask]
        low_freq_phase = phase[mask]
        
        # Extract statistical features
        feature_vec = [
            np.mean(low_freq_amp),           # Mean amplitude
            np.std(low_freq_amp),            # Amplitude std
            np.median(low_freq_amp),         # Amplitude median
            np.sum(low_freq_amp),            # Total energy
            np.mean(low_freq_phase),         # Mean phase
            np.std(low_freq_phase),          # Phase std
            np.percentile(low_freq_amp, 25), # 25th percentile
            np.percentile(low_freq_amp, 75), # 75th percentile
        ]
        
        # Also add high-frequency features for comparison
        high_freq_mask = ~mask
        high_freq_amp = amp[high_freq_mask]
        if len(high_freq_amp) > 0:
            feature_vec.extend([
                np.mean(high_freq_amp),
                np.std(high_freq_amp),
                np.sum(high_freq_amp),
            ])
        
        features.append(feature_vec)
    
    return np.array(features)

def confidence_ellipse(x, y, ax, n_std=2.0, facecolor='none', edgecolor='black', alpha=0.1, linewidth=2, **kwargs):
    """
    Draw confidence ellipse.
    x, y: coordinates of data points
    n_std: number of standard deviations (2.0 corresponds to ~95% confidence interval)
    """
    if x.size != y.size:
        raise ValueError("x and y must have the same size")
    
    # Compute covariance matrix
    cov = np.cov(x, y)
    
    # Compute ellipse center
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    
    # Compute eigenvalues and eigenvectors to determine ellipse direction and size
    eigenvals, eigenvecs = np.linalg.eigh(cov)
    order = eigenvals.argsort()[::-1]
    eigenvals, eigenvecs = eigenvals[order], eigenvecs[:, order]
    
    # Compute angle (in degrees)
    angle = np.degrees(np.arctan2(*eigenvecs[:, 0][::-1]))
    
    # Compute ellipse width and height (based on standard deviation)
    width, height = 2 * n_std * np.sqrt(eigenvals)
    
    # Create ellipse object
    ellipse = Ellipse((mean_x, mean_y), width=width, height=height, angle=angle,
                      facecolor=facecolor, edgecolor=edgecolor, alpha=alpha, linewidth=linewidth, **kwargs)
    
    return ellipse

def visualize_spectral_distribution(folders, labels=None, method='tsne', cutoff_ratio=0.5, save_path=None, show_ellipse=True, ellipse_alpha=0.1):
    """
    Visualize spectral features of datasets with dimensionality reduction.
    method: 'pca' or 'tsne'
    """
    all_features = []
    all_labels = []
    all_images_list = []  # Save all images to avoid reloading
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']  # Colors for four datasets
    
    # Extract features from all datasets
    for i, folder in enumerate(folders):
        imgs = load_images_from_folder(folder)
        all_images_list.append(imgs)  # Save images
        features = extract_spectral_features(imgs, cutoff_ratio=cutoff_ratio)
        all_features.append(features)
        label_name = labels[i] if labels else f"Dataset {i+1}"
        all_labels.extend([label_name] * len(features))
    
    # Combine all features
    X = np.vstack(all_features)
    
    # Normalize features
    X_mean = X.mean(axis=0)
    X_std = X.std(axis=0)
    X_std[X_std == 0] = 1  # Avoid division by zero
    X_normalized = (X - X_mean) / X_std
    
    # Dimensionality reduction
    if method.lower() == 'pca':
        reducer = PCA(n_components=2, random_state=42)
        X_reduced = reducer.fit_transform(X_normalized)
        title_suffix = f'PCA (Explained Variance: {reducer.explained_variance_ratio_.sum():.2%})'
    elif method.lower() == 'tsne':
        reducer = TSNE(n_components=2, random_state=42, perplexity=min(30, len(X)//4))
        X_reduced = reducer.fit_transform(X_normalized)
        title_suffix = 't-SNE'
    else:
        raise ValueError("method must be 'pca' or 'tsne'")
    
    # Visualization
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Draw scatter points and confidence ellipses for each dataset
    start_idx = 0
    for i, imgs in enumerate(all_images_list):
        n_samples = len(imgs)
        end_idx = start_idx + n_samples
        
        label_name = labels[i] if labels else f"Dataset {i+1}"
        x_data = X_reduced[start_idx:end_idx, 0]
        y_data = X_reduced[start_idx:end_idx, 1]
        
        # Draw confidence ellipse (draw first so scatter points are on top)
        if show_ellipse and n_samples >= 3:  # Need at least 3 points to compute covariance
            ellipse = confidence_ellipse(x_data, y_data, ax, 
                                        n_std=2.0,  # 95% confidence interval
                                        facecolor=colors[i % len(colors)],
                                        edgecolor=colors[i % len(colors)],
                                        alpha=ellipse_alpha,
                                        linewidth=2.5)
            ax.add_patch(ellipse)
        
        # Draw scatter points
        ax.scatter(x_data, y_data,
                   c=colors[i % len(colors)],
                   label=label_name,
                   alpha=0.6,
                   s=80,
                   edgecolors='black',
                   linewidths=0.8,
                   zorder=10)  # Ensure scatter points are on top of ellipses
        
        start_idx = end_idx
    
    ax.set_xlabel(f'Component 1 ({title_suffix})', fontsize=16, fontweight='medium')
    ax.set_ylabel(f'Component 2 ({title_suffix})', fontsize=16, fontweight='medium')
    ax.set_title(f'Raw image distribution', fontsize=20, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc='best', fontsize=14, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.show()
    
    return X_reduced, all_labels

if __name__ == "__main__":
    folders = [
        r"D:\tempdataset\RITE\images512",
        r"D:\tempdataset\HRF\images512",
        r"D:\tempdataset\CHASEDB1\images512",
        r"D:\tempdataset\Retina\train\image512"
    ]
    labels = ["RITE", "HRF", "CHASE", "Retina"]
    
    # Original heatmap visualization
    # visualize_low_freq_heatmaps(folders, labels, cutoff_ratio=0.5, save_path="low_freq_distribution.png")
    
    # New dimensionality reduction scatter plot visualization
    # visualize_spectral_distribution(folders, labels, method='tsne', cutoff_ratio=0.5, save_path="spectral_distribution_tsne.png")
    # Or try PCA
    visualize_spectral_distribution(folders, labels, method='pca', cutoff_ratio=0.5, save_path="spectral_distribution_pca.png")
