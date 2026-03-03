import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import random


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
    mask = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2

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
    plt.figure(figsize=(4 * n, 4))

    for i, folder in enumerate(folders):
        imgs = load_images_from_folder(folder)
        avg_low, mask = compute_avg_low_freq_distribution(imgs, cutoff_ratio=cutoff_ratio, enhance='log')

        # Only display low-frequency region
        display_map = np.zeros_like(avg_low)
        display_map[mask] = avg_low[mask]

        plt.subplot(1, n, i + 1)
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
    mask = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2

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
            np.mean(low_freq_amp),  # Mean amplitude
            np.std(low_freq_amp),  # Amplitude std
            np.median(low_freq_amp),  # Amplitude median
            np.sum(low_freq_amp),  # Total energy
            np.mean(low_freq_phase),  # Mean phase
            np.std(low_freq_phase),  # Phase std
            np.percentile(low_freq_amp, 25),  # 25th percentile
            np.percentile(low_freq_amp, 75),  # 75th percentile
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


def extract_low_freq_component(img, cutoff_ratio=0.5):
    """
    Extract low-frequency component from a single image.
    Returns: low-frequency amplitude (flattened for storage)
    """
    H, W = img.shape
    center_y, center_x = H // 2, W // 2
    radius = int(min(H, W) * cutoff_ratio / 2)
    
    y, x = np.ogrid[:H, :W]
    mask = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2
    
    # Compute FFT
    F = np.fft.fft2(img)
    F_shift = np.fft.fftshift(F)
    amp = np.abs(F_shift)
    
    # Extract low-frequency region
    low_freq_amp = amp[mask]
    
    return low_freq_amp, mask


class StyleCuesBank:
    """
    Style Cues Bank (SCB) for storing and retrieving low-frequency style vectors.
    Implements queue-style management with protected tail.
    """
    def __init__(self, capacity=20, k_neighbors=3, protected_tail=5, cutoff_ratio=0.5):
        """
        Initialize Style Cues Bank.
        Args:
            capacity: Maximum number of styles to store
            k_neighbors: Number of nearest neighbors to retrieve
            protected_tail: Number of most recent styles to protect from eviction
            cutoff_ratio: Ratio for low-frequency cutoff
        """
        self.capacity = capacity
        self.k_neighbors = k_neighbors
        self.protected_tail = protected_tail
        self.cutoff_ratio = cutoff_ratio
        
        # Bank structure: list of tuples (style_vector, count, dataset_label, age)
        # style_vector: flattened low-frequency amplitude
        # count: number of times this style was retrieved
        # dataset_label: which dataset this style came from
        # age: insertion order (for tie-breaking)
        self.bank = []
        self.age_counter = 0
        
    def add_style(self, style_vector, dataset_label):
        """
        Add a new style to the bank.
        Args:
            style_vector: flattened low-frequency amplitude vector
            dataset_label: label of the dataset this style belongs to
        """
        # Check if bank is full and needs eviction
        if len(self.bank) >= self.capacity:
            self._evict_least_used()
        
        # Add new style with count=1
        self.bank.append({
            'style': style_vector,
            'count': 1,
            'dataset': dataset_label,
            'age': self.age_counter
        })
        self.age_counter += 1
    
    def _evict_least_used(self):
        """Evict the least used style (excluding protected tail)."""
        if len(self.bank) < self.capacity:
            return
        
        # Only consider styles not in the protected tail
        evictable_indices = list(range(len(self.bank) - self.protected_tail))
        if not evictable_indices:
            return
        
        # Find minimum count among evictable styles
        evictable_counts = [self.bank[i]['count'] for i in evictable_indices]
        min_count = min(evictable_counts)
        
        # Find the oldest style with minimum count (break ties by age)
        candidates = [i for i in evictable_indices if self.bank[i]['count'] == min_count]
        oldest_idx = min(candidates, key=lambda i: self.bank[i]['age'])
        
        # Remove the selected style
        self.bank.pop(oldest_idx)
    
    def retrieve_and_update(self, query_style, query_dataset_label):
        """
        Retrieve K nearest neighbors and update the bank.
        Args:
            query_style: flattened low-frequency amplitude vector of query image
            query_dataset_label: label of the query dataset
        Returns:
            S_ref: averaged style reference (None if bank size < K)
            updated: whether retrieval was performed
        """
        # If bank is too small, just add without retrieval
        if len(self.bank) < self.k_neighbors:
            self.add_style(query_style, query_dataset_label)
            return None, False
        
        # Find K nearest neighbors
        bank_styles = np.array([item['style'] for item in self.bank])
        
        # Compute distances (L2 distance)
        distances = np.linalg.norm(bank_styles - query_style, axis=1)
        nearest_indices = np.argsort(distances)[:self.k_neighbors]
        
        # Update counts for retrieved styles
        for idx in nearest_indices:
            self.bank[idx]['count'] += 1
        
        # Compute average reference style
        S_ref = np.mean(bank_styles[nearest_indices], axis=0)
        
        # Add query style to bank
        self.add_style(query_style, query_dataset_label)
        
        return S_ref, True


