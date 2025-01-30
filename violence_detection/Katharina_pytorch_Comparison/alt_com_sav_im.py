from PIL import Image
import os
import json
from transformers import CLIPProcessor, CLIPModel
from tqdm import tqdm  # Progress tracking

# Define paths
IMAGE_FOLDER = "/Users/apple/Downloads/Deteced-images"
RESULTS_FILE = "/Users/apple/Documents/HIWI_Katharina/Hiwi_Katarina/violence_detection/Katharina_pytorch_Comparison/weapon_classification_results.json"
SAVE_FOLDER = "/Users/apple/Documents/HIWI_Katharina/Hiwi_Katarina/violence_detection/Matched_Images"

# Load CLIP model
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")


def load_roboflow_results(filepath):
    """Loads and processes the weapon classification results from Roboflow."""
    with open(filepath, "r") as f:
        data = json.load(f)

    if "results" not in data or not isinstance(data["results"], list):
        raise ValueError("Unexpected JSON format: Expected a dictionary with a 'results' list.")

    roboflow_results = {
        entry["image_name"]: "weapon" if any(cls in ["Knife", "Gun", "Grenade", "Baton"] for cls in entry["classes"]) else "not weapon"
        for entry in data["results"]
    }
    return roboflow_results


def analyze_with_clip(image_paths, thresholds):
    """Processes images using CLIP and applies different thresholds."""
    clip_results_per_threshold = {}

    for threshold in thresholds:
        weapon_images = []

        for image_path in tqdm(image_paths, desc=f"Processing images at threshold {threshold}"):
            img = Image.open(image_path).convert("RGB")  # Ensure RGB mode
            inputs = clip_processor(text=["weapon", "not weapon"], images=img, return_tensors="pt", padding=True)
            outputs = clip_model(**inputs)
            logits_per_image = outputs.logits_per_image.softmax(dim=1).detach().numpy()

            if logits_per_image[0][0] > threshold:  # 0-th index for "weapon"
                weapon_images.append(image_path)

        clip_results_per_threshold[threshold] = weapon_images

    return clip_results_per_threshold


def compare_results(clip_results, roboflow_results, image_folder):
    """Compares CLIP's predictions against Roboflow's ground truth."""
    comparison_stats = {}

    for threshold, clip_detected_images in clip_results.items():
        correct, false_positives, false_negatives = 0, 0, 0

        # Create a folder for this threshold
        threshold_folder = os.path.join(SAVE_FOLDER, f"threshold_{threshold}")
        os.makedirs(threshold_folder, exist_ok=True)

        for image_path in clip_detected_images:
            image_name = os.path.basename(image_path)  # Extract filename
            clip_prediction = "weapon"
            roboflow_prediction = roboflow_results.get(image_name, "not weapon")

            if clip_prediction == roboflow_prediction == "weapon":
                correct += 1
                # Load image
                img = Image.open(image_path)
                # Convert RGBA to RGB if needed
                if img.mode == "RGBA":
                    img = img.convert("RGB")
                # Save the correctly classified image
                img.save(os.path.join(threshold_folder, image_name), format="JPEG")

            elif clip_prediction == "weapon" and roboflow_prediction == "not weapon":
                false_positives += 1
            elif clip_prediction == "not weapon" and roboflow_prediction == "weapon":
                false_negatives += 1

        total_predicted_weapons = correct + false_positives
        total_actual_weapons = correct + false_negatives

        precision = correct / total_predicted_weapons if total_predicted_weapons > 0 else 0
        recall = correct / total_actual_weapons if total_actual_weapons > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        comparison_stats[threshold] = {
            "correct": correct,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "precision": round(precision, 2),
            "recall": round(recall, 2),
            "f1_score": round(f1_score, 2),
        }

    return comparison_stats

def main():
    """Main execution function."""
    # Load image paths
    image_paths = [os.path.join(IMAGE_FOLDER, f) for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    # Reduce dataset for testing (optional)
    image_paths = image_paths[:100]  # Process only 100 images for faster debugging

    print(f"Loaded {len(image_paths)} images.")

    # Load ground truth from Roboflow
    roboflow_results = load_roboflow_results(RESULTS_FILE)

    # Define thresholds
    thresholds = [i * 0.1 for i in range(1, 10)]  # 0.1, 0.2, ..., 0.9

    # Analyze with CLIP
    clip_results_per_threshold = analyze_with_clip(image_paths, thresholds)

    # Compute comparison statistics & save correctly classified images
    comparison_stats = compare_results(clip_results_per_threshold, roboflow_results, IMAGE_FOLDER)

    # Find the best threshold
    best_threshold = max(comparison_stats, key=lambda t: comparison_stats[t]["f1_score"])
    best_f1 = comparison_stats[best_threshold]["f1_score"]

    # Print and save results
    print(f"Best threshold: {best_threshold} with F1-score: {best_f1}")
    print("Comparison stats per threshold:", json.dumps(comparison_stats, indent=4))

    with open("comparison_results.json", "w") as f:
        json.dump(comparison_stats, f, indent=4)


if __name__ == "__main__":
    main()
