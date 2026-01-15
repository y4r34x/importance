"""Random Forest model for predicting contract terms."""
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

from negotiation.data.loaders import load_cuad_data
from negotiation.data.transforms import encode_boolean_columns


class TermPredictor:
    """
    Random Forest model for predicting contract terms from partial input.

    Given some known contract terms (e.g., "has Audit Rights"), predicts
    the most likely values for unknown terms based on patterns learned
    from the CUAD dataset.

    Example:
        >>> predictor = TermPredictor()
        >>> predictor.fit()
        >>> result = predictor.predict({'Audit Rights': 1, 'Anti-Assignment': 0})
        >>> print(result['Cap On Liability'])
        {'prediction': 1, 'probability': 0.78}
    """

    # Binary term columns from CUAD (excluding metadata and non-binary columns)
    TERM_COLUMNS = [
        'Termination For Convenience',
        'Change Of Control',
        'Anti-Assignment',
        'Revenue/Profit Sharing',
        'Ip Ownership Assignment',
        'Joint Ip Ownership',
        'Non-Transferable License',
        'Source Code Escrow',
        'Post-Termination Services',
        'Audit Rights',
        'Uncapped Liability',
        'Cap On Liability',
        'Liquidated Damages',
    ]

    def __init__(self, n_estimators: int = 100, random_state: int = 42):
        """
        Initialize the predictor.

        Args:
            n_estimators: Number of trees in the forest
            random_state: Random seed for reproducibility
        """
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.models = {}  # One model per target term
        self.data = None
        self._is_fitted = False

    def fit(self, data_path: str = 'data/training/cuad.tsv') -> 'TermPredictor':
        """
        Train the model on CUAD data.

        Args:
            data_path: Path to the CUAD TSV file

        Returns:
            self for method chaining
        """
        # Load and preprocess data
        df = load_cuad_data(data_path)
        df = encode_boolean_columns(df)

        # Extract only the term columns we care about
        self.data = df[self.TERM_COLUMNS].copy()

        # Drop rows with any missing values for clean training
        self.data = self.data.dropna()

        # Train one model per term (each term predicted from all others)
        for target_col in self.TERM_COLUMNS:
            feature_cols = [c for c in self.TERM_COLUMNS if c != target_col]
            X = self.data[feature_cols].values
            y = self.data[target_col].values.astype(int)

            model = RandomForestClassifier(
                n_estimators=self.n_estimators,
                random_state=self.random_state,
                max_depth=5,  # Prevent overfitting on small dataset
                min_samples_leaf=10,
            )
            model.fit(X, y)
            self.models[target_col] = {
                'model': model,
                'feature_cols': feature_cols,
            }

        self._is_fitted = True
        return self

    def predict(self, known_terms: dict) -> dict:
        """
        Predict unknown terms from known ones.

        Args:
            known_terms: Dictionary mapping term names to values (0 or 1)
                e.g., {'Audit Rights': 1, 'Anti-Assignment': 0}

        Returns:
            Dictionary with predictions for unknown terms:
            {
                'Cap On Liability': {'prediction': 1, 'probability': 0.78},
                ...
            }
        """
        if not self._is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")

        results = {}

        # Predict each term that wasn't provided as input
        for target_col in self.TERM_COLUMNS:
            if target_col in known_terms:
                continue  # Skip terms we already know

            model_info = self.models[target_col]
            model = model_info['model']
            feature_cols = model_info['feature_cols']

            # Build feature vector from known terms
            # Use median of training data for unknown features
            X = []
            for col in feature_cols:
                if col in known_terms:
                    X.append(known_terms[col])
                else:
                    # Use training median as fallback
                    X.append(self.data[col].median())

            X = np.array(X).reshape(1, -1)

            # Get prediction and probability
            pred = model.predict(X)[0]
            proba = model.predict_proba(X)[0]
            # probability of the predicted class
            prob = proba[1] if pred == 1 else proba[0]

            results[target_col] = {
                'prediction': int(pred),
                'probability': round(float(prob), 3),
            }

        return results

    def evaluate(self, cv_folds: int = 5) -> dict:
        """
        Run cross-validation to get honest accuracy estimates.

        Args:
            cv_folds: Number of cross-validation folds

        Returns:
            Dictionary with per-term accuracy scores
        """
        if self.data is None:
            raise RuntimeError("No data loaded. Call fit() first.")

        results = {}

        for target_col in self.TERM_COLUMNS:
            feature_cols = [c for c in self.TERM_COLUMNS if c != target_col]
            X = self.data[feature_cols].values
            y = self.data[target_col].values.astype(int)

            model = RandomForestClassifier(
                n_estimators=self.n_estimators,
                random_state=self.random_state,
                max_depth=5,
                min_samples_leaf=10,
            )

            scores = cross_val_score(model, X, y, cv=cv_folds, scoring='accuracy')

            # Also get baseline (always predict majority class)
            majority_class = 1 if y.mean() > 0.5 else 0
            baseline = (y == majority_class).mean()

            results[target_col] = {
                'accuracy': round(float(scores.mean()), 3),
                'std': round(float(scores.std()), 3),
                'baseline': round(float(baseline), 3),
                'lift': round(float(scores.mean() - baseline), 3),
            }

        return results

    def feature_importance(self) -> dict:
        """
        Get feature importance for each target term.

        Returns:
            Dictionary mapping each term to its top predictive features
        """
        if not self._is_fitted:
            raise RuntimeError("Model not fitted. Call fit() first.")

        results = {}

        for target_col in self.TERM_COLUMNS:
            model_info = self.models[target_col]
            model = model_info['model']
            feature_cols = model_info['feature_cols']

            importances = model.feature_importances_
            sorted_idx = np.argsort(importances)[::-1]

            top_features = []
            for idx in sorted_idx[:5]:  # Top 5 features
                top_features.append({
                    'feature': feature_cols[idx],
                    'importance': round(float(importances[idx]), 3),
                })

            results[target_col] = top_features

        return results