def process_with_scb(folders, labels=None, max_images_per_folder=25, 
                     scb_capacity=20, k_neighbors=3, protected_tail=5, 
                     cutoff_ratio=0.5, random_seed=42):
    """
    Process images through Style Cues Bank and return processed features.
    Returns:
        original_features: features before SCB processing
        processed_features: features after SCB processing (style harmonized)
        scb_features: features of styles in the SCB
        all_dataset_labels: dataset labels for all images
        scb_dataset_labels: dataset labels for SCB styles
    """
    random.seed(random_seed)
    np.random.seed(random_seed)
    
    # Initialize SCB
    scb = StyleCuesBank(capacity=scb_capacity, k_neighbors=k_neighbors, 
                       protected_tail=protected_tail, cutoff_ratio=cutoff_ratio)
    
    # Collect all images with their dataset labels
    all_images = []
    all_dataset_labels = []
    all_image_objects = []  # Store original image arrays
    
    for i, folder in enumerate(folders):
        imgs = load_images_from_folder(folder, max_images=max_images_per_folder)
        dataset_label = labels[i] if labels else f"Dataset {i+1}"
        
        for img in imgs:
            all_images.append(img)
            all_dataset_labels.append(dataset_label)
            all_image_objects.append(img)
    
    # Shuffle for random processing order
    indices = list(range(len(all_images)))
    random.shuffle(indices)
    
    # Process images through SCB
    original_features = []
    processed_features = []
    scb_styles = []
    scb_dataset_labels = []
    
    for idx in indices:
        img = all_images[idx]
        dataset_label = all_dataset_labels[idx]
        
        # Extract low-frequency component
        low_freq_amp, mask = extract_low_freq_component(img, cutoff_ratio=cutoff_ratio)
        
        # Extract original features
        img_features = extract_spectral_features(img[np.newaxis, :, :], cutoff_ratio=cutoff_ratio)[0]
        original_features.append(img_features)
        
        # Retrieve from SCB and update
        S_ref, retrieved = scb.retrieve_and_update(low_freq_amp, dataset_label)
        
        if retrieved:
            # Style harmonization: replace low-frequency with reference
            H, W = img.shape
            center_y, center_x = H // 2, W // 2
            radius = int(min(H, W) * cutoff_ratio / 2)
            y, x = np.ogrid[:H, :W]
            mask_full = (x - center_x) ** 2 + (y - center_y) ** 2 <= radius ** 2
            
            # Reconstruct FFT
            F = np.fft.fft2(img)
            F_shift = np.fft.fftshift(F)
            amp = np.abs(F_shift)
            phase = np.angle(F_shift)
            
            # Replace low-frequency amplitude with reference
            # S_ref is averaged from K styles, need to match the shape
            amp_new = amp.copy()
            mask_size = np.sum(mask_full)
            if len(S_ref) == mask_size:
                amp_new[mask_full] = S_ref
            else:
                # If sizes don't match, interpolate or use mean
                # For simplicity, use mean value scaled to match
                mean_ref = np.mean(S_ref)
                amp_new[mask_full] = mean_ref
            
            # Reconstruct image in frequency domain
            F_new = amp_new * np.exp(1j * phase)
            F_new_shift = np.fft.ifftshift(F_new)
            img_processed = np.real(np.fft.ifft2(F_new_shift))
            
            # Extract features from processed image
            processed_features.append(
                extract_spectral_features(img_processed[np.newaxis, :, :], cutoff_ratio=cutoff_ratio)[0]
            )
        else:
            # No retrieval, use original
            processed_features.append(img_features)
        
        # Store SCB styles for visualization
        if len(scb.bank) > 0:
            scb_styles = [item['style'] for item in scb.bank]
            scb_dataset_labels = [item['dataset'] for item in scb.bank]
    
    # Convert SCB styles to features (approximate using statistics)
    scb_features = []
    for style_vec in scb_styles:
        # Convert style vector to feature vector (using statistics)
        feature_vec = [
            np.mean(style_vec),
            np.std(style_vec),
            np.median(style_vec),
            np.sum(style_vec),
            np.percentile(style_vec, 25),
            np.percentile(style_vec, 75),
        ]
        # Pad to match feature dimension (add zeros for missing features)
        while len(feature_vec) < len(original_features[0]):
            feature_vec.append(0.0)
        scb_features.append(feature_vec[:len(original_features[0])])
    
    return (np.array(original_features), np.array(processed_features), 
            np.array(scb_features) if scb_features else None,
            all_dataset_labels, scb_dataset_labels)


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


def visualize_spectral_distribution(folders, labels=None, method='tsne', cutoff_ratio=0.5, save_path=None,
                                    show_ellipse=True, ellipse_alpha=0.1):
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
        label_name = labels[i] if labels else f"Dataset {i + 1}"
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
        reducer = TSNE(n_components=2, random_state=42, perplexity=min(30, len(X) // 4))
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

        label_name = labels[i] if labels else f"Dataset {i + 1}"
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
    ax.set_title(f' Fourier Domain Harmonized Distribution', fontsize=20, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc='best', fontsize=14, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.show()

    return X_reduced, all_labels


def visualize_scb_distribution(folders, labels=None, method='pca', cutoff_ratio=0.5, 
                               save_path=None, show_ellipse=True, ellipse_alpha=0.1,
                               scb_capacity=20, k_neighbors=3, protected_tail=5):
    """
    Visualize spectral features after Style Cues Bank processing.
    """
    # Process images through SCB
    original_features, processed_features, scb_features, all_labels, scb_labels = \
        process_with_scb(folders, labels=labels, cutoff_ratio=cutoff_ratio,
                        scb_capacity=scb_capacity, k_neighbors=k_neighbors, 
                        protected_tail=protected_tail)
    
    # Normalize features (only processed features)
    X_mean = processed_features.mean(axis=0)
    X_std = processed_features.std(axis=0)
    X_std[X_std == 0] = 1
    X_normalized = (processed_features - X_mean) / X_std
    
    # Dimensionality reduction
    if method.lower() == 'pca':
        reducer = PCA(n_components=2, random_state=42)
        processed_reduced = reducer.fit_transform(X_normalized)
        title_suffix = f'PCA (Explained Variance: {reducer.explained_variance_ratio_.sum():.2%})'
    elif method.lower() == 'tsne':
        reducer = TSNE(n_components=2, random_state=42, perplexity=min(30, len(X_normalized) // 4))
        processed_reduced = reducer.fit_transform(X_normalized)
        title_suffix = 't-SNE'
    else:
        raise ValueError("method must be 'pca' or 'tsne'")
    
    # Visualization
    fig, ax = plt.subplots(figsize=(10, 8))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    unique_labels = list(set(all_labels))
    
    # Draw scatter points and confidence ellipses for each dataset
    for i, label in enumerate(unique_labels):
        label_indices = [j for j, l in enumerate(all_labels) if l == label]
        x_data = processed_reduced[label_indices, 0]
        y_data = processed_reduced[label_indices, 1]
        
        # Draw confidence ellipse (draw first so scatter points are on top)
        if show_ellipse and len(label_indices) >= 3:
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
                   label=label,
                   alpha=0.6,
                   s=80,
                   edgecolors='black',
                   linewidths=0.8,
                   zorder=10)  # Ensure scatter points are on top of ellipses
    
    ax.set_xlabel(f'Component 1 ({title_suffix})', fontsize=16, fontweight='medium')
    ax.set_ylabel(f'Component 2 ({title_suffix})', fontsize=16, fontweight='medium')
    ax.set_title(f'Fourier Domain Harmonized Distribution', fontsize=20, fontweight='bold')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc='best', fontsize=14, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    plt.show()
    
    return processed_reduced, all_labels


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
    # visualize_spectral_distribution(folders, labels, method='pca', cutoff_ratio=0.5,
    #                                 save_path="spectral_distribution_pca.png")
    
    # SCB-based visualization
    visualize_scb_distribution(folders, labels, method='pca', cutoff_ratio=0.5,
                              save_path="spectral_distribution_scb.png",
                              scb_capacity=20, k_neighbors=3, protected_tail=5)
